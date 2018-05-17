# The St. Anselm's College RoboCup team 2018 repo

Repo for the code for the robots.

Works using three .py files. Two of which are responsible for getting the
'inputs' of the program. 'orange_det_picam.py' and 'arduino.py'. These are
on separate threads, which is required for some reason. These files import
data into main.py. You can see at the top of the program the way they are
read from the threads. There are 7 inputs to the program, which are:

>line

(int) integer from 0-4 indicating if white lines are detected. 1-4 are regions
0 means no lines were detected.

>US_L

(int) distance, in cm, of the reading of the left ultrasonic sensor

>US_R

ditto but with the right

>compass

angle reading of the compass sensor, used to make sure the robot is always
facing forwards

>button_on

boolean. If the button is on or off. If off, no movement is allowed

>hasbass

reading of ultrasonic sensor pointed at capture zone. Can easily be made into
boolean if required.

>bangle

angle in degrees as a bearing from the front of the robot of the ball

Useful links

>http://rcj.robocup.org/rcj2018/soccer_2018.pdf

2017 rules
