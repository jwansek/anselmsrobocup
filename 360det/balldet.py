from time import sleep
import numpy as np
import cv2

vid = cv2.VideoCapture("vid1.avi")
fps = int(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)

def find_average(pts):
    if pts is not None:
        x = int(np.mean(pts[:,0,0]))
        y = int(np.mean(pts[:,0,1]))

        return x, y
    else:
        return None, None

def find_ball(frame):
    white = cv2.inRange(frame, (100, 100, 100), (255, 255, 255))
    b, g, r = cv2.split(frame)
    ret, r = cv2.threshold(r, 130, 255, cv2.THRESH_BINARY)

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


while True:
    ret, frame = vid.read()
    if not ret:
        break

    mid = (224, 233)
    oval = (60, 35)
    cv2.circle(frame, mid, 170, (0, 0, 0), -1)
    cv2.circle(frame, mid, 260, (0, 0, 0), 100)
    cv2.rectangle(frame, (0, 0), (448, 20), (0, 0, 0), -1)
    cv2.ellipse(frame, (oval, (100, 50), 0), (255, 255, 255), 1)

    x, y, out = find_ball(frame)
    if x is not None:
        bangle = find_angle(x, y, mid)
        draw_ball(frame, x, y, bangle)


    #cv2.imshow("thresh", out)
    cv2.imshow("Press <q> to exit", frame)
    if cv2.waitKey(delay) & 0xFF == ord("q"):
        break

vid.release()
cv2.destroyAllWindows()