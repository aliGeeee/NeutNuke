import numpy as np
import scipy as sp
import pandas as pd
from scipy import signal
import cv2
from matplotlib import pyplot as plt
import os

LeftDict = {"good":[], "poor":[]}
RightDict = {"good":[], "poor":[]}

for quality in ("good", "poor"):
	mainInputDir = 'cells/%s'%quality
	mainOutputDir = 'output/%s'%quality
	bimodalData = []

	try:
		inDir = os.listdir(mainInputDir)
	except:
		print("Sad.")
		quit()

	#importing image and making grayscale
	for image in inDir:
		if image == ".DS_Store" or image == "._.DS_Store":
			continue
		try:
			os.mkdir('%s/%s'%(mainOutputDir, image[:-4]))
		except:
			pass

		print("Analysing nuclei %s/%s..."%(quality,image))

		try:
			img = cv2.imread('%s/%s'%(mainInputDir, image))
			img = img[:img.shape[0]-30,:]
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		except:
			print("%s isn't an image file!"%image)
			continue
		
		#thresholding for cells and contouring
		ret, cellThresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
		img2, cellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		#generate output and summary stats
		nucData = []
		cellData = []
		totCellArea = 0
		totNucArea = 0
		validCells = 0
		totNucCount = 0

		#iterate through contours and isolate
		
		cellArea = cv2.contourArea(cellCon[0])
		totCellArea += cellArea
		x, y, width, height = cv2.boundingRect(cellCon[0])

		#creating mask for cells
		cell = img[y:y+height, x:x+width]
		cellGrey = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

		#nuclear masking
		noBackCellGrey = []
		for j in cellGrey.tolist():
			for i in j:
				if i < 240:
					noBackCellGrey.append(i)

		retFG, fakeNucThresh = cv2.threshold(np.array(noBackCellGrey).astype(np.uint8), 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		ret, nucThresh = cv2.threshold(cellGrey, retFG, 255, cv2.THRESH_BINARY_INV)

		cv2.imwrite('%s/%s/%s.jpg'%(mainOutputDir, image[:-4], image[:-4]), img)
		cv2.imwrite('%s/%s/%sZoom.jpg'%(mainOutputDir, image[:-4], image[:-4]), cell)
		cv2.imwrite('%s/%s/%sThresh.jpg'%(mainOutputDir, image[:-4], image[:-4]), nucThresh)

		noBackCellGrey.sort()

		#bimodality and laplacian calculations
		histArray = np.array(np.histogram(np.array(noBackCellGrey), bins=range(255)))
		smoothed = signal.savgol_filter(histArray[0], 25, 2)
		
		dip = smoothed[int(retFG)]
		leftPeak = max(smoothed[:int(retFG)])
		rightPeak = max(smoothed[int(retFG):])

		LeftDict[quality].append(leftPeak/dip)
		RightDict[quality].append(rightPeak/dip)

	# 	bimodalData.append([image, bc, hds, pValue, greyLap])

	# bimodalDF = pd.DataFrame(np.array(bimodalData), columns=["Cell", "BC", "HDT Statistic", "HDT p-value", "Laplacian Var."])
	# bimodalDF.to_csv('output/%s.csv'%quality)

plt.scatter(LeftDict["good"], RightDict["good"], color="b")
plt.scatter(LeftDict["poor"], RightDict["poor"], color="r")
plt.axvline(x=6)
plt.axhline(y=3)
plt.xlabel("Left Ratio")
plt.ylabel("Right Ratio")
plt.savefig('output/PeaksRatios.jpg')
plt.close()

print("Done")