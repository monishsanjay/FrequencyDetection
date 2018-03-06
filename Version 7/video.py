import numpy as np
import cv2
import time
import os
Folder = 'folder1'
#os.mkdir(Folder)
time_start = time.time()
vidcap = cv2.VideoCapture(0)
fps = vidcap.get(cv2.CAP_PROP_FPS)
success,image = vidcap.read()
success = True
count=0
while success:
    success,bright = vidcap.read()
    if success == False:
        break
    print('Read a new frame: ', success)
    cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),bright)     # save frame as JPEG file
    brightYUV = cv2.cvtColor(bright, cv2.COLOR_BGR2YUV)
    bgr = [251, 252, 253]
         
    thresh = [4, 3, 2]
 
    #convert 1D array to 3D, then convert it to LAB and take the first element 
    yuv = cv2.cvtColor( np.uint8([[bgr]] ), cv2.COLOR_BGR2YUV)[0][0]
 
    minYUV = np.array([yuv[0] - thresh[0], yuv[1] - thresh[1], yuv[2] - thresh[2]])
    maxYUV = np.array([yuv[0] + thresh[0], yuv[1] + thresh[1], yuv[2] + thresh[2]])
 
    maskYUV = cv2.inRange(brightYUV, minYUV, maxYUV)
    resultYUV = cv2.bitwise_and(brightYUV, brightYUV, mask = maskYUV)
    cv2.imwrite(os.path.join(Folder, "frameyuv{:d}.jpg".format(count)), resultYUV)
    count+=1

    # Display the resulting frame
    cv2.imshow('frame',bright)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
time_end = time.time()
print time_end-time_start
print fps
# When everything done, release the capture
vidcap.release()
cv2.destroyAllWindows()
