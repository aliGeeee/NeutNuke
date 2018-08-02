import numpy as np
import cv2
import sqlite3
import os

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
		cellArea real,
		netNucArea real,
		nucObjs integer
		);''')
	c.execute('''CREATE TABLE NuclearBlobs (
		id integer PRIMARY KEY,
		cellID integer,
		netArea real,
		rawArea real,
		circularity real,
		convexity real,
		donutObjs integer,
		FOREIGN KEY (cellID) REFERENCES Cells(id));''')
	conn.commit()
	conn.close()
	return DBname