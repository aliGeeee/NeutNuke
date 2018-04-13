import cv2
import numpy as np;



# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold=10
params.maxThreshold=170


# Filter by Area.
params.filterByArea = True
params.minArea = 10

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.75
params.maxCircularity = 1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0
    
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
# Read image
im = cv2.imread("blob5.png", cv2.IMREAD_GRAYSCALE)
thresh = im
#ret, thresh = cv2.threshold(im, 127, 254, cv2.THRESH_BINARY)
keypoints = detector.detect(thresh)
print(len(keypoints))
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(1000)
