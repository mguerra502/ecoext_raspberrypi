import os

from RaspAppPi.View.General.TopLevelWindow import TopLevelWindow
from RaspAppPi.View.General.FrameImage import FrameImage
from RaspAppPi.View.General.CanvasImage import CanvasImage
from RaspAppPi.View.General.ImageLoader import ImageLoader

class ScannedDoneWindow(TopLevelWindow):
    def __init__(self, theView):
        super().__init__("EcoExT", 480, 320)
        self.view = theView

        self._setImageOnScannedDoneWindow()

    def _setImageOnScannedDoneWindow(self):
        logoFrame = FrameImage(self, 480, 320)
        logoFrame.pack()
        
        logoCanvas = CanvasImage(logoFrame, 480, 320)
        logoCanvas.pack()

        pathToImage = os.path.join(os.path.dirname(__file__), r"Images\scanned.png")
        logoLoader = ImageLoader(pathToImage)
        self._logoImage = logoLoader.getPhotoImage()
        logoCanvas.create_image(240, 160, image = self._logoImage)