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
		return {'SE':None, 'confL':None, 'confR':None, 'p':None}
	SE = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
	conf = abs(sps.norm.ppf(sig/2))*SE
	p0 = (p1*n1+p2*n2)/(n1+n2)
	z = abs(p1-p2)/math.sqrt(p0*(1-p0)*(1/n1+1/n2))
	p = sps.norm.sf(z)*2
	return {'SE':SE, 'confL':p2-conf, 'confR':p2+conf, 'p':round(p, 4)}

daysCSV = [str(i*2)+'d.csv' for i in range(6)]

csvInDir = 'CSVfinal'
csvOutDir = 'Graphs'

for day in daysCSV:
	print(day)
	df = pd.read_csv(csvInDir+'/'+day, index_col='clone')
	df['SE'] = None
	df['confL'] = None
	df['confR'] = None
	df['p'] = None
	p1 = float(df['1']['UI']+df['2']['UI'])
	n1 = float(df['nNotDonut']['UI'])

	clones = [i for i in df.index if i != 'UI']
	for clone in clones:
		p2 = float(df['1'][clone]+df['2'][clone])
		n2 = float(df['nNotDonut'][clone])
		x = propTest(p1, n1, p2, n2, 0.01)
		for i in ['SE', 'confL', 'confR', 'p']:
			df[i][clone] = x[i]


