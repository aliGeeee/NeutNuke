import cv2
import os
import sys

cellsDir = sys.argv[1]
print(cellsDir)

try:
	try:
		outDir = 'smallCells/{}'.format(cellsDir.replace('./allCells/', ''))
		os.mkdir(outDir)
	except:
		pass

	cellDir = [i for i in os.listdir(cellsDir) if '.DS_Store' not in i]

	for cell in cellDir:
		img = cv2.imread('{}/{}'.format(cellsDir, cell))
		ratio = 0.088010/0.249711
		smallImg = cv2.resize(img, (0,0), fx=ratio, fy=ratio)
		cv2.imwrite('{}/{}'.format(outDir, cell), smallImg)
except:
	print(cellsDir + " ERROR")