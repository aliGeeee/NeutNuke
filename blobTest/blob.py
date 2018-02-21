import cv2
import numpy as np

# Function for generating parameters
def modParams(thresh = (None,None),area = (None,None),circ = (None,None),conv = (None,None),iner = (None,None)):
	#initiate params
	params = cv2.SimpleBlobDetector_Params()

	#setting up filters
	params.filterByColor = False if thresh==(None,None) else True
	params.filterByArea = False if area==(None,None) else True
	params.filterByCircularity = False if circ==(None,None) else True
	params.filterByConvexity = False if conv==(None,None) else True
	params.filterByInertia = False if iner==(None,None) else True

	#setting min and max params
	(params.minThreshold, params.maxThreshold) = thresh
	(params.minArea, params.maxArea) = area
	(params.minCircularity, params.maxCircularity) = circ
	(params.minConvexity, params.maxConvexity) = conv
	(params.minInertiaRatio, params.maxInertiaRatio) = iner

	return params

# params = modParams(thresh=(10, 200),
# 				   area = (10,None),
# 				   circ = (0.5, 1),
# 				   conv = (0.2, None),
# 				   iner = (None, None))

params = modParams(thresh=(None, None),
				   area = (None, None),
				   circ = (None, None),
				   conv = (None, None),
				   iner = (None, None))

# Read image
im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)
for i in keypoints:
	print(i.pt, i.size)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.namedWindow('ImageWindowName', cv2.WINDOW_NORMAL)
cv2.imshow('ImageWindowName',im_with_keypoints)
cv2.waitKey(0)
