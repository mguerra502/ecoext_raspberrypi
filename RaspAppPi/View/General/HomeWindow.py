import os

from RaspAppPi.View.General.RootWindow import RootWindow
from RaspAppPi.View.General.FrameImage import FrameImage
from RaspAppPi.View.General.CanvasImage import CanvasImage
from RaspAppPi.View.General.ImageLoader import ImageLoader

class HomeWindow(RootWindow):
    def __init__(self, theView):
        super().__init__("EcoExT", 480, 320)
        self.view = theView
        self._setLogoOnHomeWindow()
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def _setLogoOnHomeWindow(self):
        logoFrame = FrameImage(self, 480, 320)
        logoFrame.pack()
        
        logoCanvas = CanvasImage(logoFrame, 480, 320)
        logoCanvas.pack()

        pathToImage = os.path.join(os.path.dirname(__file__), r"Images\logo520x520.png")
        logoLoader = ImageLoader(pathToImage)
        self._logoImage = logoLoader.getPhotoImage()
        logoCanvas.create_image(240, 160, image = self._logoImage)

    def onClosing(self):
        print("Server Connection closed!")
        self.view.getModel().getRaspberryPi().getMultiplexor().close()
        self.destroy()