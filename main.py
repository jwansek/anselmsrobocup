#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue as Queue
from arduino import Arduino
from orange_det_picam import OrangeTrack
from time import sleep
from large_text import Text
from hardware import DCMotor
import RPi.GPIO as GPIO
import argparse

p_1A_pwm = 3
p_1A_dir = 5
p_1B_pwm = 11
p_1B_dir = 7
p_2A_pwm = 16
p_2A_dir = 12
p_2B_pwm = 13
p_2B_dir = 15
initpower = 75

GPIO.setmode(GPIO.BOARD)
m_1A = DCMotor(p_1A_pwm, p_1A_dir, initpower)
m_1B = DCMotor(p_1B_pwm, p_1B_dir, initpower)
m_2A = DCMotor(p_2A_pwm, p_2A_dir, initpower)
m_2B = DCMotor(p_2B_pwm, p_2B_dir, initpower)
   
class Main:
    def __init__(self, use_arduino):        
        
        self.ard_q = Queue.Queue()
        self.cam_q = Queue.Queue()
        self.use_arduino = use_arduino
        
    def get_ard_q(self):
        return self.ard_q
    
    def get_cam_q(self):
        return self.cam_q
        
    def mainloop(self):
        last_cam_q_rep = ""
        last_ard_q_rep = ""
        text = Text()
        sleep(5)
        while True:
            try:
                #get stuff from arduino thread (or not)
                if self.use_arduino:
                    ard_q_rep = None
                    try:
                        while True:
                            ard_q_rep = self.ard_q.get_nowait()
                    except Queue.Empty:
                        pass
                    
                    if ard_q_rep is not None:
                        last_ard_q_rep = ard_q_rep
                else:
                    last_ard_q_rep = [0, 100, 100, 0, 1, 8]
                    
                cam_q_rep = None
                
                try:
                    while True:
                        cam_q_rep = self.cam_q.get_nowait()
                except Queue.Empty:
                    pass
                
                # we have a report, so do something with it
                if cam_q_rep is not None:
                    last_cam_q_rep = cam_q_rep
            
                print("\t\t\t", last_cam_q_rep)
                try:
                    line = last_ard_q_rep[0]
                    US_L = last_ard_q_rep[1]
                    US_R = last_ard_q_rep[2]
                    compass = last_ard_q_rep[3]
                    button_on = last_ard_q_rep[4]
                    hasball = last_ard_q_rep[5]
                    bangle = last_cam_q_rep
                except IndexError:  
                    continue
                
                                            
                ######  ######  #######  #####  ######     #    #     # 
                #     # #     # #     # #     # #     #   # #   ##   ## 
                #     # #     # #     # #       #     #  #   #  # # # # 
                ######  ######  #     # #  #### ######  #     # #  #  # 
                #       #   #   #     # #     # #   #   ####### #     # 
                #       #    #  #     # #     # #    #  #     # #     # 
                #       #     # #######  #####  #     # #     # #     # starts here!
                #TODO: write the program
                print(line, US_L, US_R, compass, button_on, hasball)
                
                if hasball:
                    robot_stop()
                else:
                    robot_forwards(compass)

                sleep(0.0625)
            
            except KeyboardInterrupt:
                print("Exited")
                robot_stop()
                break

def robot_forwards(correction):
    if correction < -5:
        m_1B.backwards(100)
        m_1A.forwards(50)
    elif correction > 5:
        m_1B.backwards(50)
        m_1A.forwards(100)
    else:
        m_1A.forwards()
        m_1B.backwards()

def robot_stop():
    m_1A.stop()
    m_1B.stop()
    m_2A.stop()
    m_2B.stop()
            

#uber-main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--view_camera', required=False,
                    help = "Show the camera's view. More fps if disabled",
                    action = 'store_true')
    ap.add_argument('-a', '--arduino', required=False,
                    help = "Use the arduino's sensor readings",
                    action = 'store_true')
    ap.add_argument('-s', '--serial_connection', required = True,
                    help = "Use GPIO or USB serial connection"
                    action = "store_true")
    args = vars(ap.parse_args())

    if not args['serial_connection'].upper() in ['USB', 'GPIO']:
        ap.error("Please speciy a correct serial connection option. Must be equal to 'USB' or 'GPIO'.")

    if args['serial_connection'] == "USB":
        serialconnection = "/dev/ttyACM0"
    elif args['serial_connection'] == "GPIO":
        serialconnection = "dev/ttyS0"
    
    main = Main(use_arduino = args["arduino"])
    arduino = Arduino(main.get_ard_q(), serialport = serialconnection)
    ot = OrangeTrack(main.get_cam_q(), showgui = args["view_camera"])
    arduino.start()
    ot.start()
    main.mainloop()
