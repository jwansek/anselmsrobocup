import main
main.robot_stop()

import queue as Queue
import tkinter as tk
from tkinter import ttk
from arduino import Arduino
from PIL import Image

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(0, 0)
        self.title("Directions GUI")

        self.ard_q = Queue.Queue()

        self._job = None

        self.protocol("WM_DELETE_WINDOW", self.call_stop())
        self._icon = tk.PhotoImage(file = "GUIAssets/motor.gif")
        self.tk.call("wm", "iconphoto", self._w, self._icon)
        
        self._btn_forwards_left = ttk.Button(self, text = "FL", command = self.call_forwards_left)
        self._btn_forwards_left.grid(row = 0, column = 0)
        self._btn_forwards = ttk.Button(self, text = "F", command = self.call_forwards)
        self._btn_forwards.grid(row = 0, column = 1)
        self._btn_forwards = ttk.Button(self, text = "FR", command = self.call_forwards_right)
        self._btn_forwards.grid(row = 0, column = 2)

        self._btn_forwards_left = ttk.Button(self, text = "L", command = self.call_left)
        self._btn_forwards_left.grid(row = 1, column = 0)
        self._btn_forwards = ttk.Button(self, text = "Stop", command = self.call_stop)
        self._btn_forwards.grid(row = 1, column = 1)
        self._btn_forwards = ttk.Button(self, text = "R", command = self.call_right)
        self._btn_forwards.grid(row = 1, column = 2)

        self._btn_forwards_left = ttk.Button(self, text = "BL", command = self.call_backwards_left)
        self._btn_forwards_left.grid(row = 2, column = 0)
        self._btn_forwards = ttk.Button(self, text = "B", command = self.call_backwards)
        self._btn_forwards.grid(row = 2, column = 1)
        self._btn_forwards = ttk.Button(self, text = "BR", command = self.call_backwards_right)
        self._btn_forwards.grid(row = 2, column = 2)

    def get_ard_q(self):
        return self.ard_q

    def _get_arduino(self):
        ard_q_rep = None
        try:
            while True:
                ard_q_rep = self.ard_q.get_nowait()
        except Queue.Empty:
            pass

        return ard_q_rep

    def call_stop(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()

    def call_forwards_left(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.forwards_left()

    def call_forwards(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.forwards()

    def call_forwards_right(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.forwards_right()

    def call_left(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.left()

    def call_right(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.right()

    def call_backwards_right(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.backwards_right()

    def call_backwards(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.backwards()

    def call_backwards_left(self):
        try:
            self.after_cancel(self._job)
        except IndexError:
            pass
        main.robot_stop()
        self.backwards_left()

    def forwards_left(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_forwards_left(compass, switch)

        self._job = self.after(64, self.forwards_left)

    def forwards(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_forwards(compass, switch)

        self._job = self.after(64, self.forwards)

    def forwards_right(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_forwards_right(compass, switch)

        self._job = self.after(64, self.forwards_right)

    def right(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_right(compass, switch)

        self._job = self.after(64, self.right)

    def left(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_left(compass, switch)

        self._job = self.after(64, self.left)

    def backwards_right(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_backwards_right(compass, switch)

        self._job = self.after(64, self.backwards_right)
    
    def backwards(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_backwards(compass, switch)

        self._job = self.after(64, self.backwards)
    
    def backwards_left(self):
        arduino_data = self._get_arduino()
        if arduino_data is not None:
            compass = arduino_data[3]
            switch = arduino_data[-2]
            main.robot_backwards.left(compass, switch)

        self._job = self.after(64, self.backwards_left)

if __name__ == "__main__":
    app = App()
    arduino = Arduino(app.get_ard_q())
    arduino.start()
    app.mainloop()
