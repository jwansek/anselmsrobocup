import os
try:
    import cv2
except ImportError:
    print("""The program failed because you need to run this program in the openCV virtual environment.
This can be done in the following way:
    -Open the terminal
    -type source ~/.profile
    -type workon cv
    -type cd %s
    -type python3 %s""" % (os.getcwd(), __file__))
    
import time
import picamera
from picamera.array import PiRGBArray
import numpy as np
    
xres = 912
yres = 912

picam = picamera.PiCamera()
picam.exposure_compensation = -6

font = cv2.FONT_HERSHEY_SIMPLEX

fps_navg = 5 # how many frames to average over for the FPS timer
fps_times = []

fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter("output2.avi", fourcc, 5.0, (447, 448))

with picam as camera:
    camera.resolution = (xres, yres)
    stream = PiRGBArray(camera, size=(xres, yres))
    
    for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.flip(image, -1)
        #cv2.circle(image, (448, 416), 100, (0, 0, 0), -1)
        image = image[int(yres/4.8):yres-int(yres/3.318), int(xres/4.053):xres-int(xres/3.8)].copy()
        
        cv2.imshow("Press q to exit", image)
        out.write(image)
        key = cv2.waitKey(1) & 0xFF

        stream.truncate(0)
        
        if key == ord("q"):
            out.release()
            break      
