import os
import sqlite3
import random
from shutil import copyfile

try:
	os.mkdir('NVCells')
except:
	pass

outputDir = 'output'
imageDirs = os.listdir(outputDir)

for imageDir in [i for i in imageDirs if '.DS_Store' not in i and '.db' not in i]:
	try:
		os.mkdir('NVCells/'+imageDir)
	except:
		pass

	cellImages = os.listdir('{}/{}'.format(outputDir, imageDir))
	sampleList = random.sample([j for j in cellImages if '.DS_Store' not in j and '.db' not in j], min(200, len(cellImages)-1))
	
	for chosen in sampleList:
		copyfile('cellsReal/{}/{}.jpg'.format(imageDir, chosen), 'NVCells/{}/{}.jpg'.format(imageDir, chosen))