import numpy as np
import scipy as sp
from scipy import signal
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy
from progress.bar import Bar

#setting manual values
cellThreshValue = 200
nucThreshValue = 80
otsu=True
mainOutputDir = 'output'
mainInputDir = 'cells'

#function for calculating circularity
def calcCirc(cont):
	return 4*np.pi*cv2.contourArea(cont)/cv2.arcLength(cont, True)**2

try:
	inDir = os.listdir(mainInputDir)
except:
	print("Sad.")
	quit()

imageData = []

#importing image and making grayscale
for image in inDir:
	if image == ".DS_Store" or image == "._.DS_Store":
		continue
	try:
		os.mkdir('output/%s'%image[:-4])
	except:
		pass

	print("Analysing nuclei %s..."%image)

	#bar = Bar('\tProcessing', max=noCellCon)
	#bar.next()
	try:
		img = cv2.imread('%s/%s'%(mainInputDir, image))
		img = img[98:img.shape[0]-98, 98:img.shape[1]-98]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
		print("%s isn't an image file!"%image)
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
				if i < 240:
					noBackCellGrey.append(i)

		retFG, fakeNucThresh = cv2.threshold(np.array(noBackCellGrey).astype(np.uint8), 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		ret, nucThresh = cv2.threshold(cellGrey, retFG, 255, cv2.THRESH_BINARY_INV)
	else:
		ret, nucThresh = cv2.threshold(cellGrey, nucThreshValue, 255, cv2.THRESH_BINARY_INV)

	#ret, nucConRaw, hierarchy = cv2.findContours(nucThresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	#nucCon = sorted(nucConRaw, key=lambda x: -cv2.contourArea(x))

	#distance transforms
	distTrans = cv2.distanceTransform(nucThresh, cv2.DIST_L2, 3)
	distTrans *= 255/np.amax(distTrans)
	cv2.imwrite('output/%s/%sThresh.jpg'%(image[:-4], image[:-4]), nucThresh)
	cv2.imwrite('output/%s/%sDT.jpg'%(image[:-4], image[:-4]), distTrans)

	ret, DTThresh = cv2.threshold(distTrans, 150, 255, cv2.THRESH_BINARY)
	cv2.imwrite('output/%s/%sDTThresh.jpg'%(image[:-4], image[:-4]), DTThresh)
	cv2.imwrite('output/%s/%s.jpg'%(image[:-4], image[:-4]), img)

	noBackCellGrey.sort()

	#bimodality and laplacian calculations
	histArray = np.array(np.histogram(np.array(noBackCellGrey), bins=range(255)))
	smoothed = signal.savgol_filter(histArray[0], 25, 2)
	sk = sp.stats.skew(noBackCellGrey)
	ku = sp.stats.kurtosis(noBackCellGrey)
	bc = round((sk**2+1)/(ku+3), 3)

	greyLap = round(cv2.Laplacian(gray, cv2.CV_64F).var(),3)

	plt.hist(np.array(noBackCellGrey).astype(np.uint8).ravel(),256,[0,256])
	plt.axvline(x=retFG, color='g')
	plt.plot(histArray[1][:-1], smoothed, color='r')
	plt.title('BC = %s, p = %s, lap = %s'%(bc, pValue, greyLap))

	plt.savefig('output/%s/%sHist.jpg'%(image[:-4], image[:-4]))
	plt.close()

print("Done")