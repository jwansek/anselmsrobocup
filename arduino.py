from tkinter import *
from time import sleep
import serial
import threading
import hardware
import RPi.GPIO as GPIO
import sys

class Arduino(threading.Thread):
    def __init__ (self, q, serialport):
        threading.Thread.__init__(self)
        self.q = q

        self.ser = serial.Serial(serialport, 9600, timeout = 1)
        
    def run(self):
        while True:
            self.q.put(self.getReading())
      
    def getReading(self):
        try:
            return [int(i.decode()) for i in self.ser.readline().split(b"\t")]
        except ValueError:
            return None

#this will only be called if THIS program is run, not as a module in another program
#this is used as a test
if __name__ == "__main__":
    port = sys.argv[1]
    if port == "GPIO":
        port = "/dev/ttyS0"
    elif port == "USB":
        port = "/dev/ttyACM0"
    else:
        print("Invalid argument. Must be equal to 'GPIO' or 'USB'.")

    ser = serial.Serial(port, 9600, timeout = 1)
    
    print("Running test program")
    print("Press <Ctrl+C> to end the program")
    while True:
        try:
            print([int(i.decode()) for i in ser.readline().split(b"\t")])
        except ValueError:
            continue

