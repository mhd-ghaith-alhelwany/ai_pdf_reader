import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, NONE
from PIL import ImageTk,Image  
import os
import shutil
from pdf2image import convert_from_path
from helper import *
import threading
from eyeDetector import getEyesLocation, atLeastOneEyeOpen

path = 'code/tmp/'
 
class thread(threading.Thread):
    def __init__(self, canvas):
        threading.Thread.__init__(self)
        self.canvas = canvas
        self.mode = 'scroll'
        self.counter = 0
    def run(self):   
        vid = cv2.VideoCapture(0)
        while(True):
            _, frame = vid.read()
            if self.mode == 'scroll':
                location = getEyesLocation(frame)
                scroll_val = int((location) * 10)
                self.canvas.yview_scroll(scroll_val, "units")
            if self.mode == 'screenshot':
                if atLeastOneEyeOpen(frame):
                    self.counter = self.counter + 1
                else:
                    self.counter = 0
                if self.counter == 10:
                    self.counter = 0
                    self.mode = 'scroll'
                    os.system('scrot')

            if cv2.waitKey(1) == 13:
                self.mode = 'screenshot' if self.mode == 'scroll' else 'screenshot'
                self.counter = 0
            cv2.imshow('main frame', frame)

        vid.release()


class PdfViewer:
    def __init__(self, file):
        self.file = file
        self.images = convert_from_path(file, dpi=200)
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)

    def load_images(self):
        for i in range(len(self.images)):
            name = path + str(i) + '.png'
            self.images[i].save(name, 'PNG')
            change_background_color(name, [255, 0, 0], [128, 128, 128])
            # eye_comfort(name)

            image = ImageTk.PhotoImage(Image.open(name).resize((425, 550), Image.ANTIALIAS))
            b = ttk.Label(self.scrollable_frame, image=image)
            b.pack()
            b.image = image
            self.root.update()

    def show(self):

        root = tk.Tk()
        container = tk.Frame(root)
        canvas = tk.Canvas(container, width=425, height=1100)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        container.pack(fill=NONE, expand=False)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.root = root
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame

        self.load_images()
        
        thread(self.canvas).start()

        root.mainloop()