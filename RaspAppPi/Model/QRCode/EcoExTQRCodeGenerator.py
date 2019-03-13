import qrcode
from PIL import Image
from base64 import urlsafe_b64encode
import subprocess
import glob
import os

class EcoExTQRCodeGenerator:
    
    # Getting the logo from the file system
    _ecoExTLogo = Image.open('logo520x520.png')
    
    def __init__(self, valueToEncode):
        # Creating the QR Code Object
        self._valueToEncode = valueToEncode
        self._ecoExTQRCode = self._qRCodeDef()
        self._ecoExTQRCodeImage = None
        self._createEcoExTQRCodeImage()
        
    def _qRCodeDef(self):
        qR = qrcode.QRCode(
            version = 6,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 7,
            border = 1,
        )
        
        # Encoding the value that was inputed to the method
        qR.add_data(self._valueToEncode)
        qR.make(fit = False)
        
        return qR
        
    def _createEcoExTQRCodeImage(self):
        # Create an image that shows the QR Code of the encoded value
        self._ecoExTQRCodeImage = self._ecoExTQRCode.make_image(fill_color = "black", back_color = "white")
    
        # Resizing the logo
        self._ecoExTLogo = self._ecoExTLogo.resize((80, 80), Image.ANTIALIAS)
        
        # Puttin the logo in the middle of the QR code
        offSet = (int((self._ecoExTQRCodeImage.size[0] - self._ecoExTLogo.size[0])/2), int((self._ecoExTQRCodeImage.size[1] - self._ecoExTLogo.size[1])/2))
        
        ## First we have to convert the QR Image into a RGBA image
        self._ecoExTQRCodeImage = self._ecoExTQRCodeImage.convert('RGBA')
        
        ## Then we paste the logo on the code
        self._ecoExTQRCodeImage.paste(self._ecoExTLogo, offSet, self._ecoExTLogo)
        
    #def showQRCode(self):
    #    self.saveQRCode()
    #    for infile in glob.glob(os.path.join('QRImage{}.bmp'.format(urlsafe_b64encode(self._valueToEncode).decode('utf-8')))):
            # Need to put the address of your photo viewer instead of this --> C:\Program Files (x86)\Google\Picasa3\PicasaPhotoViewer.exe
    #        viewer = subprocess.Popen(['C:\Program Files (x86)\Google\Picasa3\PicasaPhotoViewer.exe', infile])
    #        viewer.wait()
    #        viewer.terminate()
    #        viewer.kill()
        
    def closeQRCode(self):
        self._ecoExTQRCodeImage.close()
        
    def saveQRCode(self):
        # Saving the QR Code with the logo
        self._ecoExTQRCodeImage.save('QRImage{}.bmp'.format(urlsafe_b64encode(self._valueToEncode).decode('utf-8')))
        
    def getQRCodeImage(self):
        return self._ecoExTQRCodeImage
        