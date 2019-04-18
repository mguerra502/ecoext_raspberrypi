from tkinter import Tk

class QRWindowController():
    def __init__(self, control):
        self._controller = control

    def qrScannedWindowTransition(self):
        self._controller.getView().createScannedQRCodeWindow()
        self._controller.getView().getHomeWindow().withdraw()