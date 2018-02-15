import numpy as np
import cv2
from matplotlib import pyplot as plt
# import sys
# print(sys.version)

#img = cv2.imread('water_coins.jpg')

img = cv2.imread('test_cells.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

for i in range(0,260,20):
	ret, thresh = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY)
	cv2.imwrite('threshTest/thresh_%s.jpg'%str(i),thresh)

# cv2.imwrite('grey1.jpg',gray)
# cv2.imwrite('grey2.jpg',255-gray)
# 
# # noise removal
# kernel = np.ones((3,3),np.uint8)
# opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
# 
# # sure background area
# sure_bg = cv2.dilate(opening,kernel,iterations=3)
# 
# # Finding sure foreground area
# dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
# ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
# 
# # Finding unknown region
# sure_fg = np.uint8(sure_fg)
# unknown = cv2.subtract(sure_bg,sure_fg)
# 
# cv2.imwrite('unknown.jpg', unknown)
# cv2.imwrite('DT.jpg', dist_transform)

print("\nDone")