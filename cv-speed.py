import cv2
import sys
import time
import numpy as np
from matplotlib import pyplot as plt

#cascPath = sys.argv[1]
#faceCascade = cv2.CascadeClassifier(cascPath)

FRAME_WIDTH = 3
FRAME_HEIGHT = 4
BRIGHTNESS = 10
CONTRAST = 11
SATURATION = 12
HUE = 13
GAIN = 14
EXPOSURE = 15
BUFFERSIZE = 21

camera = cv2.VideoCapture(0)
camera.set(FRAME_WIDTH, 320) # frame width
camera.set(FRAME_HEIGHT, 240) # frame height

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
threshmin = 220
while True:
  # Capture next frame; read twice to keep buffer empty, reducing latency
  _, _ = camera.read()
  ret, frame = camera.read()

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h,s,v = cv2.split(hsv)

  # Threshold the image for bright regions
  ret, thresh = cv2.threshold(v, threshmin, 255, cv2.THRESH_BINARY_INV)

  # Erode and dilate the thresholded image
  thresh = cv2.medianBlur(thresh, 5)

  # Detect blobs.
  keypoints = detector.detect(thresh)
  if len(keypoints):
    (x, y) = keypoints[0].pt
  else:
    (x, y) = (-1, -1)
  print "%.2f, %.2f" % (x, y)

  # Draw detected blobs as red circles.
  thresh = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  cv2.imshow("video", thresh)
  cv2.imshow("v", v)

  key = cv2.waitKey(1)

  if key & 0xFF == ord('1'):
    threshmin = threshmin - 5
    print threshmin

  if key & 0xFF == ord('2'):
    threshmin = threshmin + 5
    print threshmin

  if key & 0xFF == ord('3'):
    cv2.imwrite('rec-img.jpg', thresh)
    time.sleep(1)

  if key & 0xFF == ord('q'):
    break

# When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()
