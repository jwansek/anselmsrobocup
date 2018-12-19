from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import numpy as np
import argparse
import cv2

class App(tk.Tk):
    def __init__(self, path, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._path = path

        self._lbl_thresh = tk.Label(self, text = "thresh")
        self._lbl_orig = tk.Label(self, text = "original")
        self._lbl_thresh.grid(row = 0, column = 0)
        self._lbl_orig.grid(row = 0, column = 1)

        tk.Label(self, text = "Orange:").grid(row = 1, column = 0, padx = 3)
        tk.Label(self, text = "White:").grid(row = 1, column = 1, padx = 3)

        self._scl_orange = ttk.Scale(self, from_ = 0, to = 255, length = 200)
        self._scl_white = ttk.Scale(self, from_ = 0, to = 255, length = 200)
        self._scl_orange.grid(row = 2, column = 0, pady = 3)
        self._scl_white.grid(row = 2, column = 1, pady = 3)
        self._scl_orange.set(130)
        self._scl_white.set(100)

        self._lbl_num_orange = tk.Label(self, text = "130")
        self._lbl_num_white = tk.Label(self, text = "100")
        self._lbl_num_orange.grid(row = 3, column = 0, pady = 3)
        self._lbl_num_white.grid(row = 3, column = 1, pady = 3)

        self._img_orig = self._np_to_tk(cv2.imread(self._path))
        self._lbl_orig.config(image = self._img_orig)
        
        self.after(10, self._load_image)

    def _load_image(self):
        o = int(self._scl_orange.get())
        w = int(self._scl_white.get())
        self._lbl_num_orange.config(text = str(o))
        self._lbl_num_white.config(text = str(w))

        frame = cv2.imread(self._path)
        white = cv2.inRange(frame, (w, w, w), (255, 255, 255))
        b, g, r = cv2.split(frame)
        ret, r = cv2.threshold(r, o, 255, cv2.THRESH_BINARY)

        out = cv2.bitwise_and(r, cv2.bitwise_not(white))

        self._img_thresh = self._np_to_tk(out)
        self._lbl_thresh.config(image = self._img_thresh)

        self.after(10, self._load_image)

    def _np_to_tk(self, img):
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except cv2.error:
            #binary image
            pass
        image = Image.fromarray(img)
        return ImageTk.PhotoImage(image)

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=False,
                help='Path to the image')
args = vars(ap.parse_args())

app = App(path = args["image"])
app.mainloop()

