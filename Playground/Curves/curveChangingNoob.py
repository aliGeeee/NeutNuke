import numpy as np
import scipy as sp
import cv2
import os
import multiprocessing as mp
from matplotlib import pyplot as plt
import time

start_time = time.time()

mainInputDir = 'cells/'
mainOutputDir = 'output/'
bimodalData = []

def curve(npArray, a):
	if a == 0:
		return npArray
	else:
		theta = a * np.pi/4
		r = 255/np.sqrt(2)/np.sin(theta)
		y = np.sqrt(r**2 - (npArray - r*np.cos(np.pi/4-theta))**2) - r*np.sin(np.pi/4-theta)
		return y.astype(np.uint8)
try:
	inDir = os.listdir(mainInputDir)
	inDir.sort()
except:
	print("Sad.")
	quit()
	

#importing image and making grayscale
for image in inDir:
	if image == ".DS_Store" or image == "._.DS_Store":
		continue
	try:
		os.mkdir('%s/%s'%(mainOutputDir, image[:-4]))
	except:
		pass

	print("Analysing nuclei %s..."%(image))

	try:
		img = cv2.imread('%s/%s'%(mainInputDir, image))
		img = img[100:img.shape[0]-100, 100:img.shape[1]-100]
	except:
		print("%s isn't an image file!"%image)
		continue

	for i in (0, 0.2, 0.4, 0.6, 0.8, 1):
		curvedImg = curve(img, i)

		curvedGrey = cv2.cvtColor(curvedImg, cv2.COLOR_BGR2GRAY)

		noWhite = []
		for j in curvedGrey.tolist():
			for k in j:
				if k < 240:
					noWhite.append(k)

		plt.hist(np.array(noWhite).astype(np.uint8).ravel(),256,[0,256])
		plt.savefig('%s/%s/%s%sHist.jpg'%(mainOutputDir, image[:-4], image[:-4], i))
		plt.close()

		cv2.imwrite('%s/%s/%s%s.jpg'%(mainOutputDir, image[:-4], image[:-4], i), curvedImg)

	print("Done anaylysing nuclei %s\n"%image)
	#return None

print("Done within %s seconds"%str(time.time()-start_time))