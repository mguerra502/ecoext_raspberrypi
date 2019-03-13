import os

from RaspAppPi.View.General.TopLevelWindow import TopLevelWindow
from RaspAppPi.View.General.FrameImage import FrameImage
from RaspAppPi.View.General.CanvasImage import CanvasImage
from RaspAppPi.View.General.ImageLoader import ImageLoader

class QRCodeWindow(TopLevelWindow):
    def __init__(self, theView, qrCodeImage):
        super().__init__("EcoExT", 480, 320)
        self.view = theView
        self._qrCodeImage = qrCodeImage
        self._setQRCodeOnWindow()

    def _setQRCodeOnWindow(self):
        logoFrame = FrameImage(self, 480, 320)
        logoFrame.pack()
        
        logoCanvas = CanvasImage(logoFrame, 480, 320)
        logoCanvas.pack()

        logoCanvas.create_image(240, 160, image = self._qrCodeImage)