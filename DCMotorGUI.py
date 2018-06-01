import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from hardware import DCMotor

class App(tk.Tk):

    direction = "f"
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(0, 0)
        self.title("DC Motor test application")
        self.protocol("WM_DELETE_WINDOW", self._onClose)
        self._icon = tk.PhotoImage(file = "GUIAssets/motor.gif")
        self.tk.call("wm", "iconphoto", self._w, self._icon)
        
        self._img_m = tk.PhotoImage(file = "GUIAssets/motor.png")
        self._img_l = tk.PhotoImage(file = "GUIAssets/left.png")
        self._img_r = tk.PhotoImage(file = "GUIAssets/right.png")
        tk.Label(self, image = self._img_m).grid(row = 0, column = 0, rowspan = 4)

        tk.Label(self, text = "DC Motor test application", font = ("Verdana", 14, "bold")).grid(row = 0, column = 1, columnspan = 3, padx = 3)
        ttk.Button(self, image = self._img_l, command = self._backwards).grid(row = 1, column = 1, pady = 5)
        ttk.Button(self, text = "Stop", command = self._stop).grid(row = 1, column = 2, pady = 5)
        ttk.Button(self, image = self._img_r, command = self._forwards).grid(row = 1, column = 3, pady = 5)

        p_pwm = simpledialog.askinteger("Input pin", "Input pwm pin:")
        p_dir = simpledialog.askinteger("Input pin", "Input dir pin:")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.motor = DCMotor(p_pwm, p_dir, 100)

        tk.Label(self, text = "pwm pin: %i       dir pin: %i" % (p_pwm, p_dir)).grid(row = 2, column = 1, columnspan = 3)
        
        self._scale = tk.Scale(self, from_ = 0, to = 100, length = 200, orient = tk.HORIZONTAL, command = lambda a: self._onScale(a))
        self._scale.grid(row = 3, column = 1, columnspan = 3)

    def _backwards(self):
        self.direction = "b"
        self.motor.backwards()

    def _forwards(self):
        self.direction = "f"
        self.motor.forwards()

    def _stop(self):
        self.motor.stop()

    def _onScale(self, power):
        if self.direction == "b":
            self.motor.backwards(float(power))
        else:
            self.motor.forwards(float(power))

    def _onClose(self):
        print("close")
        del self.motor
        self.destroy()

if __name__ == "__main__":
    root = App()
    root.mainloop()
