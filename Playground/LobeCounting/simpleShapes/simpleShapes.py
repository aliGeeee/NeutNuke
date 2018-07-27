import numpy as np
import scipy as sp
from scipy import signal
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os

circ = cv2.cvtColor(cv2.imread('circle.png'), cv2.COLOR_BGR2GRAY)
donut = cv2.cvtColor(cv2.imread('donut.png'), cv2.COLOR_BGR2GRAY)
eight = cv2.cvtColor(cv2.imread('donut2.png'), cv2.COLOR_BGR2GRAY)
nine = cv2.cvtColor(cv2.imread('donut3.png'), cv2.COLOR_BGR2GRAY)

ret, circCon, circH = cv2.findContours(circ, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
ret, donutCon, donutH = cv2.findContours(donut, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
ret, eightCon, eightH = cv2.findContours(eight, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
ret, nineCon, nineH = cv2.findContours(nine, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(circH, len(circCon))
print(donutH, len(donutCon))
print(eightH, len(eightCon))
print(nineH, len(nineCon))
#nucCon = sorted(nucConRaw, key=lambda x: -cv2.contourArea(x))

# #distance transforms
# distTrans = cv2.distanceTransform(nucThresh, cv2.DIST_L2, 3)
# distTrans *= 255/np.amax(distTrans)
# cv2.imwrite('output/%s/%sThresh.jpg'%(image[:-4], image[:-4]), nucThresh)
# cv2.imwrite('output/%s/%sDT.jpg'%(image[:-4], image[:-4]), distTrans)

# ret, DTThresh = cv2.threshold(distTrans, 150, 255, cv2.THRESH_BINARY)
# cv2.imwrite('output/%s/%sDTThresh.jpg'%(image[:-4], image[:-4]), DTThresh)
# cv2.imwrite('output/%s/%s.jpg'%(image[:-4], image[:-4]), img)

# noBackCellGrey.sort()

# #bimodality and laplacian calculations
# histArray = np.array(np.histogram(np.array(noBackCellGrey), bins=range(255)))
# smoothed = signal.savgol_filter(histArray[0], 25, 2)
# sk = sp.stats.skew(noBackCellGrey)
# ku = sp.stats.kurtosis(noBackCellGrey)
# bc = round((sk**2+1)/(ku+3), 3)

# dipTestResult = diptest.dip_test(np.array(noBackCellGrey))
# pValue = round(np.array(dipTestResult[1])[0], 3)


# greyLap = round(cv2.Laplacian(gray, cv2.CV_64F).var(),3)

# plt.hist(np.array(noBackCellGrey).astype(np.uint8).ravel(),256,[0,256])
# plt.axvline(x=retFG, color='g')
# plt.plot(histArray[1][:-1], smoothed, color='r')
# plt.title('BC = %s, p = %s, lap = %s'%(bc, pValue, greyLap))

# plt.savefig('output/%s/%sHist.jpg'%(image[:-4], image[:-4]))
# plt.close()

# print("Done")