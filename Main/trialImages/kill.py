import cv2
import numpy as np

img = cv2.imread("D0#2.tif")
print("done")
img2 = img[int(img.shape[0]/2):int(img.shape[0]/2)+1000, int(img.shape[1]/2):int(img.shape[1]/2)+1000]
print("super done")
cv2.imshow("Lmao.tif", img2)
cv2.imwrite("Lmao.tif", img2)
cv2.waitKey(20000)