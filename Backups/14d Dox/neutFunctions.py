import numpy as np
import cv2
import pandas as pd
import sqlite3
import os
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

def calcCirc(cont):
	return 4*np.pi*cv2.contourArea(cont)/cv2.arcLength(cont, True)**2

def calcConv(cont):
	conHullArea = cv2.contourArea(cv2.convexHull(cont))
	return cv2.contourArea(cont)/conHullArea

def cvtGrey(array):
	newArray = np.zeros((array.shape[0], array.shape[1]))
	for i in range(array.shape[0]):
		for j in range(array.shape[1]):
			newArray[i][j] = int(0.114*array[i][j][0] + 0.587*array[i][j][1] + 0.299*array[i][j][2])
	return newArray.astype(np.uint8)

def createDB(outputDir):
	x = os.listdir(outputDir)
	DBs = [i for i in x if i[-3:] == ".db"]
	DBno = max([int(i.replace('outputDB_','').replace('.db','')) for i in DBs])+1 if len(DBs) > 0 else 0
	DBname = 'outputDB_%s.db'%str(DBno)
	conn = sqlite3.connect('%s/%s'%(outputDir, DBname))
	c = conn.cursor()
	# c.execute('''CREATE TABLE Images (
	# 	id int NOT NULL AUTO_INCREMENT, 
	# 	name text, 
	# 	PRIMARY KEY (id)
	# 	);''')
	c.execute('''CREATE TABLE Cells (
		id integer PRIMARY KEY,
		name text,
		batch text,
		acceptable boolean,
		cellArea real,
		netNucArea real,
		nucObjs integer,
		circ2 real,
		lobes integer,
		cytoIntensity real,
		nucIntensity real,
		dipIntensity real
		);''')
	c.execute('''CREATE TABLE NuclearBlobs (
		id integer PRIMARY KEY,
		cellID integer,
		netArea real,
		rawArea real,
		circularity real,
		convexity real,
		donutObjs integer,
		FOREIGN KEY (cellID) REFERENCES Cells(id)
		);''')
	conn.commit()
	conn.close()
	return DBname

def createResultFiles():
	return None

