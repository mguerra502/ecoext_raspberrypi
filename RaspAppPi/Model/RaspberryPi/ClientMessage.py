import sys
import selectors
import json
import io
import struct
import socket

from RaspAppPi.Model.QRCode.EcoExTQRCodeGenerator import EcoExTQRCodeGenerator

class ClientMessage():
    def __init__(self, controller, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recvBuffer = b""
        self._sendBuffer = b""
        self._requestQueued = False
        self._jsonHeaderLen = None
        self.jsonHeader = None
        self.response = None
        self._controller = controller
        self._unavailableServiceFlag = False

    def processClientEvents(self, mask):
        if mask & selectors.EVENT_READ:
            self.readServerMessage()
        
        if mask & selectors.EVENT_WRITE:
            self.writeClientMessage()

    def closeClientConnection(self, unavailableServiceFlag):
        print("Closing connection to {}".format(self.addr))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print("Error: selector.unregister() exception for {}: {}".format(self.addr, repr(e)))

        try:
            self.sock.close()
        except OSError as e:
            print("Error: socket.close() exception for {}: {}".format(self.addr, repr(e)))
        finally:
            # Delete ref to socket for garbage collector
            self.sock = None
            self._unavailableServiceFlag = unavailableServiceFlag

    def writeClientMessage(self):
        if not self._requestQueued:
            self.queueClientRequest()

        self._writeClientMessage()

        if self._requestQueued:
            if not self._sendBuffer:
                # Set selector to listen for read events, we are done writing
                self._setSelectorClientEventsMask("r")

    def queueClientRequest(self):
        content = {**self.request["content"], **dict(port = self.request["port"])}
        contentType = self.request["type"]
        contentEncoding = self.request["encoding"]
        
        # Assuming that the content is always of type json
        req = {
            "contentBytes": self._jsonEncode(content, contentEncoding),
            "contentType": contentType,
            "contentEncoding": contentEncoding
        }

        message = self._createClientMessage(**req)
        print("here")
        print(repr(message))
        
        self._sendBuffer += message
        self._requestQueued = True

    def _jsonEncode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii = False).encode(encoding)

    def _createClientMessage(self, *, contentBytes, contentType, contentEncoding):
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

    def _writeClientMessage(self):
        if self._sendBuffer:
            print("Sending {} to {}".format(repr(self._sendBuffer), self.addr))
            try:
                # Should be ready to write
                sent = self.sock.send(self._sendBuffer)
            except socket.error:
                # Resource temporarily unavailable
                print("Service temporarily unavailable")
                self.closeClientConnection(True)
            else:
                self._sendBuffer = self._sendBuffer[sent:]

    def _setSelectorClientEventsMask(self, mode):
        """ Set selector to listen for events: mode is 'r', 'w', or 'rw'. """
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError("Invalid events mask mode {}.".format(repr(mode)))

        self.selector.modify(self.sock, events, data = self)

    def readServerMessage(self):
        self._readServerMessage()

        if self._jsonHeaderLen is None:
            self.processClientProtoHeader()

        if self._jsonHeaderLen is not None:
            if self.jsonHeader is None:
                self.processClientJsonHeader()

        if self.jsonHeader:
            if self.response is None:
                self.processServerResponse()

    def _readServerMessage(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable
            pass
        else:
            if data:
                self._recvBuffer += data
            else:
                raise RuntimeError("Peer closed!")

    def processClientProtoHeader(self):
        headerLen = 2
        if len(self._recvBuffer) >= headerLen:
            self._jsonHeaderLen = struct.unpack(">H", self._recvBuffer[:headerLen])[0]
            self._recvBuffer = self._recvBuffer[headerLen:]
    
    def processClientJsonHeader(self):
        headerLen = self._jsonHeaderLen
        if len(self._recvBuffer) >= headerLen:
            self.jsonHeader = self._jsonDecode(self._recvBuffer[:headerLen], "utf-8")
            self._recvBuffer = self._recvBuffer[headerLen:]
            for reqHeader in ("byteorder", "content-length", "content-type", "content-encoding"):
                if reqHeader not in self.jsonHeader:
                    raise ValueError("Missing required header {}.".format(reqHeader))

    def _jsonDecode(self, jsonBytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(jsonBytes), encoding = encoding, newline = "")
        obj = json.load(tiow)
        tiow.close()

        return obj

    def processServerResponse(self):
        contentLen = self.jsonHeader["content-length"]
        if not len(self._recvBuffer) >= contentLen:
            return

        data = self._recvBuffer[:contentLen]
        self._recvBuffer = self._recvBuffer[contentLen:]
        encoding = self.jsonHeader["content-encoding"]
        self.response = self._jsonDecode(data, encoding)
        print("received response {} from {}.".format(self.response, self.addr))
        result = self.response.get("content")
        print("Got result: {}.".format(result))
        # Show QR code
        # print(result.encode("utf-8"))
        # self.qr = EcoExTQRCodeGenerator(result.encode("utf-8"))
        # self.qrImage = self.qr.getQRCodeImage()
        # self._controller.homeQRWindowTransition(self.qrImage)
        # Close when response has been processed
        self.closeClientConnection(False)

    def getUnavailableServiceFlag(self):
        return self._unavailableServiceFlag