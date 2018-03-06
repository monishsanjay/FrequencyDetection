import cv2
import time
import numpy as np
import os
Folder = 'folder'
#os.mkdir(Folder)
time_start = time.time()
vidcap = cv2.VideoCapture('3hz.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
success,image = vidcap.read()
success = True
count=0
i=0
dot=0
led=0
lower = np.array([150,150,150])
upper = np.array([255,255,255])


while success:
    success,bright = vidcap.read()
    tt = vidcap.get(cv2.CAP_PROP_POS_MSEC)
    print tt
    if success == False:
        
        break
    print('Read a new frame: ', success)
    cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),bright)     # save frame as JPEG file
    #image1=cv2.cvtColor(bright, cv2.COLOR_RGB2GRAY)
    #[minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(image1)
    #bright=cv2.imread('frame12.jpg',1)
    #dark=cv2.imread('frame11.jpg',1)
    #margin = 0.99
    brightYUV = cv2.cvtColor(bright, cv2.COLOR_BGR2YUV)
    #darkYUV = cv2.cvtColor(dark, cv2.COLOR_BGR2YUV)
    bgr = [251, 252, 253]
    
    #thresh1 = int(maxVal * margin)
    #print "Brightest pixel val is %d" %(maxVal)
    #print "Threshold is defined as %d" %(thresh1)
    
    thresh = [4, 3, 2]
 
    #convert 1D array to 3D, then convert it to LAB and take the first element 
    yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]
 
    minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])
    maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])
 
    maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)
    resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)
    cv2.imwrite(os.path.join(Folder, "frameyuv{:d}.jpg".format(count)), resultYUV)
    count+=1
    brightRGB = cv2.cvtColor(resultYUV, cv2.COLOR_YUV2BGR)
    #cv2.imwrite(os.path.join(Folder, "framergb{:d}.jpg".format(count)), brightRGB)
    mask = cv2.inRange(brightRGB, lower, upper)
    result = cv2.bitwise_and(brightRGB, brightRGB, mask = mask)
    if np.any(result) == 0:
        if led==0:
            continue
        i+=1
        led=0
    else:
        if led==1:
            continue
        dot+=1
        led=1
           
time_end = time.time()
print dot, i
print time_end-time_start
print fps
print dot/tt*1000