def clean(grey, minArea):
	ret, cellThresh1 = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY)
	ret, rawCellCon1, hierarchy = cv2.findContours(cellThresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon1 = [x for x in rawCellCon1 if cv2.contourArea(x)<minArea]
	mask1 = np.zeros(grey.shape, np.uint8)
	cv2.drawContours(mask1, cellCon1, -1, 255, -1)

	ret, cellThresh2 = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY_INV)
	ret, rawCellCon2, hierarchy = cv2.findContours(cellThresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon2 = [x for x in rawCellCon2 if cv2.contourArea(x)<minArea]
	mask2 = np.zeros(grey.shape, np.uint8)
	cv2.drawContours(mask2, cellCon2, -1, 255, -1)

	mask = cv2.bitwise_and(mask1, mask2)
	cleanGrey = cv2.bitwise_xor(grey, mask)

	return cleanGrey

def countLobes(rawGrey):
	class LobeRemnant(object):
		def __init__(self, lineage, allIter, startArray):
			self.lineage = [i for i in lineage]
			self.allIter = allIter
			self.terminal = False
			self.iter = 0
			self.array = startArray
			self.childLobes = []
			self.history = {0: startArray}
			self.dilation = -1
			self.dilating = True
			self.colours = []
			self.finalSeed = np.zeros(startArray.shape, np.uint8)

			self.erode()

		def erode(self):
			self.newArray = cv2.erode(self.array, kernel = np.ones((3,3), np.uint8), iterations = 1)

			ret, self.rawCons, self.erodeHierarchy = cv2.findContours(self.newArray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			self.cons = [self.rawCons[i] for i in range(len(self.rawCons)) if self.erodeHierarchy[0][i][3] == -1]

			#end of the line
			if len(self.cons) == 0:
				self.terminal = True
				self.dilation = self.iter
				self.history[self.iter] = self.array

			#one way forward
			elif len(self.cons) == 1:
				if self.iter < 10:
					self.iter += 1
					self.allIter += 1
					self.array = self.newArray
					self.history[self.iter] = self.array
					self.erode()
				else:
					self.terminal = True
					self.dilation = self.iter
					self.history[self.iter] = self.array
			
			#time to split
			else:
				self.dilation = self.iter + 1
				for i in range(len(self.cons)):
					self.mask = np.zeros(self.array.shape, np.uint8)
					cv2.drawContours(self.mask, self.cons, i, 255, -1)
					self.childLobes.append(LobeRemnant([j for j in self.lineage]+[i], self.allIter, self.mask))

		def findTerminals(self):
			allTerminals = []
			for child in self.childLobes:
				if child.terminal:
					allTerminals += [child]
				else:
					allTerminals += child.findTerminals()
			return allTerminals

		def getChildrenColours(self):
			for child in self.childLobes:
				if child.terminal:
					self.colours += child.colours
				else:
					self.colours += child.getChildrenColours()
			return self.colours

		def setDilation(self):
			for child in self.childLobes:
				child.setDilation()
			self.dilation = self.iter

		def dilate(self, seed):
			if len(self.colours) == 0:
				self.getChildrenColours()

			if self.dilating == False or self.dilation == 0:
				self.dilating = False
				#finished dilation self
				self.finalSeed = seed

			elif True not in [i.dilating for i in self.childLobes] or len(self.childLobes) == 0:
				#dilate self since all children are dilated
				self.newSeed = np.zeros(seed.shape, np.uint8)

				self.blobsDict = {}
				for colour in self.colours:
					ret, self.mask1 = cv2.threshold(seed, colour-1, 255, cv2.THRESH_BINARY)
					ret, self.mask2 = cv2.threshold(seed, colour+1, 255, cv2.THRESH_BINARY)
					ret, self.mask = cv2.threshold(cv2.bitwise_xor(self.mask1, self.mask2), 127, 255, cv2.THRESH_BINARY)

					ret, self.rawBlobCons, blobHierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
					self.blobCons = [i for i in self.rawBlobCons if cv2.contourArea(i) > -1]

					if len(self.blobCons) == 0:
						raise UserWarning("NO BLOBS in {}".format(self.lineage))
					self.blobsDict[colour] = self.blobCons

				for pt in [(y,x) for y in range(seed.shape[0]) for x in range(seed.shape[1])]:
					if self.history[self.dilation-1][pt] < 255:
						continue
					self.distLog = {'minDist':None, 'colour':None}
					for colour in self.colours:
						for blob in self.blobsDict[colour]:
							dist = -cv2.pointPolygonTest(blob, (pt[1], pt[0]), True)
							if self.distLog['minDist'] == None or dist < self.distLog['minDist']:
								self.distLog['minDist'] = dist
								self.distLog['colour'] = colour

					self.newSeed[pt] = self.distLog['colour']

				self.dilation -= 1
				if self.dilation == 0:
					self.dilating = False
				self.dilate(self.newSeed)

			else:
				#dilate children since there are some children not dilated
				for child in [i for i in self.childLobes if i.dilating == True]:
					if len(child.colours) == 0:
						raise UserWarning("NO COLOURS in {}".format(child.lineage))
					#get children to dilate
					child.dilate(seed)
				selfSeed = np.zeros(seed.shape, np.uint8)
				for child in self.childLobes:
					selfSeed += child.finalSeed
				selfSeed = selfSeed.astype(np.uint8)
				self.dilate(selfSeed)

	# grey = clean(rawGrey, 20)
	# ret, rawInitCons, hierarchy = cv2.findContours(grey, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# initCons = [rawInitCons[i] for i in range(len(rawInitCons)) if hierarchy[0][i][3] == -1]
		
	# mask = np.zeros(grey.shape, np.uint8)
	# cv2.drawContours(mask, initCons, -1, 255, -1)

	mask = clean(rawGrey, 20)

	#generating lobes
	x = LobeRemnant(lineage=[0], allIter=0, startArray=mask)
	terminals = x.findTerminals()

	termsToReturn = len(terminals)
	if termsToReturn == 0:
		termsToReturn = 1
		finalImg = np.multiply(mask, 0.5, casting='unsafe').astype(np.uint8)
	else:
		#filling lobes
		rawColours = [i/(len(terminals)+1)*255 for i in range(len(terminals)+1)][1:]
		rawColours.reverse()
		colours = np.asarray(rawColours).astype(np.uint8)

		seed = np.zeros(mask.shape, np.uint8)

		for i in range(len(terminals)):
			terminals[i].colours = [colours[i]]
			toColour = np.multiply(terminals[i].history[max(terminals[i].history.keys())], colours[i]/255, casting='unsafe').astype(np.uint8)
			seed += toColour

		x.dilate(seed)
		finalImg = x.finalSeed

	return (termsToReturn, myColourMap(finalImg))

def clean(grey, minArea):
	ret, cellThresh1 = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY)
	ret, rawCellCon1, hierarchy = cv2.findContours(cellThresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon1 = [x for x in rawCellCon1 if cv2.contourArea(x)<minArea]
	mask1 = np.zeros(grey.shape, np.uint8)
	cv2.drawContours(mask1, cellCon1, -1, 255, -1)

	ret, cellThresh2 = cv2.threshold(grey, 128, 255, cv2.THRESH_BINARY_INV)
	ret, rawCellCon2, hierarchy = cv2.findContours(cellThresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cellCon2 = [x for x in rawCellCon2 if cv2.contourArea(x)<minArea]
	mask2 = np.zeros(grey.shape, np.uint8)
	cv2.drawContours(mask2, cellCon2, -1, 255, -1)

	mask = cv2.bitwise_and(mask1, mask2)
	cleanGrey = cv2.bitwise_xor(grey, mask)

	ret, cleanGrey2 = cv2.threshold(cleanGrey, 128, 255, cv2.THRESH_BINARY)

	return cleanGrey2

def testParent(parent, child):
	for i in range(len(parent)):
		if parent[i] != child[i]:
			return False
	return True

def filterSeed(seed, colourList):
	mainMask = np.zeros(seed.shape, np.uint8)
	for colour in colourList:
		ret, mask1 = cv2.threshold(seed, colour-1, 255, cv2.THRESH_BINARY)
		ret, mask2 = cv2.threshold(seed, colour+1, 255, cv2.THRESH_BINARY)
		ret, mask = cv2.threshold(cv2.bitwise_xor(mask1, mask2), 127, 255, cv2.THRESH_BINARY)
		mainMask += mask.astype(np.uint8)
	return mainMask

def myColourMap(img):
	finalImg = cv2.applyColorMap(img, 4)
	for pt in [(y,x) for y in range(finalImg.shape[0]) for x in range(finalImg.shape[1])]:
		if list(finalImg[pt]) == [0, 0, 255]:
			finalImg[pt] = np.asarray([0, 0, 0])
	return finalImg

