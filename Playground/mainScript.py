import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy

#creating an output directory
try:
	os.mkdir('output')
except:
	pass

#setting manual threshold values
cellThreshValue = 200
nucThreshValue = 100

try:
	dirs = os.listdir('images')
except:
	print("Make sure there is folder called 'images' containing input images.")
	quit()

#importing image and making grayscale
for imageFile in dirs:
	print("Analysing %s..."%imageFile)
	outputDir = 'output/%s'%imageFile[:-4]
	try:
		os.mkdir(outputDir)
	except:
		pass

	img = cv2.imread('images/%s'%imageFile)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#thresholding for cells
	ret, threshCell = cv2.threshold(gray, cellThreshValue, 255, cv2.THRESH_BINARY_INV)
	cv2.imwrite('%s/thresh_200.jpg'%outputDir, threshCell)

	#generating contours around cells
	img2, cellCon, hierarchy = cv2.findContours(threshCell, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	origImg = img

	#generate output and summary stats
	nucData = []

	#iterate through contours and isolate
	for i in range(len(cellCon)):
		area = cv2.contourArea(cellCon[i])
		x, y, width, height = cv2.boundingRect(cellCon[i])

		#excluding tiny and big blobs
		if area > 300 and area < 1000:
			#excluding cells on edges
			if not (x == 0 or x+width >= img.shape[1] or y == 0 or y+height >= img.shape[0]):
				#creating mask for cells
				rawMask = np.zeros((img.shape[0], img.shape[1], 1), dtype = "uint8")
				cv2.drawContours(rawMask, cellCon, i, (255), -1)
				revMask = np.bitwise_not(rawMask)
				res1 = cv2.bitwise_and(img, img, mask = rawMask)
				res2 = res1 + revMask

				#isolating cells
				margin = 100
				rawROI = np.zeros((height+2*margin, width+2*margin, 3))+255
				rawROI[margin:margin+height, margin:margin+width] = res2[y:y+height, x:x+width]

				#creating output image of isolated cell
				imgTxt = copy.copy(rawROI)
				cv2.putText(imgTxt, "Area = %s"%area, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))

				name = "ROI_%s"%str(i)

				try:
					os.mkdir("%s/cells"%outputDir)
				except:
					pass

				try:
					os.mkdir("%s/cells/%s"%(outputDir,name))
				except:
					pass

				cv2.imwrite("%s/cells/%s/%s.jpg"%(outputDir,name,name), imgTxt)

				#nuclear analysis
				rawROI = rawROI.astype(np.uint8)
				gray = cv2.cvtColor(rawROI, cv2.COLOR_BGR2GRAY)

				ret, nucThresh = cv2.threshold(gray, nucThreshValue, 255, cv2.THRESH_BINARY_INV)
				cv2.imwrite('%s/cells/%s/thresh_120.jpg'%(outputDir,name), nucThresh)

				ret, nucConRaw, hierarchy = cv2.findContours(nucThresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
				nucCon = sorted(nucConRaw, key=lambda x: -cv2.contourArea(x))

				n = 1
				for j in range(len(nucCon)):
					#picking only nuclei and removing tiny artefacts 
					if hierarchy[0][j][3] == -1 and cv2.contourArea(nucCon[j]) > 3:
						conArea = cv2.contourArea(nucCon[j])
						conPeri = cv2.arcLength(nucCon[j], True)
						conHullArea = cv2.contourArea(cv2.convexHull(nucCon[j]))
						conCirc = 4*np.pi*conArea/conPeri**2
						convex = conArea/conHullArea
						nucData.append([name, n, round(conArea/area, 3), round(conCirc, 3), round(convex, 3)])
						n+=1

				# # noise removal
				# kernel = np.ones((1,1), np.uint8)
				# opening = cv2.morphologyEx(threshNuclear, cv2.MORPH_OPEN, kernel, iterations = 2)
				# cv2.imwrite('output/cells/%s/noNoise_100.jpg'%name, opening)


				# sure_bg = cv2.dilate(opening, kernel, iterations=3)
				# cv2.imwrite('output/cells/%s/bg.jpg'%name, sure_bg)

				# #Finding sure foreground area
				# dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)*100
				# # dist_transform = opening
				# ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

				# # Finding unknown region
				# sure_fg = np.uint8(sure_fg)
				# unknown = cv2.subtract(sure_bg,sure_fg)
				# # 
				# cv2.imwrite('output/cells/%s/fg.jpg'%name, sure_fg)
				# cv2.imwrite('output/cells/%s/unknown.jpg'%name, unknown)
				# cv2.imwrite('output/cells/%s/DT.jpg'%name, dist_transform)

				# # Marker labelling
				# ret, markers = cv2.connectedComponents(sure_fg)
				# # Add one to all labels so that sure background is not 0, but 1
				# markers = markers+1
				# # Now, mark the region of unknown with zero
				# markers[unknown==255] = 0

				# markers = cv2.watershed(rawROI,markers)
				# rawROI[markers == -1] = [0,0,255]

				# #markers2 = cv2.applyColorMap(255-gray, cv2.COLORMAP_JET)

				# cv2.imwrite('output/cells/%s/markers.jpg'%name,markers)
				# #cv2.imwrite('output/cells/%s/markersC.jpg'%name,markers2)
				# cv2.imwrite('output/cells/%s/imggg.jpg'%name,rawROI)

	nucDF = pd.DataFrame(np.array(nucData), columns = ["Cell", "Nucleus", "Area Fraction", "Circularity", "Convexity"])
	nucDF.to_csv("%s/nucStats.csv"%outputDir)

	x = nucDF['Circularity'].values
	y = nucDF['Area Fraction'].values

	fig = plt.figure()
	plt.scatter(x, y)
	plt.title('Test Scatter ')
	plt.xlabel('Circularity')
	plt.ylabel('Area Fraction')
	fig.savefig('%s/testScatter.jpg'%outputDir)

print("Done")