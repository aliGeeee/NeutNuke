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
import neutFunctions as nfpics

outputMain = '../output2'
sumDir = 'pics'

batches = ['D0#1', 'D0#2', 'D2#1', 'D2#2', 'D4#1', 'D4#2', 'D6#1', 'D6#2', 'D8#1', 'D8#2', 'D10#1', 'D10#2', 'D12#1', 'D12#2', 'D14#1', 'D14#2']
categoryRange = range(1,6)
xDict = {i:[] for i in categoryRange}
nList = []

countDonuts = True

for outputDir in batches:
	outputDirDirs = os.listdir('{}/{}'.format(outputMain, outputDir))
	DBs = [i for i in outputDirDirs if i[-3:] == ".db"]
	DBno = max([int(i.replace('outputDB_','').replace('.db','')) for i in DBs])
	DBname = 'outputDB_%s.db'%str(DBno)
	conn = sqlite3.connect('{}/{}/{}'.format(outputMain, outputDir, DBname))
	c = conn.cursor()

	c.execute('''SELECT id FROM Cells WHERE acceptable AND lobes IS NOT NULL;''')
	acceptableCells = [i[0] for i in c.fetchall()]
	noDonutLobes = []
	for cellId in acceptableCells:
		if countDonuts:
			c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID = ?;''', (cellId,))
			w = sum([i[0] for i in c.fetchall()])
			if w == 0:
				c.execute('''SELECT lobes FROM Cells WHERE id=?;''', (cellId,))
				noDonutLobes.append(c.fetchone()[0])
		else:
			c.execute('''SELECT lobes FROM Cells WHERE id=?;''', (cellId,))
			noDonutLobes.append(c.fetchone()[0])
	
	nList.append(len(noDonutLobes))
	for i in categoryRange:
		if i < max(categoryRange):
			nlobes = [lobe for lobe in noDonutLobes if i <= lobe < i+1]
		else:
			nlobes = [lobe for lobe in noDonutLobes if i <= lobe]
		xDict[i].append(len(nlobes))

	c.close()
	conn.close()

#plotting replicates
ind = np.arange(len(batches))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence
plt.figure(figsize=(14,8))

barDict = {}
base = np.asarray([0 for i in batches]).astype(np.float64)
for i in categoryRange:
	normalised = np.asarray(xDict[i])/np.asarray(nList)
	barDict[i] = plt.bar(ind, normalised, width, bottom=base)
	base += normalised

xLabels = ['{}\nn={}'.format(batches[i], nList[i]) for i in range(len(batches))]

plt.xlabel('Dox treatment day')
plt.ylabel('Proportion')
plt.xticks(ind, xLabels)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend([barDict[i][0] for i in barDict] , [str(i) for i in barDict], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    ncol=len(barDict), mode="expand", borderaxespad=0.)

plt.savefig('{}/{}'.format(sumDir, 'lobeReplicatesDonut.png' if countDonuts else 'lobeReplicates.png'))
plt.close()


#plotting pools
batches = [batches[2*i][:-2] for i in range(int(len(batches)/2))]
nList = [nList[2*j]+nList[2*j+1] for j in range(len(batches))]
for i in xDict:
	xDict[i] = [xDict[i][2*j]+xDict[i][2*j+1] for j in range(len(batches))]

ind = np.arange(len(batches))    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence
plt.figure(figsize=(14,8))

barDict = {}
base = np.asarray([0 for i in batches]).astype(np.float64)
for i in categoryRange:
	normalised = np.asarray(xDict[i])/np.asarray(nList)
	print(i, normalised)
	barDict[i] = plt.bar(ind, normalised, width, bottom=base)
	base += normalised

xLabels = ['{}\nn={}'.format(batches[i], nList[i]) for i in range(len(batches))]

plt.xlabel('Dox treatment day')
plt.ylabel('Proportion')
plt.xticks(ind, xLabels)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.legend([barDict[i][0] for i in barDict] , [str(i) for i in barDict], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    ncol=len(barDict), mode="expand", borderaxespad=0.)

plt.savefig('{}/{}'.format(sumDir, 'lobePoolsDonut.png' if countDonuts else 'lobePools.png'))
plt.close()
