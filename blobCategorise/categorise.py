import cv2
import numpy as np

# Function for generating parameters
def modParams(paramDict):
	area = paramDict['area'] if 'area' in paramDict else (None,None)
	circ = paramDict['circ'] if 'circ' in paramDict else (None,None)
	conv = paramDict['conv'] if 'conv' in paramDict else (None,None)
	iner = paramDict['iner'] if 'iner' in paramDict else (None,None)

	params = cv2.SimpleBlobDetector_Params()

	#setting up filters
	params.filterByArea = False if area==(None,None) else True
	params.filterByCircularity = False if circ==(None,None) else True
	params.filterByConvexity = False if conv==(None,None) else True
	params.filterByInertia = False if iner==(None,None) else True

	#setting min and max params
	(params.minThreshold, params.maxThreshold) = (127,255)
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
def findParams(param, reso):
	lower = []
	higher = []
	for i in range(reso + 1):
		params = modParams({param:(i/reso, 10e+6)})
		detector = cv2.SimpleBlobDetector_create(params)
		keypoints = detector.detect(thresh)
		if len(keypoints) < 1:
			higher.append(i)
		elif len(keypoints) > 1:
			print("Error: Too many blobs detected in %s test."%param)
			break
		else:
			lower.append(i)
	
	if len(lower)==0:
		print("%s = 0"%param)
	elif len(higher)==0:
		print("%s = 1"%param)
	else:
		if max(lower) + 1 == min(higher):
			x = min(higher)/reso
			print("%s = %s (success)" % (param,x))
		else:
			print("Error: no smooth transition detected in %s test"%param)


# Read image and threshold
img = cv2.imread("blob.png", cv2.IMREAD_GRAYSCALE)
ret, thresh = cv2.threshold(img, 127, 254, cv2.THRESH_BINARY_INV)

# Check for existence of blobs
params = modParams({})
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(thresh)
if len(keypoints) < 1:
	print("No blobs detected")
elif len(keypoints) > 1:
	print("Too many blobs detected")
else:
	print(keypoints[0].pt)

# Find circ
for param in ['area', 'circ', 'conv', 'iner']:
	findParams(param, 100)


# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.namedWindow('ImageWindowName', cv2.WINDOW_NORMAL)
cv2.imshow('ImageWindowName',im_with_keypoints)
cv2.waitKey(0)
