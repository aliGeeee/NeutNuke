import copy
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import scipy as sp
from scipy import signal
import sqlite3
import sys
sys.path.append('..')

import neutFunctions as nfpics

# outputDir = sys.argv[1]
# outputDirDirs = os.listdir(sys.argv[1])

outputMain = '../output'
sumDir = 'pics'

cellDFDict = {}
nucDFDict = {}
attribDFDict = {}

nucLabels = {'circularity':'Circularity',
		'convexity':'Convexity',
		'netArea':'Nuclear area',
		'donutObjs':'Donuts',
		'rawArea':'Total Area'}

cellLabels = {'circ2':'Amended Circularity',
		'countdonuts':'Donut Objects'}

for attrib in list(nucLabels.keys())+list(cellLabels.keys()):
	attribDFDict[attrib] = pd.DataFrame(data=[], columns = ['batch', attrib])

batches = ['D0#1', 'D0#2', 'D2#1', 'D2#2', 'D4#1', 'D4#2', 'D6#1', 'D6#2', 'D8#1', 'D8#2', 'D10#1', 'D10#2', 'D12#1', 'D12#2', 'D14#1', 'D14#2']
donutNoList = []

# for outputDir in [i for i in os.listdir(outputMain) if '.DS_Store' not in i]:
for outputDir in batches:
	outputDirDirs = os.listdir('{}/{}'.format(outputMain, outputDir))
	DBs = [i for i in outputDirDirs if i[-3:] == ".db"]
	DBno = max([int(i.replace('outputDB_','').replace('.db','')) for i in DBs])
	DBname = 'outputDB_%s.db'%str(DBno)
	conn = sqlite3.connect('{}/{}/{}'.format(outputMain, outputDir, DBname))
	c = conn.cursor()

	cellDFDict[outputDir] = pd.read_sql_query('''SELECT * FROM Cells WHERE acceptable;''', conn)
	nucDFDict[outputDir] = pd.read_sql_query('''SELECT * FROM NuclearBlobs;''', conn)

	#nuclear plots
	for attrib in nucLabels.keys():
		x = [[outputDir, i] for i in nucDFDict[outputDir].loc[:, attrib]]
		y = pd.DataFrame(data=x, columns = ['batch', attrib])
		attribDFDict[attrib] = attribDFDict[attrib].append(y)

	#cell plots
	for attrib in cellLabels.keys():
		if attrib == 'countdonuts':
			x = []
			for index, cell in cellDFDict[outputDir].iterrows():
				c.execute('''SELECT donutObjs FROM NuclearBlobs WHERE cellID=?;''', (int(cell['id']),))
				w = sum([i[0] for i in c.fetchall()])
				v = w if w < 3 else 3
				x += [[outputDir, v]]
			totDonuts = len([i for i in x if i[1] > 0])
			donutNoList.append([totDonuts, len(x)])
		else:
			x = [[outputDir, i] for i in cellDFDict[outputDir].loc[:, attrib]]
		y = pd.DataFrame(data=x, columns = ['batch', attrib])
		attribDFDict[attrib] = attribDFDict[attrib].append(y)

	c.close()
	conn.close()

for attrib in nucLabels.keys():
	plt.figure(figsize=(20,12))
	sns.set(font_scale=1.8)
	pal = sns.color_palette()
	ax = sns.violinplot(x='batch', y=attrib, data=attribDFDict[attrib], palette=pal)
	ax.set(xlabel='Batch', ylabel=nucLabels[attrib])
	plt.savefig('{}/{}'.format(sumDir, attrib+'.png'))
	plt.close()

for attrib in cellLabels.keys():
	plt.figure(figsize=(20,12))
	sns.set(font_scale=1.8)
	pal = sns.color_palette()
	if attrib == 'colourdonuts':
		ax = sns.violinplot(x='batch', y=attrib, data=attribDFDict[attrib], palette=pal)
	else:
		ax = sns.violinplot(x='batch', y=attrib, data=attribDFDict[attrib], palette=pal)
	ax.set(xlabel='Batch', ylabel=cellLabels[attrib])
	plt.savefig('{}/{}'.format(sumDir, attrib+'.png'))
	plt.close()


ind = np.arange(len(batches))

plt.figure(figsize=(20,12))
plt.bar(ind, [i[0]/i[1] for i in donutNoList], 0.6)

plt.xlabel('Dox treatment day')
plt.ylabel('Donut proportion')
plt.xticks(ind, batches)
plt.yticks(np.arange(0, 0.6, 0.05))

plt.savefig('{}/{}'.format(sumDir, 'donutProp.png'))
plt.close()


ind = np.arange(int(len(batches)/2))
collectedDonutData = [(donutNoList[2*i][0]+donutNoList[2*i+1][0])/(donutNoList[2*i][1]+donutNoList[2*i+1][1]) 
				for i in range(int(len(batches)/2))]
labelsList = [batches[2*i][:-2] for i in range(int(len(batches)/2))]

plt.figure(figsize=(20,12))
plt.bar(ind, collectedDonutData, 0.6)

plt.xlabel('Dox treatment day')
plt.ylabel('Donut proportion')
plt.xticks(ind, labelsList)
plt.yticks(np.arange(0, 0.6, 0.05))

plt.savefig('{}/{}'.format(sumDir, 'donutProp2.png'))
plt.close()

# try:
# 	os.mkdir('{}/{}'.format(sumDir, outputDir.replace('./output/','')))
# except:
# 	pass

# sns.set_style("whitegrid")
# tips = sns.load_dataset("tips")
# print(tips)
# print(type(tips))
# ax = sns.swarmplot(x="day", y="total_bill", data=tips)
# ax = sns.boxplot(x="day", y="total_bill", data=tips,
#		 showcaps=False,boxprops={'facecolor':'None'},
#		 showfliers=False,whiskerprops={'linewidth':0})

