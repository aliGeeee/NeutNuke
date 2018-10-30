import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy as sp
from scipy import stats as sps
import math

def propTest(p1, n1, p2, n2, sig):
	if n1 == 0 or n2 == 0:
		return {'SE':0, 'conf':0, 'p':None}
	SE = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
	conf = abs(sps.norm.ppf(sig/2))*SE
	p0 = (p1*n1+p2*n2)/(n1+n2)
	z = abs(p1-p2)/math.sqrt(p0*(1-p0)*(1/n1+1/n2))
	p = sps.norm.sf(z)*2
	return {'SE':SE, 'conf':conf, 'p':round(p, 4)}

def asterisks(p):
	if p > 0.05:
		return 'ns'
	elif p >= 0.01:
		return '*'
	elif p >= 0.001:
		return '* *'
	else:
		return '* * *'


daysCSV = [str(i*2)+'d.csv' for i in range(6)]
nameDict = {'B2':'Prdm1 Cl 2',
	'B3':'Prdm1 Cl 3',
	'L2.5':'Lbr #2 Cl 5',
	'L2.8':'Lbr #2 Cl 8',
	'S2':'Spi1 Cl 2',
	'S3':'Spi1 Cl 3',
	'P2.3':'Pnpla6 #2 Cl 3',
	'P2.4':'Pnpla6 #2 Cl 4',
	'W1.1':'Wdr #1 Cl 1',
	'W1.4':'Wdr #1 Cl 4',
	'W2.6':'Wdr #2 Cl 6',
	'UI':'Uninfected'}

csvInDir = 'csvs'
csvOutDir = 'graphs'

for day in daysCSV:
	print(day)
	df = pd.read_csv(csvInDir+'/'+day, index_col='clone')
	df['SE'] = 0
	df['conf'] = 0
	df['p'] = None
	p1 = float(df['1']['UI']+df['2']['UI'])
	n1 = float(df['nNotDonut']['UI'])

	df['conf'] = 0.0
	df['p'] = 0.0
	clones = [i for i in df.index if i != 'UI']
	for clone in clones:
		p2 = float(df['1'][clone]+df['2'][clone])
		n2 = float(df['nNotDonut'][clone])
		x = propTest(p1, n1, p2, n2, 0.05)
		for i in ['SE', 'conf', 'p']:
			df.at[clone, i] = x[i]

	plt.figure()
	plt.title('Day {} low-lobed cell fraction'.format(day[:-5]))
	rawLabelList = sorted([i for i in df.index if i != 'UI'])
	heightList = [(df['1'][i]+df['2'][i])*100 for i in rawLabelList]
	labelList = [i for i in rawLabelList]
	bars = plt.bar(x = labelList, height = heightList)
	n = 0
	for rect in bars:
		plt.text(rect.get_x() + rect.get_width()/2, 110, 'n\n{}'.format(df['nNotDonut'][rawLabelList[n]]), ha='center', va='top')
		if n > 0:
			plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
		n += 1
	plt.xticks(rotation=45, ha='right')
	plt.ylim((0,110))
	plt.yticks(np.arange(0,110,20))

	plt.xlabel('Clone')
	plt.ylabel('% within non-annular cells')
	#plt.axhline(y=(df['1']['UI']+df['2']['UI'])*100, linestyle = '--', color='r')
	plt.tight_layout()
	plt.savefig('{}/{}_uni.png'.format(csvOutDir, day[:-4]))
	plt.close()





	df['SE'] = 0
	df['conf'] = 0
	df['p'] = None
	p1 = float(df['6']['UI'])
	n1 = float(df['nNotDonut']['UI'])
	df['conf'] = 0.0
	df['p'] = 0.0
	clones = [i for i in df.index if i != 'UI']
	for clone in clones:
		p2 = float(df['6'][clone])
		n2 = float(df['nNotDonut'][clone])
		x = propTest(p1, n1, p2, n2, 0.05)
		for i in ['SE', 'conf', 'p']:
			df.at[clone, i] = x[i]

	plt.figure()
	plt.title('Day {} highly-lobed cell fraction'.format(day[:-5]))
	rawLabelList = sorted([i for i in df.index if i != 'UI'])
	heightList = [(df['6'][i])*100 for i in rawLabelList]
	labelList = [i for i in rawLabelList]
	bars = plt.bar(x = labelList, height = heightList, color = 'g')
	n = 0
	for rect in bars:
		plt.text(rect.get_x() + rect.get_width()/2, 25, 'n\n{}'.format(df['nNotDonut'][rawLabelList[n]]), ha='center', va='top')
		if n > 0:
			plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
		n += 1
	plt.xticks(rotation=45, ha='right')
	plt.ylim((0,25))
	plt.yticks(np.arange(0,25,5))
	plt.xlabel('Clone')
	plt.ylabel('% within non-annular cells')
	#plt.axhline(y=(df['5']['UI']+df['6']['UI'])*100, linestyle = '--', color='r')
	plt.tight_layout()
	plt.savefig('{}/{}_multi.png'.format(csvOutDir, day[:-4]))
	plt.close()




	df['SE'] = 0
	df['conf'] = 0
	df['p'] = None
	p1 = float(df['donutFrac']['UI'])
	n1 = float(df['n']['UI'])
	df['conf'] = 0.0
	df['p'] = 0.0
	clones = [i for i in df.index if i != 'UI']
	for clone in clones:
		p2 = float(df['donutFrac'][clone])
		n2 = float(df['n'][clone])
		x = propTest(p1, n1, p2, n2, 0.05)
		for i in ['SE', 'conf', 'p']:
			df.at[clone, i] = x[i]

	plt.figure()
	plt.title('Day {} annular cell fraction'.format(day[:-5]))
	rawLabelList = sorted([i for i in df.index if i != 'UI'])
	heightList = [(df['donutFrac'][i])*100 for i in rawLabelList]
	labelList = [i for i in rawLabelList]
	bars = plt.bar(x = labelList, height = heightList, color = 'r')
	n = 0
	for rect in bars:
		plt.text(rect.get_x() + rect.get_width()/2, 50, 'n\n{}'.format(df['n'][rawLabelList[n]]), ha='center', va='top')
		if n > 0:
			plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
		n += 1
	plt.xticks(rotation=45, ha='right')
	plt.ylim((0,50))
	plt.yticks(np.arange(0,55,5))
	plt.xlabel('Clone')
	plt.ylabel('% annular cells')
	#plt.axhline(y=df['donutFrac']['UI']*100, linestyle = '--', color='b')
	plt.tight_layout()
	plt.savefig('{}/{}_donut.png'.format(csvOutDir, day[:-4]))
	plt.close()
