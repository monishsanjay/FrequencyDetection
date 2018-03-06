import cv2
import time
import numpy as np
import os
Folder = 'folder'
#os.mkdir(Folder)
time_start = time.time()
vidcap = cv2.VideoCapture('video.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
success,image = vidcap.read()
count = 0
v=0
success = True
while success:
  hist = 0
  maxVal=0
  thresh = 0
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),image)     # save frame as JPEG file
  img = cv2.medianBlur(image,3)
  ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
  th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
  th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
  cv2.imwrite(os.path.join(Folder, "frametb{:d}.jpg".format(count)),th1)
  cv2.imwrite(os.path.join(Folder, "frameadm{:d}.jpg".format(count)),th2)
  cv2.imwrite(os.path.join(Folder, "frameadg{:d}.jpg".format(count)),th3)
  time_end = time.time()
print time_end-time_start
print fps
