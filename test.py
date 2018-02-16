import numpy as np
import cv2
from matplotlib import pyplot as plt
# import sys
# print(sys.version)

#img = cv2.imread('water_coins.jpg')

img = cv2.imread('test_cells.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('wholeTest/thresh_100.jpg', thresh)

# noise removal
kernel = np.ones((1,1), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
cv2.imwrite('wholeTest/noNoise_100.jpg', opening)


sure_bg = cv2.dilate(opening, kernel, iterations=3)
cv2.imwrite('wholeTest/bg.jpg', sure_bg)

#Finding sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)*100
# dist_transform = opening
ret, sure_fg = cv2.threshold(dist_transform,0.2*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
# 
cv2.imwrite('wholeTest/fg.jpg', sure_fg)
cv2.imwrite('wholeTest/unknown.jpg', unknown)
cv2.imwrite('wholeTest/DT.jpg', dist_transform)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
img[markers == -1] = [0,0,255]

markers2 = cv2.applyColorMap(255-gray, cv2.COLORMAP_JET)

cv2.imwrite('wholeTest/markers.jpg',markers)
cv2.imwrite('wholeTest/markersC.jpg',markers2)
cv2.imwrite('wholeTest/imggg.jpg',img)

print("\nDone")