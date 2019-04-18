from tkinter import Tk

class HomeWindowController():
    def __init__(self, control):
        self._controller = control

    def homeQRWindowTransition(self, qrImage):
        self._controller.getView().createQRCodeWindow(qrImage)
        self._controller.getView().getQRWindow().after(20000, self.closeQRWindowAfter20Seconds)
        self._controller.getView().getHomeWindow().withdraw()

    def closeQRWindowAfter20Seconds(self):
        self._controller.getView().createNotScannedQRCodeWindow()
        self._controller.getView().getNotScannedWindow().after(5000, self.closeNotScannedWindowAfter5Seconds)
        self._controller.getView().getQRWindow().destroy()

    def closeNotScannedWindowAfter5Seconds(self):
        self._controller.getView().getHomeWindow().update()
        self._controller.getView().getHomeWindow().deiconify()
        self._controller.getView().getHomeWindow().focus()
        self._controller.getView().getNotScannedWindow().destroy()

        