import sys
import selectors
import json
import io
import struct

from ServerDatabaseConnector import ServerDatabaseConnector
from EcoExTIDEncrypter import EcoExTIDEncrypter

class ServerMessage():
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr # Pi IPv4 address
        self._recvBuffer = b""
        self._sendBuffer = b""
        self._jsonHeaderLEn = None
        self.jsonHeader = None
        self.request = None
        self.responseCreated = False

    def processServerEvents(self, mask):
        if mask & selectors.EVENT_READ:
            self.readPiMessage()

        if mask & selectors.EVENT_WRITE:
            self.writeServerMessage()

    def readPiMessage(self):
        self._readPiMessage()

        if self._jsonHeaderLEn is None:
            self.processProtoHeader()

        if self._jsonHeaderLEn is not None:
            if self.jsonHeader is None:
                self.processJsonHeader()

        if self.jsonHeader:
            if self.request is None:
                self.processPiRequest()

    def _readPiMessage(self):
        try:
            # Should be able to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable
            pass
        else:
            if data:
                self._recvBuffer += data
            else:
                raise RuntimeError("Peer closed.")

    def processProtoHeader(self):
        headerLen = 2
        if len(self._recvBuffer) >= headerLen:
            self._jsonHeaderLEn = struct.unpack(">H", self._recvBuffer[:headerLen])[0]
            self._recvBuffer = self._recvBuffer[headerLen:]

    def processJsonHeader(self):
        headerLen = self._jsonHeaderLEn
        if len(self._recvBuffer) >= headerLen:
            self.jsonHeader = self._jsonDecode(self._recvBuffer[:headerLen], "utf-8")
            self._recvBuffer = self._recvBuffer[headerLen:]
            for reqHeader in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding"
            ):
                if reqHeader not in self.jsonHeader:
                    raise ValueError("Missing required header {}.".format(reqHeader))

    def _jsonDecode(self, jsonBytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(jsonBytes), encoding = encoding, newline = ""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def processPiRequest(self):
        contentLen = self.jsonHeader["content-length"]
        if not len(self._recvBuffer) >= contentLen:
            return

        data = self._recvBuffer[:contentLen]
        self._recvBuffer = self._recvBuffer[contentLen:]
        # I am always expecting a json request.
        encoding = self.jsonHeader["content-encoding"]
        self.request = self._jsonDecode(data, encoding)
        print("Received request {} from {}.".format(repr(self.request), self.addr))
        
        self._storeTransactionInDatabase()
        self._setSelectorServerEventsMask('w')
        
    def _storeTransactionInDatabase(self):
        # Here, we write the method to store the data in the database
        dataBaseConnector = ServerDatabaseConnector()
        transactionIdentifier = EcoExTIDEncrypter(dataBaseConnector.storeTransactionInDatabase(self.request["transactions"][0])[0], self.request["port"], self.addr[0])
        self._transactionToken = transactionIdentifier.getEncryptedEncodedID()
        dataBaseConnector.closeConnection()
        # TODO here encryption and encoding for the QR code

    def _setSelectorServerEventsMask(self, mode):
        # Set selector to listen for events:
        # Modes: 'r', 'w', or 'rw'
        if mode == 'r':
            events = selectors.EVENT_READ
        elif mode == 'w':
            events = selectors.EVENT_WRITE
        elif mode == 'rw':
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError("Invalid events mask mode {}.".format(repr(mode)))

        self.selector.modify(self.sock, events, data = self)

    def writeServerMessage(self):
        if self.request:
            if not self.responseCreated:
                self.createServerResponse()

        self._writeServerMessage()

    def createServerResponse(self):
        # I am assuming that the reponse is the type json
        # TODO
        content = {"content": self._transactionToken.decode("utf-8")}
        contentEncoding = "utf-8"
        response = {
            "contentBytes": self._jsonEncode(content, contentEncoding),
            "contentType": "text/json",
            "contentEncoding": contentEncoding
        }
        message = self._createServerMessage(**response)
        self.responseCreated = True
        self._sendBuffer += message

    def _jsonEncode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii = False).encode(encoding)

    def _createServerMessage(self, *, contentBytes, contentType, contentEncoding):
        jsonHeader = {
            "byteorder": sys.byteorder,
            "content-type": contentType,
            "content-encoding": contentEncoding,
            "content-length": len(contentBytes)
        }
        jsonHeaderBytes = self._jsonEncode(jsonHeader, "utf-8")
        messageHeader = struct.pack(">H", len(jsonHeaderBytes))
        message = messageHeader + jsonHeaderBytes + contentBytes

        return message

    def _writeServerMessage(self):
        if self._sendBuffer:
            print("Sending {} to {}.".format(repr(self._sendBuffer), self.addr))
            try:
                # Should be ready to write
                sent = self.sock.send(self._sendBuffer)
            except BlockingIOError:
                # Resource temporarily unavailable
                pass
            else:
                self._sendBuffer = self._sendBuffer[sent:]
                # Close when the buffer is drained.
                # The response has been sent.
                if sent and not self._sendBuffer:
                    print("Closing connection!")
                    self.closeServerConnection()

    def closeServerConnection(self):
        print("Closing connection to {}.".format(self.addr))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print("Error: selector.unregister() exception for {}: {}".format(self.addr, repr(e)))

        try:
            self.sock.close()
        except OSError as e:
            print("Error: socket.close() exception for {}: {}".format(self.addr, repr(e)))
        finally:
            # Delete reference to socket object for garbage collector
            self.sock = None

    