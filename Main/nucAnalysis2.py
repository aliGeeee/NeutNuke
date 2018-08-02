import copy
import cv2
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import neutFunctions as nf
import numpy as np
import os
import pandas as pd
import scipy as sp
from scipy import signal
import sqlite3
import sys

#setting manual values
cellThreshValue = 200
mainOutputDir = 'output'

cellsDir = sys.argv[1]

print("Analysing nuclei in %s..."%cellsDir)
ROIDirs = os.listdir(cellsDir)

batchOutputDir = "%s/%s"%(mainOutputDir, cellsDir.replace("./cells/", ""))

try:
	os.mkdir(mainOutputDir)
except:
	pass

try:
	os.mkdir(batchOutputDir)
except:
	pass

DBname = nf.createDB(batchOutputDir)
conn = sqlite3.connect('{}/{}'.format(batchOutputDir, DBname))
c = conn.cursor()
	
for ROI in [i for i in ROIDirs if i not in ('.DS_Store', '._.DS_Store')]:
	try:
		print("\t%s"%ROI)
		img = cv2.imread("%s/%s"%(cellsDir,ROI))
		img = img[:img.shape[0]-30].astype(np.uint8)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	except:
		print("\tSomething went wrong! Perhaps %s isn't an image file!"%ROI)
		continue

	ret, cellThresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
	#generating contours around cells
	img2, rawCellCon, hierarchy = cv2.findContours(cellThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#generate output and summary stats
	nucData = {'totNucArea':0}
	cellData = {}

	#iterate through contours and isolate
	cellCon = sorted(rawCellCon, key=lambda x:-cv2.contourArea(x))
	cellArea = cv2.contourArea(cellCon[0])
	cellData['cellArea'] = cellArea
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

	histArray = np.array(np.histogram(np.array(noBackCellGrey), bins=range(255)))
	smoothed = signal.savgol_filter(histArray[0], 25, 2)

	dip1 = smoothed[int(retFG)]
	leftPeak = max(smoothed[:int(retFG)])
	rightPeak = max(smoothed[int(retFG):])
	try:
		realdip = min(smoothed[list(smoothed).index(leftPeak):list(smoothed).index(rightPeak)])
	except:
		realdip = dip1

	if leftPeak/realdip < 4 and rightPeak/realdip < 2:
		print("Reject %s"%ROI)
		continue

	rawNucThreshValue = list(smoothed).index(realdip)
	nucThreshValue = min(rawNucThreshValue, 110)
	ret, nucThresh = cv2.threshold(cellGrey, nucThreshValue, 255, cv2.THRESH_BINARY_INV)

	try:
		os.mkdir('%s/%s'%(batchOutputDir, ROI[:-4]))
	except:
		pass

	plt.hist(np.array(noBackCellGrey).astype(np.uint8).ravel(),256,[0,256])
	plt.axvline(x=nucThreshValue, color='r')
	plt.savefig('%s/%s/Hist.png'%(batchOutputDir, ROI[:-4]))
	plt.close()

	cv2.imwrite('%s/%s/mask.jpg'%(batchOutputDir, ROI[:-4]), nucThresh)
	cv2.imwrite('%s/%s/cell.jpg'%(batchOutputDir, ROI[:-4]), cell)

	#DB for cells
	c.execute('''INSERT INTO Cells (name, cellArea) VALUES (?,?);''', (ROI[:-4], cellData['cellArea'],))
	cellID = c.lastrowid

	#nuclear analysis

	nucMinArea = 15
	ret, nucCon, hierarchyRaw = cv2.findContours(nucThresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	nucData = {i:{'hierarchy':list(hierarchyRaw[0][i])} for i in range(len(nucCon)) if cv2.contourArea(nucCon[i]) > nucMinArea}

	lvl1 = [i for i in nucData if nucData[i]['hierarchy'][3] == -1]
	lvl1_sorted = sorted(lvl1, key=lambda x:-cv2.contourArea(nucCon[x]))
	
	for lvl1Obj in lvl1_sorted:
		#donut analysis
		nucData[lvl1Obj]['donutObjs'] = [i for i in nucData if nucData[i]['hierarchy'][3]==lvl1_sorted[0]]
		#area analysis
		nucData[lvl1Obj]['rawArea'] = cv2.contourArea(nucCon[lvl1Obj])
		nucData[lvl1Obj]['netArea'] = nucData[lvl1Obj]['rawArea'] - sum([cv2.contourArea(nucCon[i]) for i in nucData[lvl1Obj]['donutObjs']])

		#circularity and convexity
		nucData[lvl1Obj]['circularity'] = round(nf.calcCirc(nucCon[lvl1Obj]), 3)
		nucData[lvl1Obj]['convexity'] = round(nf.calcConv(nucCon[lvl1Obj]), 3)

		#DB for nuclei
		c.execute('''INSERT INTO NuclearBlobs (cellID, netArea, rawArea, circularity, convexity, donutObjs) VALUES (?,?,?,?,?,?);''',
			(cellID, nucData[lvl1Obj]['netArea'], nucData[lvl1Obj]['rawArea'], nucData[lvl1Obj]['circularity'], nucData[lvl1Obj]['convexity'], len(nucData[lvl1Obj]['donutObjs']),))
		
	cellData['nucObjs'] = len(lvl1_sorted)
	cellData['netNucArea'] = sum([nucData[i]['netArea'] for i in nucData if 'netArea' in nucData[i]])
	c.execute('''UPDATE Cells SET netNucArea=?, nucObjs=? WHERE id=?;''', (cellData['netNucArea'], cellData['nucObjs'], cellID,))
	
	
	# nucCon = sorted(nucConRaw, key=lambda x: -cv2.contourArea(x))
	# n = 0
	
	# locTotNucArea = 0
	# for j in range(len(nucCon)):
	# 	#picking only nuclei and removing tiny artefacts 
	# 	if hierarchy[0][j][3] == -1 and cv2.contourArea(nucCon[j]) > nucMinArea:
	# 		conArea = cv2.contourArea(nucCon[j])
	# 		locTotNucArea += conArea
	# 		conHullArea = cv2.contourArea(cv2.convexHull(nucCon[j]))
	# 		conCirc = nf.calcCirc(nucCon[j])
	# 		convex = conArea/conHullArea

	# 		nucData.append([ROI, n+1, round(conArea/cellArea, 3), round(conCirc, 3), round(convex, 3)])
	# 		n+=1

	# 	elif hierarchy[0][j][3]

	# if n>0:
	# 	cellData.append([ROI, cellArea, round(locTotNucArea/cellArea, 3), n])
	# 	totNucArea += locTotNucArea
	# 	totNucCount += n


	

# imgDF = pd.DataFrame(np.array(imageData), columns = ["Image File", "No. Cells", "No. Valid Cells",
#		 "Nuc. Area Frac.", "Circ. Mean", "Circ. SD", "Conv. Mean", "Conv. SD", "n Mean"])
# imgDF.to_csv('%s/imageStats.csv'%mainOutputDir)

conn.commit()
conn.close()

print("Done")