import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy

df = pd.read_csv('output/imageStats.csv', index_col='Unnamed: 0')

doxDFRaw = df.loc[df['Image File'].str.contains('dox')]
doxDF = doxDFRaw.loc[doxDFRaw['No. Valid Cells'] != 1]
untDFRaw = df.loc[df['Image File'].str.contains('unt')]
untDF = untDFRaw.loc[untDFRaw['No. Valid Cells'] != 1]

quant = 'n'

plt.figure(figsize = (10,6))
plt.title('Nuclear fragments per cell')
plt.xlabel('Image No.')
plt.ylabel('Mean nuclear fragments per cell')
plt.ylim([1.0, 2.5])
plt.yticks(np.arange(1.0, 2.6, 0.5))
plt.axhline(y=0.45, linestyle = '--')

xListUnt = ["n=%s"%i for i in untDF["No. Valid Cells"].values.astype('int')]
for i in range(len(xListUnt)):
	xListUnt[i] = "%s\n%s"%(i+1, xListUnt[i])
yListUnt = untDF['%s Mean'%quant].values.astype('float')
#yErrUnt = untDF['%s SD'%quant].values.astype('float')

plt.scatter(xListUnt, yListUnt, color = 'blue', marker = 's', label = 'Untreated')
#plt.errorbar(xListUnt, yListUnt, yerr = yErrUnt, color = 'blue', linestyle = "None")

xListDox = ["n=%s"%i for i in doxDF["No. Valid Cells"].values.astype('int')]
for i in range(len(xListDox)):
	xListDox[i] = "%s\n%s"%(i+1+len(xListUnt),xListDox[i])
yListDox = doxDF['%s Mean'%quant].values.astype('float')
#yErrDox = doxDF['%s SD'%quant].values.astype('float')

plt.scatter(xListDox, yListDox, color = 'red', marker = 'o', label = 'Dox')
#plt.errorbar(xListDox, yListDox, yerr = yErrDox, color = 'red', linestyle = "None")

plt.legend(loc='upper left')
plt.savefig('testStatScatter.jpg')
plt.close()

print("Done")