from base64 import urlsafe_b64encode

class EcoExTIDEncoder():
    
    def __init__(self, ecoExTIDEncrypted):
        self._ecoExTIDEncoded = self._encoder(ecoExTIDEncrypted)
    
    def _encoder(self, valueToEncode):
        return urlsafe_b64encode(valueToEncode)
    
    def getEcoExTIDEncoded(self):
        return self._ecoExTIDEncoded