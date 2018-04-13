import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import copy

def removeEdgeObj(x, y, width, height, dimX, dimY):
	if x == 0 or y == 0:
		return False
	elif x+width >= dimX or y+height >= dimY:
		return False
	else:
		return True

try:
	os.mkdir("output")
except:
	pass

img = cv2.imread('rawCells.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, threshNuclear = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('output/thresh_120.jpg', threshNuclear)

ret, threshCell = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('output/thresh_200.jpg', threshCell)

img2, contours, hierarchy = cv2.findContours(threshCell, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

origImg = img

#iterate through contours and isolate
for i in range(len(contours)):
	area = cv2.contourArea(contours[i])
	x, y, width, height = cv2.boundingRect(contours[i])
	if area > 300 and area < 1000:
		if removeEdgeObj(x, y, width, height, img.shape[1], img.shape[0]) == True:
			rawMask = np.zeros((img.shape[0], img.shape[1], 1), dtype = "uint8")
			cv2.drawContours(rawMask, contours, i, (255), -1)

			revMask = np.bitwise_not(rawMask)
			#cv2.drawContours(origImg, contours, i, (0,0,255), -1)
			#cv2.imwrite("Masks_%s.png"%str(i), rawMask)

			res1 = cv2.bitwise_and(img, img, mask = rawMask)
			res2 = res1 + revMask
			cv2.imwrite("output/sad.png", res2)

			margin = 100
			rawROI = np.zeros((height+2*margin, width+2*margin, 3))+255
			rawROI[margin:margin+height, margin:margin+width] = res2[y:y+height, x:x+width]

			area = cv2.contourArea(contours[i])

			imgTxt = copy.copy(rawROI)

			cv2.putText(imgTxt, "Area = %s"%area, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))

			name = "ROI_%s"%str(i)

			try:
				os.mkdir("output/cells")
			except:
				pass

			try:
				os.mkdir("output/cells/%s"%name)
			except:
				pass

			cv2.imwrite("output/cells/%s/%s.jpg"%(name,name), imgTxt)

			#nuclear analysis
			rawROI = rawROI.astype(np.uint8)
			gray = cv2.cvtColor(rawROI, cv2.COLOR_BGR2GRAY)

			ret, nucThresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
			cv2.imwrite('output/cells/%s/thresh_120.jpg'%name, nucThresh)

			lmao, nucCon, hierarchy = cv2.findContours(nucThresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

			n=0
			for j in range(len(nucCon)):
				if hierarchy[0][j][3] == -1:
					if cv2.contourArea(nucCon[j]) > 3:
						print(name, cv2.contourArea(nucCon[j]), area, round(cv2.contourArea(nucCon[j])/area,2))
						n+=1

			imgTxt = copy.copy(rawROI)

			cv2.putText(imgTxt, "Area = %s"%area, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))


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

print("Done")