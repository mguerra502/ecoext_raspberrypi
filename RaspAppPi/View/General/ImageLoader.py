from PIL import Image, ImageTk

class ImageLoader():

    def __init__(self, imageLocation):
        self.__photoImage = ImageTk.PhotoImage(Image.open(imageLocation).resize((300,300), Image.ANTIALIAS))

    def getPhotoImage(self):
        return self.__photoImage
