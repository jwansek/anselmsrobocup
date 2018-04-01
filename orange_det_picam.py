#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import io
import time
import picamera
from picamera.array import PiRGBArray
import numpy as np
import threading
import imutils
import math as maths

class OrangeTrack(threading.Thread):

    orangeLower = (5, 121, 125)
    orangeUpper = (200, 255, 255)

    xres = 928
    yres = 464
    ycrop = 80

    #top left and bottom right co-ordinates of the rear view mirror
    rvm = ((190, 0), (750, 120))

    font = cv2.FONT_HERSHEY_SIMPLEX
    fps_navg = 5 # how many frames to average over for the FPS timer
    fps_times = []

    div = int(xres / 130)
    oval = (int(xres*0.07), int(yres*0.7))
    
    def __init__(self, q, showgui = True):
        self.q = q
        threading.Thread.__init__(self)
        self.showgui = showgui

    def __ball_det(self, image):
        #convert to HSV colour space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #create a mask and do a series of erodations and dilations to remove any small blobs
        mask = cv2.inRange(hsv, self.orangeLower, self.orangeUpper)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        
        #find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        #only proceed if at least one contour was found
        if len(cnts) > 0:
            #find the largest contour in the mask, then use
            #it to compute the minimum enclosing circle and
            #centroid
            c = max(cnts, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            #only proceed if at least one contour was found
            if radius > 5:
                #now work out which area the ball was detected in
                if x > self.rvm[0][0] and x < self.rvm[1][0] and y > self.rvm[0][1] and y < self.rvm[1][1]:
                    return int(x), int(y), int(radius), 1
                else:
                     return int(x), int(y), int(radius), 0

    def __draw_ball(self, image, x, y, r, bangle, region):
        #draw arrow diagram
        cv2.ellipse(image, (self.oval, (100, 50), 0), (255, 255, 255), 1)
        cv2.line(image, self.oval, (self.oval[0] - (round(maths.sin(maths.radians(-bangle))*50)), self.oval[1] - (round(maths.cos(maths.radians(-bangle))*25))), (51, 92, 255), 2)
        #can't put ° symbol because openCV doesn't like extended ASCII apparently. Sad.
        cv2.putText(image, str(bangle), (self.oval[0] - 50, self.oval[1] + 50), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        #draw circle
        cv2.circle(image, (x, y), r, (0, 255, 255), 2)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(image, str(r), (round(x+(r/4)), y), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        #labels for stuff at bottom of image
        if region == 0:
            cv2.rectangle(image, (x-5, self.yres-self.ycrop-50),(x+5, self.yres-self.ycrop), (0, 255, 255), -1)
            cv2.putText(image, str(x), (x+10, self.yres-self.ycrop-50), self.font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        elif region == 1:
            cv2.rectangle(image, (x-5, 0),(x+5, 25), (0, 255, 255), -1)
            cv2.putText(image, str(x), (x-70, 25), self.font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        
        return image

    def __translate(self, x, region):
        #works out the real angle of the ball
        #from the x coordinate and the region
        bangle = int(x / self.div - 65)
        if region == 0:
            if bangle < 0:
                return bangle + 360
            else:
                return bangle
        if region == 1:
            return 180 - bangle
      
    def run(self):        
        picam = picamera.PiCamera()
        picam.exposure_compensation = -6
        fps_navg = 5 # how many frames to average over for the FPS timer
        fps_times = []

        with picam as camera:
            camera.resolution = (self.xres, self.yres)
            stream = PiRGBArray(camera, size=(self.xres, self.yres))
            
            for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                image = frame.array
                image = cv2.flip(image, -1)
                image = image[0:self.yres-self.ycrop, 0:self.xres].copy()
                cv2.rectangle(image, self.rvm[0], self.rvm[1], (0, 255, 0), 2)

                # frame rate calculation and display
                fps_times.append(time.time())
                if len(fps_times) >= fps_navg:
                    fps_times = fps_times[-fps_navg:]
                    fps = "%.2f FPS" % (fps_navg/(fps_times[-1] - fps_times[0]))
                    print("\t\t\t\t\t", fps)
                    cv2.putText(image, fps, (0, 15), self.font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

                ballpos = self.__ball_det(image)
                #ballpos is [x, y, radius, region]
                if ballpos is not None:
                    bangle = self.__translate(ballpos[0], ballpos[3])
                    if self.showgui:
                        cv2.imshow("Camera vision", self.__draw_ball(image, ballpos[0], ballpos[1], ballpos[2], bangle, ballpos[3]))
                    self.q.put(bangle)
                else:
                    if self.showgui:
                        cv2.imshow("Camera vision", image)
                                               
                key = cv2.waitKey(1) & 0xFF

                #no idea what this does
                stream.truncate(0)
                
                #is the 'q' key is pressed, stop the loop (thus end the program)
                #doesn't even work LUL
                if key == ord("q"):
                    break
