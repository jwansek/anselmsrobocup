from tkinter import *
from time import sleep
import serial
import threading
import hardware
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyS0", 9600, timeout = 1)

class Arduino(threading.Thread):
    def __init__ (self, q):
        self.q = q
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            self.q.put(self.getReading())
      
    def getReading(self):
        try:
            return [int(i.decode()) for i in ser.readline().split(b"\t")]
        except ValueError:
            return None

#this will only be called if THIS program is run, not as a module in another program
#this is used as a test
if __name__ == "__main__":
    print("Running test program")
    print("Press <Ctrl+C> to end the program")
    while True:
        try:
            print([int(i.decode()) for i in ser.readline().split(b"\t")])
        except ValueError:
            continue

