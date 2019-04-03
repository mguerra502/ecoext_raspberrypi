from tkinter import Tk

class HomeWindowController():
    def __init__(self, control):
        self._controller = control

    def homeQRWindowTransition(self, qrImage):
        self._controller.getView().createQRCodeWindow(qrImage)