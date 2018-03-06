import cv2
import time
import numpy as np
import os
import math                                                                           # import all the necessary libraries
Folder = 'folder'   
#os.mkdir(Folder)                                                                     # make a folder called "folder"
time_start = time.time()                                                              # to measure the total time taken to process
vidcap = cv2.VideoCapture('15hz.mp4')                                                 # open video file called "....mp4"
fps = vidcap.get(cv2.CAP_PROP_FPS)                                                    # get the frames per second value
success,image = vidcap.read()                                                         # check if video file opened successfully
success = True                      
count=0                                                                               # counts the number of frames
dtbt=0                                                                                # counts the number of dark to bright transitions
btdt=0                                                                                # counts the numbers of bright to dark transitions
ledstate=0                                                                            # state of the led
lower = np.array([150,150,150])                                                       # mask for checking if frame has LED is ON or not
upper = np.array([255,255,255])
bgr = [251, 252, 253]                                                                 # BGR values of led in ON state
thresh = [4, 3, 2]
while success:
    success,frame = vidcap.read()                                                     # read a frame
    tt = vidcap.get(cv2.CAP_PROP_POS_MSEC)                                            # get time stamp of frame
    print tt                                                                          # display timestamp
    if success == False:                                                              # if no frame present, exit loop
          break
    print('Read a new frame: ', success)                                              # display if frame has been read or not
    cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),frame)            # save the read frame
    brightYUV = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)                                # convert frame from BGR format to YUV format
    yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]                  # convert RGB values of LED in ON state to YUV format
    minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])   # lower range of values for LED in ON state
    maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])   # upper range of values for LED in ON state
    maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)                                  # mask of upper and lower range of values
    resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)                 # perform AND operation to find the region with LED in ON state if present
    cv2.imwrite(os.path.join(Folder, "frameyuv{:d}.jpg".format(count)), resultYUV)    # save frame
    count+=1                                                                          # increase frame count
    brightRGB = cv2.cvtColor(resultYUV, cv2.COLOR_YUV2BGR)                            # convert back to BGR format
    maskRGB = cv2.inRange(brightRGB, lower, upper)                                    # form a mask to check if frame has LED ON or not
    resultRGB = cv2.bitwise_and(brightRGB, brightRGB, mask = maskRGB)                 # perfrom AND operation to return TRUE or FALSE
    if np.any(resultRGB) == 0:                                                        # to count the number of dark to bright and bright to dark transitions
        if ledstate==0:
            continue
        dtbt+=1
        ledstate=0
    else:
        if ledstate==1:
            continue
        btdt+=1
        ledstate=1
           
time_end = time.time()                                                                # measure total time taken to process
print "Bright to dark transition: ",btdt
print "Dark to bright tranisitions: ",dtbt                                            # display number of tranisitions
print "Time taken to process: ", time_end-time_start                                  # display time taken to process
print "Frames per second: ", fps                                                      # display frames per second value
print "Frequency: ", (btdt/tt*1000)                                                   # display frequency
