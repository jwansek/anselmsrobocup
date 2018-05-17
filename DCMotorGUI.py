import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import simpledialog
from hardware import DCMotor

class App(tk.Tk):

    direction = "f"
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(0, 0)
        self.title("DC Motor test application")
        self.protocol("WM_DELETE_WINDOW", self._onClose)

        tk.Label(self, text = "DC Motor test application", font = ("Verdana", 14, "bold")).grid(row = 0, column = 0, columnspan = 3, padx = 3)
        tk.Button(self, text = "Backwards", command = self._backwards).grid(row = 1, column = 0, pady = 5)
        tk.Button(self, text = "Stop", command = self._stop).grid(row = 1, column = 1, pady = 5)
        tk.Button(self, text = "Forwards", command = self._forwards).grid(row = 1, column = 2, pady = 5)

        self._scale = tk.Scale(self, from_ = 0, to = 100, length = 200, orient = tk.HORIZONTAL, command = lambda a: self._onScale(a))
        self._scale.grid(row = 2, column = 0, columnspan = 3)

        p_pwm = simpledialog.askinteger("Input pin", "Input pwm pin:")
        p_dir = simpledialog.askinteger("Input pin", "Input dir pin:")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.motor = DCMotor(p_pwm, p_dir, 100)

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
