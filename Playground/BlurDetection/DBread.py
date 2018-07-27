import sqlite3
import shutil

def checkIdentical(someList):
	if len(someList)<2:
		return True
	else:
		identical = True
		for i in range(1,len(someList)):
			if someList[0]!=someList[i]:
				identical = False
		return identical

#opening database
conn = sqlite3.connect('neutVision.sqlite3')
c = conn.cursor()

c.execute('SELECT id, name FROM Images WHERE count>=2')
allImgs = c.fetchall()

for image in allImgs:
	c.execute('SELECT quality FROM Scores WHERE img=?', (image[0],))
	allScores = c.fetchall()
	if checkIdentical(allScores):
		print("Copying %s"%image[1])
		if allScores[0][0]=='Good: nucleus visible':
			shutil.copy2('cells2/%s'%image[1], 'cells/good')
		else:
			shutil.copy2('cells2/%s'%image[1], 'cells/poor')

