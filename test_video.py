import cv2
import imutils
import picamera
from picamera.array import PiRGBArray
import numpy as np

xres = 928
yres = 464
ycrop = 80

picam = picamera.PiCamera()
picam.exposure_compensation = -6

with picam as camera:
    camera.resolution = (xres, yres)
    stream = PiRGBArray(camera, size = (xres, yres))

    for frame in camera.capture_continuous(stream, format = "bgr", use_video_port = True):
        image = frame.array
        image = cv2.flip(image, -1)
        image = image[0:yres-ycrop, 0:xres]

        cv2.imshow("Camera Vision", image)
        key = cv2.waitKey(1) & 0xFF

        #no idea what this does
        stream.truncate(0)
        
        #is the 'q' key is pressed, stop the loop (thus end the program)
        #doesn't even work LUL
        if key == ord("q"):
            break
        
