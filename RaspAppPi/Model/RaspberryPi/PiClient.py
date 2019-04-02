import sys
import socket
import selectors
import traceback
import json
from RaspAppPi.Model.RaspberryPi.ClientMessage import ClientMessage

class PiClient():
    def __init__(self, controller, host, port, message, piPort):
        self._controller = controller
        self.multiplexor = selectors.DefaultSelector()
        self.host, self.port = host, port
        self.request = self.createRequest(message, piPort)
        self.startConnection()

    def createRequest(self, message, piPort):
        return dict(
            type = "text/json",
            encoding = "utf-8",
            content = message,
            port = piPort
        )

    def startConnection(self):
        addr = (self.host, self.port)
        print("Starting connection to {}".format(addr))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = ClientMessage(self._controller, self.multiplexor, sock, addr, self.request)
        
        self.multiplexor.register(sock, events, data = message)

    def sendMessageToServer(self):
        try:
            while True:
                events = self.multiplexor.select(timeout = 1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.processClientEvents(mask)
                        
                    except Exception:
                        print("Main: Error: exception for {}:\n{}".format(message.addr, traceback.format_exc()))
                        message.closeClientConnection()
                # Check for a socket being monitored to continue.
                if not self.multiplexor.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.multiplexor.close()
            print("Client connection closed!")