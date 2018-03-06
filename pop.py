import cv2
import time
import numpy as np
import os
import sys
Folder = 'folder'
#os.mkdir(Folder)
def to_gray(img):
    """
    Converts the input in grey levels
    Returns a one channel image
    """
    #grey_img = np.zeros(((1920,1080,1),np.uint8))
    grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY )
    
    return grey_img   
    
def grey_histogram(img, nBins=64):
    """
    Returns a one dimension histogram for the given image
    The image is expected to have one channel, 8 bits depth
    nBins can be defined between 1 and 255 
    """
    hist_size = [nBins]
    h_ranges = [0, 255]
    hist = cv2.CreateHist(hist_size , cv2.CV_HIST_ARRAY, [[0, 255]], 1)
    cv2.CalcHist([img], hist)

    return hist

def extract_bright(grey_img, histogram=False):
    """
    Extracts brightest part of the image.
    Expected to be the LEDs (provided that there is a dark background)
    Returns a Thresholded image
    histgram defines if we use the hist calculation to find the best margin
    """
    ## Searches for image maximum (brightest pixel)
    # We expect the LEDs to be brighter than the rest of the image
    [minVal, maxVal, minLoc, maxLoc] = cv2.minMaxLoc(grey_img)
    print "Brightest pixel val is %d" %(maxVal)
    
    #We retrieve only the brightest part of the image
    # Here is use a fixed margin (80%), but you can use hist to enhance this one    
    if 0:
        ## Histogram may be used to wisely define the margin
        # We expect a huge spike corresponding to the mean of the background
        # and another smaller spike of bright values (the LEDs)
        hist = grey_histogram(img, nBins=64)
        [hminValue, hmaxValue, hminIdx, hmaxIdx] = cv2.GetMinMaxHistValue(hist) 
        margin = 0# statistics to be calculated using hist data    
    else:  
        margin = 0.8
        
    thresh = int( maxVal * margin) # in pix value to be extracted
    print "Threshold is defined as %d" %(thresh)

    #thresh_img = np.zeros((1920,1080,3),np.uint8)
    ret,thresh_img = cv2.threshold(grey_img, thresh, 255, cv2.THRESH_BINARY)
    
    return thresh_img

def find_leds(thresh_img):
    """
    Given a binary image showing the brightest pixels in an image, 
    returns a result image, displaying found leds in a rectangle
    """
    _,contours,_ = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE )
                            

    regions = []
    while contours:
        pts = [ pt for pt in contours ]
        x, y = zip(pts)    
        min_x, min_y = min(x), min(y)
        width, height = max(x) - min_x + 1, max(y) - min_y + 1
        regions.append((min_x, min_y, width, height))
        out_img = np.zeros((1920,1080,3),np.uint8)
    for x,y,width,height in regions:
        pt1 = x,y
        pt2 = x+width,y+height
        color = (0,255,0)
        cv2.rectangle( out_img, pt1, pt2, color, 2)

    return  out_img, regions
'''
def leds_positions(regions):
    """
    Function using the regions in input to calculate the position of found leds
    """
    centers = []
    for x, y, width, height in regions:
        centers.append( [x+ (width / 2),y + (height / 2)])

    return centers
'''
time_start = time.time()
vidcap = cv2.VideoCapture('video.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  grey_img = to_gray(image)
  # Detect brightest point in image :
  thresh_img = extract_bright(grey_img)
  # We want to extract the elements left, and count their number
  led_img,regions = find_leds(thresh_img)
  #centers = leds_positions(regions)
  cv2.imwrite(os.path.join(Folder, "frame{:d}.jpg".format(count)),led_img)     # save frame as JPEG file
  count += 1

time_end = time.time()
print time_end-time_start
print fps
