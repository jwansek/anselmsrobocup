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
#it's probably better to run this in command than IDLE because IDLE adds loads of
#latency which makes it look as if the phototransistors aren't working properly
if __name__ == "__main__":
    print("Running test program")
    print("Press <Ctrl+C> to end the program")

    while True:
        try:
            rep = [int(i.decode()) for i in ser.readline().split(b"\t")]
            print(rep)
        except Exception as e:
            print(e)
