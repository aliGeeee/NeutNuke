import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy
from progress.bar import Bar

inputNo = input()

#setting manual values
cellThreshValue = 200
nucThreshValue = 80

mainOutputDir = 'output%s'%inputNo
mainInputDir = 'images%s'%inputNo

#function for calculating circularity
def calcCirc(cont):
	return 4*np.pi*cv2.contourArea(cont)/cv2.arcLength(cont, True)**2

try:
	outDirs = os.listdir(mainOutputDir)
except:
	print("Make sure you have run 'cellIsolation.py' before running 'nucAnalysis.py'.")
	quit()

imageData = []

#importing image and making grayscale
for imageDir in outDirs:
	if imageDir == ".DS_Store" or imageDir == "._.DS_Store":
		continue

	print("Analysing nuclei in %s..."%imageDir)
	imageOutDir = '%s/%s'%(mainOutputDir, imageDir)

	ROIDirs = os.listdir("%s/cells"%imageOutDir)

	bar = Bar('\tProcessing', max=noCellCon)
	for ROI in ROIDirs:
		bar.next()
		try:
			img = cv2.imread('%s/cells/%s.jpg'%(imageOutDir, ROI))
			img = img[:img.shape[0]-30,:]
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		except:
			print("%s isn't an image file!"%ROI)
			continue
		
		#thresholding for cells
		ret, cellThresh = cv2.threshold(gray, cellThreshValue, 255, cv2.THRESH_BINARY_INV)

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
		
		cellArea = cv2.contourArea(cellCon[0])
		totCellArea += cellArea
		x, y, width, height = cv2.boundingRect(cellCon[0])

		#creating mask for cells
		cell = img[y:y+height, x:x+width]
		cellGrey = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

		#nuclear masking
		if otsu:
			noBackCellGrey = []
			for j in cellGrey.tolist():
				for i in j:
					if i < 200:
						noBackCellGrey.append(i)

			retFG, fakeNucThresh = cv2.threshold(np.array(noBackCellGrey).astype(np.uint8), 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
			ret, nucThresh = cv2.threshold(cellGrey, retFG, 255, cv2.THRESH_BINARY_INV)
		else:
			ret, nucThresh = cv2.threshold(cellGrey, nucThreshValue, 255, cv2.THRESH_BINARY_INV)

		cv2.imwrite('%s/cells/%s/mask.jpg'%(imageOutDir,ROI), nucThresh)

		ret, nucConRaw, hierarchy = cv2.findContours(nucThresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
		nucCon = sorted(nucConRaw, key=lambda x: -cv2.contourArea(x))

		n = 0
		locTotNucArea = 0
		for j in range(len(nucCon)):
			#picking only nuclei and removing tiny artefacts 
			if hierarchy[0][j][3] == -1 and cv2.contourArea(nucCon[j]) > nucMinArea:
				conArea = cv2.contourArea(nucCon[j])
				locTotNucArea += conArea
				conHullArea = cv2.contourArea(cv2.convexHull(nucCon[j]))
				conCirc = calcCirc(nucCon[j])
				convex = conArea/conHullArea

				nucData.append([ROI, n+1, round(conArea/cellArea, 3), round(conCirc, 3), round(convex, 3)])
				n+=1

		if n>0:
			cellData.append([ROI, cellArea, round(locTotNucArea/cellArea, 3), n])
			totNucArea += locTotNucArea
			totNucCount += n
	bar.finish()

		#dataanalysis section
		#saving stats as CSVs
	if len(nucData) > 0:
		nucDF = pd.DataFrame(np.array(nucData), columns = ["Cell", "Nucleus", "Area Fraction", "Circularity", "Convexity"])
		nucDF.to_csv('%s/nucStats.csv'%outputDir)

	if len(cellData) > 0:
		cellDF = pd.DataFrame(np.array(cellData), columns = ["Cell", "Cell Area", "Nuc Fraction", "No. Nuclear Frags"])
		cellDF.to_csv('%s/cellStats.csv'%outputDir)

	#generating some summary stats
	nucCircMean = round(np.mean(nucDF['Circularity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)
	nucCircSD = round(np.std(nucDF['Circularity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)

	nucConvMean = round(np.mean(nucDF['Convexity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)
	nucConvSD = round(np.std(nucDF['Convexity'].values.astype('float')[nucDF['Area Fraction'].values.astype('float') > 0.1]), 3)

	nucCountMean = round(totNucCount/validCells, 3)

	#saving whole image data
	imageData.append([imageDir, len(cellCon), validCells, round(totNucArea/totCellArea, 3), nucCircMean, nucCircSD, nucConvMean, nucConvSD, nucCountMean])

	#plotting some scatterplots
	# xQuant = 'Convexity'
	# yQuant = 'Area Fraction'
	# plt.xlim([0.0, 1.0])
	# plt.ylim([0.0, 1.0])
	# plt.xticks(np.arange(0.0, 1.1, 0.1))
	# plt.yticks(np.arange(0.0, 1.1, 0.1))
	# plt.scatter(nucDF[xQuant].values.astype('float'), nucDF[yQuant].values.astype('float'))
	# plt.title(imageDir)
	# plt.xlabel(xQuant)
	# plt.ylabel(yQuant)
	# plt.savefig('%s/testScatter.jpg'%outputDir)
	# plt.close()

imgDF = pd.DataFrame(np.array(imageData), columns = ["Image File", "No. Cells", "No. Valid Cells", "Nuc. Area Frac.", "Circ. Mean", "Circ. SD", "Conv. Mean", "Conv. SD", "n Mean"])
imgDF.to_csv('%s/imageStats.csv'%mainOutputDir)

print("Done")