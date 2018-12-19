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

WHITE_THRESH = 100
ORANGE_THRESH = 130

def find_average(pts):
    if pts is not None:
        x = int(np.mean(pts[:,0,0]))
        y = int(np.mean(pts[:,0,1]))

        return x, y
    else:
        return None, None

def find_ball(frame):
    white = cv2.inRange(frame, (WHITE_THRESH, WHITE_THRESH, WHITE_THRESH), (255, 255, 255))
    b, g, r = cv2.split(frame)
    ret, r = cv2.threshold(r, ORANGE_THRESH, 255, cv2.THRESH_BINARY)

    out = cv2.bitwise_and(r, cv2.bitwise_not(white))
    x, y = find_average(cv2.findNonZero(out))
    return x, y, out

def find_angle(x, y, mid):
    return np.degrees(np.arctan2(y - mid[1], x - mid[0]))

def draw_ball(frame, x, y, bangle):
    cv2.line(frame, oval, (oval[0] - (int(np.sin(np.radians(-bangle))*50)), oval[1] - (int(np.cos(np.radians(-bangle))*25))), (51, 92, 255), 2)
    cv2.putText(frame, "%.0f" % bangle, (oval[0] - 50, oval[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), )

    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
    cv2.circle(frame, mid, 3, (255, 255, 255), -1)
    cv2.line(frame, (x, y), mid, (255, 255, 255), 1)

def  translate(bangle):
        #works out the real angle of the ball
        #from the x coordinate and the region
        bangle += 90
        if bangle < 0:
            return bangle + 180
        else:
            return bangle
        
with picam as camera:
    camera.resolution = (xres, yres)
    stream = PiRGBArray(camera, size=(xres, yres))
    
    for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
        image = frame.array
        image = cv2.flip(image, -1)
        image = image[int(yres/5):yres-int(yres/3.15), int(xres/4.05):xres-int(xres/3.7)].copy()
        image = cv2.flip(image, 1)

        mid = (221, 221)
        oval = (55, 30)
        cv2.circle(image, mid, 160, (0, 0, 0), -1)
        cv2.circle(image, mid, 260, (0, 0, 0), 100)
        cv2.ellipse(image, (oval, (100, 50), 0), (255, 255, 255), 1)

        x, y, out = find_ball(image)
        if x is not None:
            bangle = translate(find_angle(x, y, mid))
            draw_ball(image, x, y, bangle)

        x, y, white = find_ball(image)

        # frame rate calculation and display
        fps_times.append(time.time())
        if len(fps_times) >= fps_navg:
            fps_times = fps_times[-fps_navg:]
            fps = "%.1f FPS" % (fps_navg/(fps_times[-1] - fps_times[0]))
            cv2.putText(image, fps, (375, 15), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)


        cv2.imshow("Press q to exit", image)
        cv2.imshow("thresh", out)
        key = cv2.waitKey(1) & 0xFF

        stream.truncate(0)
        
        if key == ord("q"):
            break      
