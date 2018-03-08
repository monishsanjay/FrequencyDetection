import cv2
import numpy as np
import math
import time
import os
Folder = 'folder'   
#os.mkdir(Folder)                                                                       # make a folder called "folder"
time_start = time.time()                                                                # to measure the total time taken to process
def frame_grab(x):                                                                      # function to get a particular frame
    while True:                                                                         # while video is open
        vidcap = cv2.VideoCapture(x)
        i=0
        while i<28:
            success,frame = vidcap.read()                                               # take a frame from the middle of the video
            i+=1   
        if success == False:                                                            # if no frame present, exit loop
            break
        print('Read a new frame on: ', success)                                         # display if frame has been read or not
        break          
    return frame
 
def find_area(frame, thresh, bgr1,lower,upper):                                         # function to return area of contour
    resultYUV, bgr= YUV_conv(frame, thresh, bgr1)                                       # function calls
    imgray = BGR_conv(resultYUV,lower,upper) 
    largest_area=area_calc(imgray)
    return largest_area, bgr

def split_frame(frame):                                                                 # function to split frames into BGR vlaues
    (B, G, R) = cv2.split(frame)                                                        # split frame into RGB values and find the max value
    B1 = np.amax(B)
    G1 = np.amax(G)
    R1 = np.amax(R)
    return [B1, G1, R1]

def YUV_conv(frame,thresh,bgr1):                                                        # function to convert frame to YUV format and threshold
    brightYUV = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)                                  # convert frame from BGR format to YUV format
    bgr = np.array([bgr1[0] - thresh[0], bgr1[1] - thresh[1], bgr1[2] - thresh[2]])     # to set bgr values of the LED
    yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]                    # convert RGB values of LED in ON state to YUV format
    minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])     # lower range of values for LED in ON state
    maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])     # upper range of values for LED in ON state
    maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)                                    # mask of upper and lower range of values
    resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)                   # perform AND operation to find the region with LED in ON state if present
    return resultYUV,bgr

def BGR_conv(resultYUV,lower,upper):                                                    # function to convert frame back to BGR format
    brightRGB = cv2.cvtColor(resultYUV, cv2.COLOR_YUV2BGR)                              # convert back to BGR format
    maskRGB = cv2.inRange(brightRGB, lower, upper)                                      # form a mask to check if frame has LED ON or not
    resultRGB = cv2.bitwise_and(brightRGB, brightRGB, mask = maskRGB)                   # perfrom AND operation to return TRUE or FALSE
    imgray = cv2.cvtColor(resultRGB,cv2.COLOR_BGR2GRAY)
    return imgray
def area_calc(imgray):                                                                  # function to find area of contour
    
    _,contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # find the contours of the bright spot in the image
    largest_area=0
    if len(contours)>0:                                                                 # if contours are present, do the following
        for cnt in contours:
            area=cv2.contourArea(cnt)
            largest_area=largest_area+area
    return largest_area
        
def threshold_find(bgr):                                                                # function to find the threshold value
    thresh = [abs(255-bgr[0]-3), abs(255-bgr[1]-3), abs(255-bgr[2]-3)]
    return thresh

def loop(thresh,bgr1,largest_area,lower,upper):                                         # main loop function
    count=0
    ledstate=0
    dtbt=0
    btdt=0
    tt=0
    vidcap = cv2.VideoCapture("ledhz.mp4")
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    for _ in range(0,30):
        tt = vidcap.get(cv2.CAP_PROP_POS_MSEC)
        success,frame3 = vidcap.read()                                                 
    
        if success == False:                                                            # if no frame present, exit loop
            break
        print('Read a new frame on: ', success)                                         # display if frame has been read or not
        cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),frame3)         # save the read frame
        count+=1
        area,bgr=find_area(frame3,thresh,bgr1,lower,upper)
        if area>largest_area:                                                           # to detect if led is ON or OFF                                                        
            if ledstate==0:
                continue
            dtbt+=1                                                                     # to count the number of dark to bright and bright to dark transitions
            ledstate=0
        else:
            if ledstate==1:
                continue
            btdt+=1                                                                     # to count the number of bright to dark transitions
            ledstate=1
        if count>30:                                                                    # performs opertation on 30 frames
            vidcap.release()
            cv2.destroyAllWindows()
            break
    return dtbt,btdt,tt,fps

if __name__ == '__main__':
    ledstate=0
    frame1=frame_grab("ledon.mp4")
    bgr1=split_frame(frame1)
    print "maximum pixel value=",bgr1
    thresh=threshold_find(bgr1)
    print "threshold=",thresh
    frame2=frame_grab("ledoff.mp4")
    bgr2=split_frame(frame2)
    print "minimum pixel value =",bgr2
    lower = np.array([bgr2[0]-20,bgr2[1]-20,bgr2[2]-20])
    upper = np.array([255,255,255])
    print "lower threshold =",lower
    print "upper threshold =",upper
    frame1=frame_grab("ledon.mp4")
    largest_area1, bgr=find_area(frame1, thresh, bgr1,lower,upper)
    print "bgr values to be set=",bgr
    print "largest area =",largest_area1
    print "80% of largest area=",0.8*largest_area1
    largest_area=largest_area1*0.8
    dtbt,btdt,tt,fps=loop(thresh,bgr1,largest_area,lower,upper)
    time_end = time.time()                                                                # measure total time taken to process
    print "Bright to dark transition: ",btdt
    print "Dark to bright tranisitions: ",dtbt               
    print "Time taken to process: ", time_end-time_start                                  # display time taken to process
    print "Frames per second: ", fps                                                      # display frames per second value
    print "Frequency: ", (btdt/tt*1000)                                                   # find frequency               
    
    
