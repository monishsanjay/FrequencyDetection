import cv2
import numpy as np
bright=cv2.imread('frame12.jpg',1)
dark=cv2.imread('frame11.jpg',1)
brightYUV = cv2.cvtColor(bright, cv2.COLOR_BGR2YUV)
darkYUV = cv2.cvtColor(dark, cv2.COLOR_BGR2YUV)
bgr = [40, 16, 255]
thresh = 40
 
#convert 1D array to 3D, then convert it to LAB and take the first element 
yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]
 
minYUV = np.array([yuv[0] - thresh, yuv[1] - thresh, yuv[2] - thresh])
maxYUV = np.array([yuv[0] + thresh, yuv[1] + thresh, yuv[2] + thresh])
 
maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)
resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)
cv2.imwrite("Result YUV.jpg", resultYUV)

cv2.waitKey(0)
cv2.destroyAllWindows()
