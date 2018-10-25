import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import scipy as sp
import sqlite3
import sys
sys.path.append('..')
import neutFunctions as nf

outputMain = '../outputClone'
sumDir = 'pics'
csvOutput = 'CSV'
try:
	os.mkdir(csvOutput)
except:
	pass

slides = nf.sortFileNames([i for i in os.listdir(outputMain) if '.DS_Store' not in i])
uniqueCloneSet = set([i[0] for i in [j.split('_') for j in slides]])
uniqueDaySet = set([i[1] for i in [j.split('_') for j in slides]])


countDonuts = False
categoryRange = range(1,7)

dictToDF = {'clone':[], 'day':[], 'replicate':[], 'nNotDonut':[], 'n':[], 'donutFrac':[]}
for i in categoryRange:
	dictToDF[str(i)] = []

for slide in slides:
	#opening DB
	outputDirDirs = os.listdir('{}/{}'.format(outputMain, slide))
	DBs = [i for i in outputDirDirs if i[-3:] == ".db"]
	DBno = max([int(i.replace('outputDB_','').replace('.db','')) for i in DBs])
	DBname = 'outputDB_%s.db'%str(DBno)
	conn = sqlite3.connect('{}/{}/{}'.format(outputMain, slide, DBname))
	c = conn.cursor()

	#analysing lobes
	c.execute('''SELECT id FROM Cells WHERE acceptable AND lobes IS NOT NULL;''')
	acceptableLobedCells = [i[0] for i in c.fetchall()]
	noDonutLobes = []
	for cellId in acceptableLobedCells:
		if not countDonuts:
			c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID = ?;''', (cellId,))
			w = sum([i[0] for i in c.fetchall()])
			if w == 0:
				c.execute('''SELECT lobes FROM Cells WHERE id=?;''', (cellId,))
				noDonutLobes.append(c.fetchone()[0])
		else:
			c.execute('''SELECT lobes FROM Cells WHERE id=?;''', (cellId,))
			noDonutLobes.append(c.fetchone()[0])
	
	n = len(noDonutLobes)
	x = slide.split('_')
	dictToDF['clone'].append(x[0])
	dictToDF['day'].append(x[1])
	dictToDF['replicate'].append(x[2])
	dictToDF['nNotDonut'].append(n)

	for i in categoryRange:
		if i < max(categoryRange):
			nlobes = [lobe for lobe in noDonutLobes if i <= lobe < i+1]
		else:
			nlobes = [lobe for lobe in noDonutLobes if i <= lobe]
		x = 0 if n == 0 else len(nlobes)/n
		dictToDF[str(i)].append(x)

	#analysing donuts
	c.execute('''SELECT id FROM Cells WHERE acceptable;''')
	acceptableCells = [i[0] for i in c.fetchall()]
	dictToDF['n'].append(len(acceptableCells))
	noDonuts = 0
	for cellId in acceptableCells:
		c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID = ?;''', (cellId,))
		w = sum([i[0] for i in c.fetchall()])
		if w>0:
			noDonuts += 1
	x = noDonuts/len(acceptableCells) if len(acceptableCells) != 0 else 0
	dictToDF['donutFrac'].append(x)

	#analysing circ
	# c.execute('''SELECT id FROM Cells WHERE acceptable;''')
	# acceptableCells = [i[0] for i in c.fetchall()]
	# dictToDF['n'].append(len(acceptableCells))
	# noDonuts = 0
	# for cellId in acceptableCells:
	# 	c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID = ?;''', (cellId,))
	# 	w = sum([i[0] for i in c.fetchall()])
	# 	if w>0:
	# 		noDonuts += 1
	# x = noDonuts/len(acceptableCells) if len(acceptableCells) != 0 else 0
	# dictToDF['donutFrac'].append(x)

	# c.close()
	# conn.close()

df = pd.DataFrame(data=dictToDF)
df.to_csv('{}/all.csv'.format(csvOutput))

for unique in uniqueCloneSet:
	uniqueDF = df.loc[df['clone'] == unique]
	uniqueDF.to_csv('{}/{}_old.csv'.format(csvOutput, unique))

for unique in uniqueDaySet:
	uniqueDF = df.loc[df['day'] == unique]
	uniqueDF.to_csv('{}/{}_old.csv'.format(csvOutput, unique))

# for unique in uniqueDaySet:
# 	uniqueDF = df.loc[df['circ'] == unique]
# 	unuqueDF.to_csv('{}/{}.csv'.format(csvOutput, unique))
