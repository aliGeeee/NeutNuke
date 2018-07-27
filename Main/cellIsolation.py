import numpy as np
import cv2
import os
import copy
from progress.bar import Bar

inputNo = input()

#setting manual values
cellThreshValue = 200
areaMin = 3000
areaMax = 6000
mainOutputDir = 'output%s'%inputNo
mainInputDir = 'images%s'%inputNo
annotateArea = True

#function for calculating circularity
def calcCirc(cont):
	return 4*np.pi*cv2.contourArea(cont)/cv2.arcLength(cont, True)**2

#creating an output directory
try:
	os.mkdir(mainOutputDir)
except:
	pass

try:
	dirs = os.listdir(mainInputDir)
except:
	print("Make sure there is folder called 'images' containing input images.")
	quit()

#importing image and making grayscale
for imageFile in dirs:
	if imageFile == ".DS_Store":
		continue

	print("Isolating cells from %s..."%imageFile)
	outputDir = '%s/%s'%(mainOutputDir, imageFile[:-4])
	try:
		os.mkdir(outputDir)
	except:
		pass

	try:
		img = cv2.imread('%s/%s'%(mainInputDir, imageFile))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
		print("%s isn't an image file!"%imageFile)
		continue
	
	#thresholding for cells
	ret, cellThresh = cv2.threshold(gray, cellThreshValue, 255, cv2.THRESH_BINARY_INV)
	#cv2.imwrite('%s/thresh_200.jpg'%outputDir, cellThresh)

	#generating contours around cells
	img2, cellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#generate output and summary stats
	nucData = []
	cellData = []
	totCellArea = 0
	totNucArea = 0
	validCells = 0
	totNucCount = 0

	#iterate through contours and isolate
	noCellCon = len(cellCon)
	bar = Bar('\tProcessing', max=noCellCon)
	for i in range(noCellCon):
		bar.next()
		cellArea = cv2.contourArea(cellCon[i])
		totCellArea += cellArea
		x, y, width, height = cv2.boundingRect(cellCon[i])

		#excluding tiny and big blobs
		if cellArea > areaMin and cellArea < areaMax and calcCirc(cellCon[i])>0.5:
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
				try:
					os.mkdir("%s/cells"%outputDir)
				except:
					pass
				try:
					os.mkdir("%s/cells/%s"%(outputDir,name))
				except:
					pass

				if annotateArea:
					imgTxt = copy.copy(rawROI)
					cv2.putText(imgTxt, "Area = %s"%cellArea, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))
					cv2.imwrite("%s/cells/%s/%s.jpg"%(outputDir,name,name), imgTxt)
				else:
					cv2.imwrite("%s/cells/%s/%s.jpg"%(outputDir,name,name), rawROI)

	bar.finish()

print("Done")