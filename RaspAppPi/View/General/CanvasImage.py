from tkinter import Canvas

class CanvasImage(Canvas):

    def __init__(self, master, width, height):
        super().__init__(master)
        self.configure(background = 'white', width = width, height = height)