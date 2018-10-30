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

csvInDir = '../csvs'
csvOutDir = '../graphs'

try:
	os.mkdir(csvInDir)
except:
	pass

try:
	os.mkdir(csvOutDir)
except:
	pass


df = pd.read_csv(csvInDir+'/all.csv', index_col='slide')
# df['SE'] = 0
# df['conf'] = 0
# df['p'] = None
# # p1 = float(df['1']['UI']+df['2']['UI'])
# # n1 = float(df['nNotDonut']['UI'])

# df['conf'] = 0.0
# df['p'] = 0.0
# clones = [i for i in df.index if i != 'UI']
# # for clone in clones:
# # 	# p2 = float(df['1'][clone]+df['2'][clone])
# # 	# n2 = float(df['nNotDonut'][clone])
# # 	# x = propTest(p1, n1, p2, n2, 0.05)
# # 	for i in ['SE', 'conf']:
# # 		df.at[clone, i] = x[i]

#GENERATING LOW LOBED GRAPHS
plt.figure()
plt.title('Low-lobed cell fraction')
rawLabelList = sorted([i for i in df.index])
heightList = [(df['1'][i]+df['2'][i])*100 for i in rawLabelList]
labelList = [i for i in rawLabelList]
bars = plt.bar(x = labelList, height = heightList)

plt.xticks(rotation=45, ha='right')
plt.ylim((0,plt.ylim()[1]*1.2))

n=0
for rect in bars:
	plt.text(rect.get_x() + rect.get_width()/2, plt.ylim()[1], 'n\n{}'.format(df['nNotDonut'][rawLabelList[n]]), ha='center', va='top')
# 	if n > 0:
# 		plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
	n += 1

plt.xlabel('Slide')
plt.ylabel('% within non-annular cells')
#plt.axhline(y=(df['1']['UI']+df['2']['UI'])*100, linestyle = '--', color='r')
plt.tight_layout()
plt.savefig('{}/lowLobed.png'.format(csvOutDir))
plt.close()


#GENERATING HIGH LOBED GRAPHS
plt.figure()
plt.title('High-lobed cell fraction')
rawLabelList = sorted([i for i in df.index])
heightList = [(df['5'][i]+df['6'][i])*100 for i in rawLabelList]
labelList = [i for i in rawLabelList]
bars = plt.bar(x = labelList, height = heightList)

plt.xticks(rotation=45, ha='right')
plt.ylim((0,plt.ylim()[1]*1.2))

n = 0
for rect in bars:
	plt.text(rect.get_x() + rect.get_width()/2, plt.ylim()[1], 'n\n{}'.format(df['nNotDonut'][rawLabelList[n]]), ha='center', va='top')
# 	if n > 0:
# 		plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
	n += 1

plt.xlabel('Slide')
plt.ylabel('% within non-annular cells')
#plt.axhline(y=(df['1']['UI']+df['2']['UI'])*100, linestyle = '--', color='r')
plt.tight_layout()
plt.savefig('{}/highLobed.png'.format(csvOutDir))
plt.close()


#GENERATING ANNULAR GRAPHS
plt.figure()
plt.title('Low-lobed cell fraction')
rawLabelList = sorted([i for i in df.index])
heightList = [(df['donutFrac'][i])*100 for i in rawLabelList]
labelList = [i for i in rawLabelList]
bars = plt.bar(x = labelList, height = heightList)

plt.xticks(rotation=45, ha='right')
plt.ylim((0,plt.ylim()[1]*1.2))

n = 0
for rect in bars:
	plt.text(rect.get_x() + rect.get_width()/2, plt.ylim()[1], 'n\n{}'.format(df['nTot'][rawLabelList[n]]), ha='center', va='top')
# 	if n > 0:
# 		plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
	n += 1

plt.xlabel('Slide')
plt.ylabel('% annular cells')
#plt.axhline(y=(df['1']['UI']+df['2']['UI'])*100, linestyle = '--', color='r')
plt.tight_layout()
plt.savefig('{}/annular.png'.format(csvOutDir))
plt.close()









# df['SE'] = 0
# df['conf'] = 0
# df['p'] = None
# p1 = float(df['6']['UI'])
# n1 = float(df['nNotDonut']['UI'])
# df['conf'] = 0.0
# df['p'] = 0.0
# clones = [i for i in df.index if i != 'UI']
# for clone in clones:
# 	p2 = float(df['6'][clone])
# 	n2 = float(df['nNotDonut'][clone])
# 	x = propTest(p1, n1, p2, n2, 0.05)
# 	for i in ['SE', 'conf', 'p']:
# 		df.at[clone, i] = x[i]

# plt.figure()
# plt.title('Day {} highly-lobed cell fraction'.format(day[:-5]))
# rawLabelList = sorted([i for i in df.index if i != 'UI'])
# heightList = [(df['6'][i])*100 for i in rawLabelList]
# labelList = [i for i in rawLabelList]
# bars = plt.bar(x = labelList, height = heightList, color = 'g')
# n = 0
# for rect in bars:
# 	plt.text(rect.get_x() + rect.get_width()/2, 25, 'n\n{}'.format(df['nNotDonut'][rawLabelList[n]]), ha='center', va='top')
# 	if n > 0:
# 		plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
# 	n += 1
# plt.xticks(rotation=45, ha='right')
# plt.ylim((0,25))
# plt.yticks(np.arange(0,25,5))
# plt.xlabel('Clone')
# plt.ylabel('% within non-annular cells')
# #plt.axhline(y=(df['5']['UI']+df['6']['UI'])*100, linestyle = '--', color='r')
# plt.tight_layout()
# plt.savefig('{}/{}_multi.png'.format(csvOutDir, day[:-4]))
# plt.close()




# df['SE'] = 0
# df['conf'] = 0
# df['p'] = None
# p1 = float(df['donutFrac']['UI'])
# n1 = float(df['n']['UI'])
# df['conf'] = 0.0
# df['p'] = 0.0
# clones = [i for i in df.index if i != 'UI']
# for clone in clones:
# 	p2 = float(df['donutFrac'][clone])
# 	n2 = float(df['n'][clone])
# 	x = propTest(p1, n1, p2, n2, 0.05)
# 	for i in ['SE', 'conf', 'p']:
# 		df.at[clone, i] = x[i]

# plt.figure()
# plt.title('Day {} annular cell fraction'.format(day[:-5]))
# rawLabelList = sorted([i for i in df.index if i != 'UI'])
# heightList = [(df['donutFrac'][i])*100 for i in rawLabelList]
# labelList = [i for i in rawLabelList]
# bars = plt.bar(x = labelList, height = heightList, color = 'r')
# n = 0
# for rect in bars:
# 	plt.text(rect.get_x() + rect.get_width()/2, 50, 'n\n{}'.format(df['n'][rawLabelList[n]]), ha='center', va='top')
# 	if n > 0:
# 		plt.text(rect.get_x() + rect.get_width()/2, rect.get_height(), asterisks(df['p'][rawLabelList[n]]), ha='center', va='bottom')
# 	n += 1
# plt.xticks(rotation=45, ha='right')
# plt.ylim((0,50))
# plt.yticks(np.arange(0,55,5))
# plt.xlabel('Clone')
# plt.ylabel('% annular cells')
# #plt.axhline(y=df['donutFrac']['UI']*100, linestyle = '--', color='b')
# plt.tight_layout()
# plt.savefig('{}/{}_donut.png'.format(csvOutDir, day[:-4]))
# plt.close()
