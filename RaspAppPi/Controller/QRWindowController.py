from tkinter import Tk

class QRWindowController():
    def __init__(self, control):
        self._controller = control

    def qrScannedWindowTransition(self):
        self._controller.getView().createScannedQRCodeWindow()
        self._controller.getView().getScannedWindow().after(5000, self.closeScannedWindowAfter5Seconds)
        self._controller.getView().getQRWindow().destroy()

    def closeScannedWindowAfter5Seconds(self):
        self._controller.getView().getHomeWindow().update()
        self._controller.getView().getHomeWindow().deiconify()
        self._controller.getView().getHomeWindow().focus()
        self._controller.getView().getScannedWindow().destroy()