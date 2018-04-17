import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy

def calcCirc(cont):
	return 4*np.pi*cv2.contourArea(cont)/cv2.arcLength(cont, True)**2

#creating an output directory
try:
	os.mkdir('output')
except:
	pass

#setting manual threshold values
cellThreshValue = 200
nucThreshValue = 110

try:
	dirs = os.listdir('images')
except:
	print("Make sure there is folder called 'images' containing input images.")
	quit()

imageData = []

#importing image and making grayscale
for imageFile in dirs:
	if imageFile == ".DS_Store":
		continue

	print("Analysing %s..."%imageFile)
	outputDir = 'output/%s'%imageFile[:-4]
	try:
		os.mkdir(outputDir)
	except:
		pass

	try:
		img = cv2.imread('images/%s'%imageFile)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
		print("%s isn't an image file!"%imageFile)
		continue
	
	#thresholding for cells
	ret, cellThresh = cv2.threshold(gray, cellThreshValue, 255, cv2.THRESH_BINARY_INV)
	cv2.imwrite('%s/thresh_200.jpg'%outputDir, cellThresh)

	#generating contours around cells
	img2, cellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	origImg = img

	#generate output and summary stats
	nucData = []
	cellData = []
	totCellArea = 0
	totNucArea = 0
	validCells = 0

	#iterate through contours and isolate
	for i in range(len(cellCon)):
		cellArea = cv2.contourArea(cellCon[i])
		totCellArea += cellArea
		x, y, width, height = cv2.boundingRect(cellCon[i])

		#excluding tiny and big blobs
		if cellArea > 300 and cellArea < 1000 and calcCirc(cellCon[i])>0.5:
			#excluding cells on edges
			if not (x == 0 or x+width >= img.shape[1] or y == 0 or y+height >= img.shape[0]):
				validCells += 1
				name = "ROI_%s"%str(i)

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
				cv2.putText(imgTxt, "Area = %s"%cellArea, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))

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

				n = 0
				locTotNucArea = 0
				for j in range(len(nucCon)):
					#picking only nuclei and removing tiny artefacts 
					if hierarchy[0][j][3] == -1 and cv2.contourArea(nucCon[j]) > 3:
						conArea = cv2.contourArea(nucCon[j])
						locTotNucArea += conArea
						conHullArea = cv2.contourArea(cv2.convexHull(nucCon[j]))
						conCirc = calcCirc(nucCon[j])
						convex = conArea/conHullArea

						nucData.append([name, n+1, round(conArea/cellArea, 3), round(conCirc, 3), round(convex, 3)])
						n+=1

				if n>0:
					cellData.append([name, cellArea, round(locTotNucArea/cellArea, 3), n])
					totNucArea += locTotNucArea

	#saving stats as CSVs
	nucDF = pd.DataFrame(np.array(nucData), columns = ["Cell", "Nucleus", "Area Fraction", "Circularity", "Convexity"])
	nucDF.to_csv('%s/nucStats.csv'%outputDir)

	cellDF = pd.DataFrame(np.array(cellData), columns = ["Cell", "Cell Area", "Nuc Fraction", "No. Nuclear Frags"])
	cellDF.to_csv('%s/cellStats.csv'%outputDir)

	#generating some summary stats
	nucCircMean = round(np.mean(nucDF['Circularity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)
	nucCircSD = round(np.std(nucDF['Circularity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)

	nucConvMean = round(np.mean(nucDF['Convexity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)
	nucConvSD = round(np.std(nucDF['Convexity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)

	#saving whole image data
	imageData.append([imageFile, len(cellCon), validCells, round(totNucArea/totCellArea, 3), nucCircMean, nucCircSD, nucConvMean, nucConvSD])

	#plotting some scatterplots
	xQuant = 'Convexity'
	yQuant = 'Area Fraction'
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.0])
	plt.xticks(np.arange(0.0, 1.1, 0.1))
	plt.yticks(np.arange(0.0, 1.1, 0.1))
	plt.scatter(nucDF[xQuant].values.astype('float'), nucDF[yQuant].values.astype('float'))
	plt.title(imageFile)
	plt.xlabel(xQuant)
	plt.ylabel(yQuant)
	plt.savefig('%s/testScatter.jpg'%outputDir)
	plt.close()

imgDF = pd.DataFrame(np.array(imageData), columns = ["Image File", "No. Cells", "No. Valid Cells", "Nuc. Area Frac.", "Circ. Mean", "Circ. SD", "Conv. Mean", "Conv. SD"])
imgDF.to_csv('output/imageStats.csv')

print("Done")