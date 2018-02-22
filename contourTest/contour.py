import numpy as np
import cv2

for i in range(10):
	img = cv2.imread('binaryBlob.png')
	imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(imgGrey, 127, 255, 0)
	img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.drawContours(img, contours, i, (0,255,0), 3)
	cv2.imwrite("LMAO_%s.png"%str(i), img)
cv2.waitKey(10000)