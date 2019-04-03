from RaspAppPi.View.General.HomeWindow import HomeWindow
from RaspAppPi.View.General.ScannedDoneWindow import ScannedDoneWindow
from RaspAppPi.View.General.QRCodeWindow import QRCodeWindow

class WindowCreator():
    def __init__(self, model):
        self._model = model
        self._homeWindow = HomeWindow(self)
        self._scannedWindow = None
        self._qrWindow = None        

    def createQRCodeWindow(self, image):
        self._qrWindow = QRCodeWindow(self, image)

    def createScannedQRCodeWindow(self):
        self._scannedWindow = ScannedDoneWindow(self)

    def getHomeWindow(self):
        return self._homeWindow

    def getScannedWindow(self):
        return self._scannedWindow

    def getQRWindow(self):
        return self._qrWindow

    def getModel(self):
        return self._model