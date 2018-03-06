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
  image1=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
  cv2.imwrite(os.path.join(Folder, "frameg{:d}.jpg".format(count)),image1)
  #hist = cv2.calcHist([image1],[0],None,[255],[0,256])
  [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(image1)
  print "Brightest pixel val is %d" %(maxVal)

  if 0:
    ## Histogram may be used to wisely define the margin
    # We expect a huge spike corresponding to the mean of the background
    # and another smaller spike of bright values (the LEDs)
    hist = cv2.calcHist([image1],[0],None,[64],[0,256])
    [hminValue, hmaxValue, hminIdx, hmaxIdx] = cv2.getMinMaxHistValue(hist) 
    margin = 0# statistics to be calculated using hist data    
  else:
    margin = 0.71
  thresh = int(maxVal * margin)
  print "Threshold is defined as %d" %(thresh)
  _,thresh1=cv2.threshold(image1,thresh,255,cv2.THRESH_BINARY)
  cv2.imwrite(os.path.join(Folder, "framet{:d}.jpg".format(count)),thresh1)
  count+=1
time_end = time.time()
print time_end-time_start
print fps
