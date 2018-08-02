import sys
import cv2
img = cv2.imread(sys.argv[1])
cv2.imshow(sys.argv[1], img)
import random
x = random.randrange(10)
print(x)
cv2.waitKey(10000)