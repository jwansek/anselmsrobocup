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
    
#xres = 912
#yres = 912
xres = 460
yres = 460

picam = picamera.PiCamera()
picam.exposure_compensation = -6

font = cv2.FONT_HERSHEY_SIMPLEX

fps_navg = 5 # how many frames to average over for the FPS timer
fps_times = []

with picam as camera:
    camera.resolution = (xres, yres)
    stream = PiRGBArray(camera, size=(xres, yres))
    
    for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.flip(image, -1)
        #cv2.circle(image, (448, 416), 100, (0, 0, 0), -1)
        #image = image[int(yres/4.8):yres-int(yres/3.318), int(xres/4.053):xres-int(xres/3.8)].copy()

        # frame rate calculation and display
        fps_times.append(time.time())
        if len(fps_times) >= fps_navg:
            fps_times = fps_times[-fps_navg:]
            fps = "%.1f FPS" % (fps_navg/(fps_times[-1] - fps_times[0]))
            cv2.putText(image, fps, (0, 15), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow("Press q to exit", image)
        key = cv2.waitKey(1) & 0xFF

        stream.truncate(0)
        
        if key == ord("q"):
            break      
