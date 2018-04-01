#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue as Queue
from arduino import Arduino
from orange_det_picam import OrangeTrack
from time import sleep
from large_text import Text
import argparse
    
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
            
                print(last_ard_q_rep)
                print("\t\t\t", last_cam_q_rep)
                line = last_ard_q_rep[0]
                US_L = last_ard_q_rep[1]
                US_R = last_ard_q_rep[2]
                compass = last_ard_q_rep[3]
                button_on = last_ard_q_rep[4]
                hasball = last_ard_q_rep[5]
                bangle = last_cam_q_rep
                
                                            
                ######  ######  #######  #####  ######     #    #     # 
                #     # #     # #     # #     # #     #   # #   ##   ## 
                #     # #     # #     # #       #     #  #   #  # # # # 
                ######  ######  #     # #  #### ######  #     # #  #  # 
                #       #   #   #     # #     # #   #   ####### #     # 
                #       #    #  #     # #     # #    #  #     # #     # 
                #       #     # #######  #####  #     # #     # #     # starts here!
                #TODO: write the program
                if line:
                    print(text.LINE_DETECTED)
                sleep(0.0625)
            
            except KeyboardInterrupt:
                print("Exited")
                break
            

#uber-main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--view_camera', required=False,
                    help = "Show the camera's view. More fps if disabled",
                    action = 'store_true')
    ap.add_argument('-a', '--arduino', required=False,
                    help = "Use the arduino's sensor readings",
                    action = 'store_true')
    args = vars(ap.parse_args())
    
    main = Main(use_arduino = args["arduino"])
    arduino = Arduino(main.get_ard_q())
    ot = OrangeTrack(main.get_cam_q(), showgui = args["view_camera"])
    arduino.start()
    ot.start()
    main.mainloop()
