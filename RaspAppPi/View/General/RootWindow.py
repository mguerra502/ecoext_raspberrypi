from tkinter import Tk, Label

class RootWindow(Tk):

    def __init__(self, title, width, height):
        super().__init__()
        self.withdraw()
        self.title(title)
        # self.iconbitmap(iconLocation)
        self.configure(background = 'white')
        # self.attributes('-fullscreen', True)
        self.geometry("%dx%d+0+0" % (width, height))
        self.resizable(False, False)
        self.after(1000, self.deiconify)
        