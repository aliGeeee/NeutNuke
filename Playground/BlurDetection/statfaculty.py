import numpy as np
import scipy as sp
from scipy import signal
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os
import copy
from progress.bar import Bar
from rpy2 import robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri

diptest = importr('diptest')
numpy2ri.activate()

# #statfaculty = list(map(int, "1001011205411322223121252002013441001000102"))
# statfaculty = list(map(int, "0111111111111111111111111111111111111111111112344444444444444444444444444444444444444444444444444445"))
# #statfaculty = list(map(int, "01233333333333333333333333333333333333333333333333333333333345"))
# statfaculty.sort()
# print(len(statfaculty))

# print(round(dip.dip(statfaculty)[0], 8))

# print(diptest.diptest(numpy.array(statfaculty), min_is_0=True))

# plt.hist(statfaculty)#setting manual values
# plt.show()

distList =[list(map(int, "0"*5+"1"*40+"2"*5+"3"*5+"4"*40+"5"*5)),# very bimodal
			list(map(int, "0"*10+"1"*30+"2"*10+"3"*10+"4"*30+"5"*10)),# a bit bimodal
			list(map(int, "0"*10+"1"*10+"2"*10+"3"*50+"4"*10+"5"*10)),# very unimodal
			list(map(int, "0"*17+"1"*17+"2"*17+"3"*17+"4"*17+"5"*17)),]# uniform

statfaculty = distList[2]

histArray = np.array(np.histogram(np.array(statfaculty), bins=range(min(statfaculty), max(statfaculty)+2)))
sk = sp.stats.skew(statfaculty)
ku = sp.stats.kurtosis(statfaculty)
bc=str((sk**2+1)/(ku+3))

#print(diptest.dip_test(np.array(histArray[0])))
dipTestResult = diptest.dip_test(np.array(statfaculty))

print("p-value: %s"%np.array(dipTestResult[1])[0])

plt.hist(np.array(statfaculty).astype(np.uint8).ravel(),256,[0,256])
plt.plot(histArray[1][:-1], histArray[0], color='r')
plt.title('BC = %s'%bc)
print(bc)
plt.close()

print("Done")