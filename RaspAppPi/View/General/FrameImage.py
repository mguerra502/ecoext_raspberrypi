from tkinter import Frame

class FrameImage(Frame):

    def __init__(self, master, width, height):
        super().__init__(master) 
        self.configure(background = 'black', width = width, height = height)
        