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

outputMain = '../output'
csvOutput = '../csvs'
try:
	os.mkdir(csvOutput)
except:
	pass

slides = sorted([i for i in os.listdir(outputMain) if '.DS_Store' not in i])


countDonuts = False
categoryRange = range(1,7)

dictToDF = {'slide':[], 'nNotDonut':[], 'nTot':[], 'donutFrac':[]}
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
	dictToDF['slide'].append(slide)
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
	dictToDF['nTot'].append(len(acceptableCells))
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