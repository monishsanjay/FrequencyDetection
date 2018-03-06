import cv2
import numpy as np
bright=cv2.imread('frame175.jpg',1)
dark=cv2.imread('frame174.jpg',1)
darkHSV = cv2.cvtColor(dark, cv2.COLOR_BGR2HSV)
brightHSV = cv2.cvtColor(dark, cv2.COLOR_BGR2HSV)
brightYCB = cv2.cvtColor(bright, cv2.COLOR_BGR2YCrCb)
darkYCB = cv2.cvtColor(dark, cv2.COLOR_BGR2YCrCb)
brightLAB = cv2.cvtColor(bright, cv2.COLOR_BGR2LAB)
darkLAB = cv2.cvtColor(dark, cv2.COLOR_BGR2LAB)
brightYUV = cv2.cvtColor(bright, cv2.COLOR_BGR2YUV)
darkYUV = cv2.cvtColor(dark, cv2.COLOR_BGR2YUV)
#hist = cv2.calcHist([img],[0],None,[64],[0,256])
th2 = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
th3 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
th4 = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
th5 = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
cv2.imwrite('threshold.jpg',th2)
cv2.imwrite('threshold1.jpg',th3)
cv2.imwrite('threshold2.jpg',th4)
cv2.imwrite('threshold3.jpg',th5)
bgr = [64, 103, 254]
thresh = [24, 56, 4]
 
minBGR = np.array([bgr[0] - thresh[0], bgr[1] - thresh[1], bgr[2] - thresh[2]])
maxBGR = np.array([bgr[0] + thresh[0], bgr[1] + thresh[1], bgr[2] + thresh[2]])
 
maskBGR = cv2.inRange(bright,minBGR,maxBGR)
resultBGR = cv2.bitwise_and(bright, bright, mask = maskBGR)
 
#convert 1D array to 3D, then convert it to HSV and take the first element 
# this will be same as shown in the above figure [65, 229, 158]
hsv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2HSV)[0][0]
 
minHSV = np.array([hsv[0] - thresh[0], hsv[1] - thresh[1], hsv[2] - thresh[2]])
maxHSV = np.array([hsv[0] + thresh[0], hsv[1] + thresh[1], hsv[2] + thresh[2]])
 
maskHSV = cv2.inRange(brightHSV, minHSV, maxHSV)
resultHSV = cv2.bitwise_and(brightHSV, brightHSV, mask = maskHSV)
 
#convert 1D array to 3D, then convert it to YCrCb and take the first element 
ycb = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YCrCb)[0][0]
 
minYCB = np.array([ycb[0] - thresh[0], ycb[1] - thresh[1], ycb[2] - thresh[2]])
maxYCB = np.array([ycb[0] + thresh[0], ycb[1] + thresh[1], ycb[2] + thresh[2]])
 
maskYCB = cv2.inRange(brightYCB, minYCB, maxYCB)
resultYCB = cv2.bitwise_and(brightYCB, brightYCB, mask = maskYCB)
 
#convert 1D array to 3D, then convert it to LAB and take the first element 
lab = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2LAB)[0][0]
 
minLAB = np.array([lab[0] - thresh[0], lab[1] - thresh[1], lab[2] - thresh[2]])
maxLAB = np.array([lab[0] + thresh[0], lab[1] + thresh[1], lab[2] + thresh[2]])
 
maskLAB = cv2.inRange(brightLAB, minLAB, maxLAB)
resultLAB = cv2.bitwise_and(brightLAB, brightLAB, mask = maskLAB)
 
#convert 1D array to 3D, then convert it to LAB and take the first element 
yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]
 
minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])
maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])
 
maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)
resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)
cv2.imwrite("Result1 YUV.jpg", resultYUV)
cv2.imwrite("Result1 BGR.jpg", resultBGR)
cv2.imwrite("Result1 HSV.jpg", resultHSV)
cv2.imwrite("Result1 YCB.jpg", resultYCB)
cv2.imwrite("Output1 LAB.jpg", resultLAB)
#cv2.imshow('',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
