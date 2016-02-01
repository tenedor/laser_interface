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
  # Capture frame-by-frame
  ret, frame = video_capture.read()

  bgr = frame
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  b,g,r = cv2.split(bgr)
  h,s,v = cv2.split(hsv)

  ret, threshed = cv2.threshold(v, threshmin, 255, cv2.THRESH_BINARY_INV)

  cimg = cv2.cvtColor(threshed, cv2.COLOR_GRAY2BGR)

  # might be good to erode+dilate the threshed image here
  threshed = cv2.medianBlur(threshed, 5)

  """
  circles = cv2.HoughCircles(threshed, cv2.cv.CV_HOUGH_GRADIENT, 1, 20)
  if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
      cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
      cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
  """

  threshed = cimg

  #contours, hierarchy = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #print contours
  #threshed = cv2.drawContours(threshed, contours, 0, (0,255,0), 3)

  rows, columns, channels = frame.shape

  #print frame.shape

  """
  for r in range(rows/10):
    for c in range(columns):
      if frame.item(r,c,0) > 100:
        frame.itemset((r,c,0), 255)
        frame.itemset((r,c,1), 0)
        frame.itemset((r,c,2), 0)

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(30, 30),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE
      )

  # Draw a rectangle around the faces
  for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
  """

  """
  t = time.time()
  if False and t - last_t > 1:
    last_t = t

    gain = video_capture.get(GAIN)
    exposure = video_capture.get(EXPOSURE)
    print "g %f\ne %f\n" % (gain, exposure)
  """

  threshed = cv2.medianBlur(threshed, 5)
   
  # Detect blobs.
  keypoints = detector.detect(threshed)
   
  # Draw detected blobs as red circles.
  # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
  threshed = cv2.drawKeypoints(threshed, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  #print 'hi'
  #plt.show()
  #print 'bye'
  cv2.imshow("video", threshed)
  #cv2.imshow("video", image)
  #cv2.imshow("video", img)

  key = cv2.waitKey(1)
  if key & 0xFF == ord('1'):
    threshmin = threshmin - 5
    print threshmin

  if key & 0xFF == ord('3'):
    cv2.imwrite('rec-img.jpg', threshed)
    time.sleep(1)

  if key & 0xFF == ord('2'):
    threshmin = threshmin + 5
    print threshmin

  if key & 0xFF == ord('q'):
    break

titles = ['Video', 'b', 'g', 'r', 'h', 's', 'v', 'threshed']
images = [frame, b, g, r, h, s, v, v]

"""
for i in range(8):
  plt.subplot(2, 4, i + 1), plt.imshow(images[i], 'gray')
  plt.title(titles[i])
  plt.xticks([]), plt.yticks([])

plt.show()
cv2.waitKey(5000)
"""

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
