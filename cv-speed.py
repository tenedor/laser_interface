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

video_capture = cv2.VideoCapture(0)
video_capture.set(FRAME_WIDTH, 320) # frame width
video_capture.set(FRAME_HEIGHT, 240) # frame height

last_t = time.time()

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
threshmin = 220
while True:
  t0 = time.time()

  # Capture frame-by-frame
  ret, frame = video_capture.read()
  t1 = time.time()

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h,s,v = cv2.split(hsv)
  t2 = time.time()

  # Threshold the image for bright regions
  ret, thresh = cv2.threshold(v, threshmin, 255, cv2.THRESH_BINARY_INV)
  t3 = time.time()

  # Erode and dilate the thresholded image
  thresh = cv2.medianBlur(thresh, 5)
  t4 = time.time()

  # Detect blobs.
  keypoints = detector.detect(thresh)
  if len(keypoints):
    (x, y) = keypoints[0].pt
  else:
    (x, y) = (-1, -1)
  print "%.2f, %.2f" % (x, y)
  t5 = time.time()

  # Draw detected blobs as red circles.
  thresh = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  t6 = time.time()

  """
  cimg = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

  thresh = cimg

  # might be good to erode+dilate the thresh image here
  thresh = cv2.medianBlur(thresh, 5)
   
  # Detect blobs.
  keypoints = detector.detect(thresh)
   
  # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
  thresh = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  """

  cv2.imshow("video", thresh)
  t7 = time.time()

  key = cv2.waitKey(1)
  if key & 0xFF == ord('1'):
    threshmin = threshmin - 5
    print threshmin

  if key & 0xFF == ord('3'):
    cv2.imwrite('rec-img.jpg', thresh)
    time.sleep(1)

  if key & 0xFF == ord('2'):
    threshmin = threshmin + 5
    print threshmin

  if key & 0xFF == ord('q'):
    break

  t8 = time.time()

  print "%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f" % (t1-t0, t2-t1, t3-t2, t4-t3, t5-t4, t6-t5, t7-t6, t8-t7)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
