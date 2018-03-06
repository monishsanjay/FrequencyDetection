import cv2
import numpy as np
import math
vidcap = cv2.VideoCapture("ledon.mp4")
success = True

while success:
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    #cv2.imshow('frame',frame)
    if success == False:                                                              # if no frame present, exit loop
          break
    print('Read a new frame on: ', success)                                              # display if frame has been read or not
    (B, G, R) = cv2.split(frame)
    B1 = np.amax(B)
    G1 = np.amax(G)
    R1 = np.amax(R)
    bgr1 = [B1,G1,R1]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        vidcap.release()
        break
    break          
B=0
G=0
R=0
vidcap = cv2.VideoCapture("ledoff.mp4")
success = True
while success:
    success,frame = vidcap.read()
    #cv2.imshow('frame',frame)
    if success == False:                                                              # if no frame present, exit loop
          break
    print('Read a new frame off: ', success)                                              # display if frame has been read or not
    (B, G, R) = cv2.split(frame)
    B2 = np.amax(B)
    G2 = np.amax(G)
    R2 = np.amax(R)
    bgr2 = [B2,G2,R2]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        vidcap.release()
        break
    break          
thresh = [abs(255-B1-3), abs(255-G1-3), abs(255-R1-3)]
lower = np.array([B2-20,G2-20,R2-20])
upper = np.array([255,255,255])
print "lower threshold =",lower
print "upper threshold =",upper                
print "maximum pixel value=",bgr1
print "minimum pixel value =",bgr2
print "threshold=",thresh
vidcap = cv2.VideoCapture("ledon.mp4")
success = True
while success:
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    success,frame = vidcap.read()
    #cv2.imshow('frame',frame)
    if success == False:                                                              # if no frame present, exit loop
          break
    print('Read a new frame area: ', success)
    brightYUV = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)                                # convert frame from BGR format to YUV format
    bgr = np.array([bgr1[0] - thresh[0], bgr1[1] - thresh[1], bgr1[2] - thresh[2]])
    yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]                  # convert RGB values of LED in ON state to YUV format
    minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])   # lower range of values for LED in ON state
    maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])   # upper range of values for LED in ON state
    maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)                                  # mask of upper and lower range of values
    resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)                 # perform AND operation to find the region with LED in ON state if present
    #cv2.imwrite(os.path.join(Folder, "frameyuv{:d}.jpg".format(count)), resultYUV)    # save frame
    #count+=1                                                                          # increase frame count
    brightRGB = cv2.cvtColor(resultYUV, cv2.COLOR_YUV2BGR)                            # convert back to BGR format
    maskRGB = cv2.inRange(brightRGB, lower, upper)                                    # form a mask to check if frame has LED ON or not
    resultRGB = cv2.bitwise_and(brightRGB, brightRGB, mask = maskRGB)                 # perfrom AND operation to return TRUE or FALSE
    imgray = cv2.cvtColor(resultRGB,cv2.COLOR_BGR2GRAY)
    largest_area=0
    _,contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  # find the contours of the bright spot in the image
    for cnt in contours:
        area=cv2.contourArea(cnt)
        #if (area>largest_area):
        largest_area=largest_area+area
    if cv2.waitKey(1) & 0xFF == ord('q'):
        vidcap.release()
    break        
print "bgr values to be set=",bgr
print "largest area =",largest_area
print "80% of largest area=",0.8*largest_area            
    
