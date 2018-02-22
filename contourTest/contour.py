import numpy as np
import cv2

#loading images and finding contours
img = cv2.imread('binaryBlob.png')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgGrey, 127, 255, 0)
img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#iterate through contours and isolate
for i in range(len(contours)):
	rawMask = np.zeros((img.shape[0], img.shape[1], 1), dtype = "uint8")
	cv2.drawContours(rawMask, contours, i, (255), -1)
	#cv2.imwrite("Masks_%s.png"%str(i), rawMask)

	x, y, width, height = cv2.boundingRect(contours[i])

	margin = 20
	rawROI = np.zeros((height+2*margin, width+2*margin, 1), dtype = "uint8")
	rawROI[margin:margin+height, margin:margin+width] = rawMask[y:y+height, x:x+width]

	circ = round(4*np.pi*cv2.contourArea(contours[i])/(cv2.arcLength(contours[i],True)**2),3)
	cv2.putText(rawROI, "Circ. = %s"%circ, (int(0.1*margin),height+int(1.9*margin)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255))


	cv2.imwrite("ROI_%s.png"%str(i), rawROI)
print("Done")