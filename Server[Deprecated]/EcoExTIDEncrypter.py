from Crypto import Random
from Crypto.Cipher import AES
from EcoExTIDEncoder import EcoExTIDEncoder
from ServerDatabaseConnector import ServerDatabaseConnector
from base64 import urlsafe_b64encode

class EcoExTIDEncrypter:
    
    def __init__(self, ecoExTTransactionID, piPort, piAddr):
        self._keysGenerator()
        self._ecoExTEncryptedID = self._encryptID(ecoExTTransactionID)
        self._encodedEncryptedID = EcoExTIDEncoder(self._ecoExTEncryptedID)
        self._storeKeysToDatabase(piPort, piAddr)
        
    def _keysGenerator(self):
        # New Instance of Random Key generator
        randomKeyGenerator = Random.new()
        # Creating the 32 bytes key
        self._keyAES = randomKeyGenerator.read(32)
        # creating the 16 bytes key
        self._keyIV = randomKeyGenerator.read(16)
        # Close the Random key generator
        randomKeyGenerator.close()
        
    def _encryptID(self, valueToEncrypt):
        # First, Create the encryption object
        encrypter = AES.new(self._keyAES, AES.MODE_CFB, self._keyIV)
        # Finally, Encrypt the value
        return encrypter.encrypt(self._toByteString(valueToEncrypt))
    
    def _toByteString(self, value):
        # First, we have to change any no valid input into a byte string
        if (isinstance(value, int)):
            # Converting integer to byte string
            return value.to_bytes(95, 'big')
        elif (isinstance(value, str)):
            # Converting string to byte string
            return int(value).to_bytes(95, 'big')
        else:
            return int(value).to_bytes(95, 'big')
    
    def getEncryptedEncodedID(self):
        return self._encodedEncryptedID.getEcoExTIDEncoded()
    
    def _storeKeysToDatabase(self, piPort, piAddr):
        connector = ServerDatabaseConnector()
        connector.storeKeysInDatabase(self._encodedEncryptedID.getEcoExTIDEncoded(), self._keyAES, self._keyIV, piPort, piAddr)
        connector.closeConnection()