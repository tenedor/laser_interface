#import serial
import time
import random
import sys
import cv2
import numpy as np
import Tkinter as Tk
import Image, ImageTk


events = {
    "mousedown": "<Button-1>",
    "mouseup": "<ButtonRelease-1>",
    "mousedrag": "<B1-Motion>",
    "mousemove": "<Motion>",
    "keypress": "<Key>",
}

keys = {
    "ESC": "\x1b",
    "DEL": "\x7f",
    "ENTER": "\r",
}


class Laser_Toggle_App:

    def __init__(self, master, ser):
        self.master_frame = master
        self.serial = ser

        FRAME_WIDTH = 3
        FRAME_HEIGHT = 4

        # video camera
        self.camera = cv2.VideoCapture(0)
        self.camera.set(FRAME_WIDTH, 320)
        self.camera.set(FRAME_HEIGHT, 240)

        # blob detector, detection threshold
        self.detector = cv2.SimpleBlobDetector()
        self.brightness_threshold = 220

        master.bind_all(events["keypress"], self.on_keypress_global)

        canvas = self.canvas = Tk.Canvas(master, width=400, height=100,
                background='white')

        self.button_rects = []
        self.button_rects.append(canvas.create_rectangle(20, 20, 80, 80,
                fill='gray'))
        self.button_rects.append(canvas.create_rectangle(120, 20, 180, 80,
                fill='gray'))
        self.button_rects.append(canvas.create_rectangle(220, 20, 280, 80,
                fill='gray'))

        self.laser_rect = canvas.create_rectangle(320, 20, 380, 80, fill='gray')

        canvas.pack()

        #self.read_serial_every_n_milliseconds(100)
        self.read_position_every_n_milliseconds(30)

    def on_keypress_global(self, e):
        c = e.char
        if c == 'q':
            self.camera.release()
            cv2.destroyAllWindows()
            self.master_frame.quit()

    def read_serial_every_n_milliseconds(self, ms):
        while self.serial.inWaiting() > 0:
            message = ord(self.serial.read())
            laser_on = bool(message & 1 << 3)
            button_states = message & 7

            if laser_on:
                self.canvas.itemconfigure(self.laser_rect, fill="red")
            else:
                self.canvas.itemconfigure(self.laser_rect, fill="gray")

            for i in range(3):
                if button_states & 1 << i:
                    self.canvas.itemconfigure(self.button_rects[i], fill="blue")
                else:
                    self.canvas.itemconfigure(self.button_rects[i], fill="gray")
        self.master_frame.after(ms, self.read_serial_every_n_milliseconds, ms)

    def read_position_every_n_milliseconds(self, ms):
        # capture next frame; read twice to keep buffer empty, reducing latency
        _, _ = self.camera.read()
        ret, frame = self.camera.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)

        # threshold image for bright regions
        ret, thresh = cv2.threshold(v, self.brightness_threshold, 255,
                cv2.THRESH_BINARY_INV)

        # erode and dilate the thresholded image
        thresh = cv2.medianBlur(thresh, 5)

        # Detect blobs.
        keypoints = self.detector.detect(thresh)
        points = []
        for kp in keypoints:
            #(x, y) = keypoints[0].pt
            (x, y) = kp.pt
            points.append((x, y))

        print "%d keypoints found" % len(points)
        for pt in points:
            print "  %.2f, %.2f" % pt

        # Draw detected blobs as red circles.
        thresh = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0,0,255),
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("video", thresh)
        cv2.imshow("v", v)

        self.master_frame.after(ms, self.read_position_every_n_milliseconds, ms)


"""
#  check command line arguments
if (len(sys.argv) != 2):
    print "command line: ftdi-mosfets.44.py serial_port"
    sys.exit()
port = sys.argv[1]

# open serial port
ser = serial.Serial(port, 9600)
ser.setDTR()
ser.flush()
"""

# for now, no serial
ser = None

root = Tk.Tk()
root.title('ftdi-mosfets.44.py (q to exit)')

laser_toggle_app = Laser_Toggle_App(root, ser)

root.mainloop()



"""


FRAME_WIDTH = 3
FRAME_HEIGHT = 4

# video camera
camera = cv2.VideoCapture(0)
camera.set(FRAME_WIDTH, 320)
camera.set(FRAME_HEIGHT, 240)

# blob detector
detector = cv2.SimpleBlobDetector()
 
threshmin = 220
while True:
  # capture next frame; read twice to keep buffer empty, reducing latency
  _, _ = camera.read()
  ret, frame = camera.read()

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h,s,v = cv2.split(hsv)

  # threshold image for bright regions
  ret, thresh = cv2.threshold(v, threshmin, 255, cv2.THRESH_BINARY_INV)

  # erode and dilate the thresholded image
  thresh = cv2.medianBlur(thresh, 5)

  # Detect blobs.
  keypoints = detector.detect(thresh)
  points = []
  for kp in keypoints:
    #(x, y) = keypoints[0].pt
    (x, y) = kp.pt
    points.append((x, y))

  print "%d keypoints found" % len(points)
  for pt in points:
    print "  %.2f, %.2f" % pt

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

  if key & 0xFF == ord('q'):
    break

# When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()
"""
