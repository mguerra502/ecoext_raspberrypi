"""Imports of the dependencies of this class."""
import selectors
import socket
import traceback

from RaspAppPi.Model.RaspberryPi.PiMessage import PiMessage

"""Class definition for the Socket and Selectors Application."""
class Pi():
    """Class for the Socket and Selectors App."""

    def __init__(self, host, port):
        """Use to Instatiante the Socket and Selectors Application."""
        self.multiplexor = selectors.DefaultSelector()
        self.host, self.port = host, port
        self._setListenerSocket()
        self.multiplexor.register(self.listenerSocket, selectors.EVENT_READ, data = None)
    
    def setViewController(self, view, controller):
        """Set a reference of the view and controller in the listening thread."""
        self._view = view
        self._controller = controller

    def _setListenerSocket(self):
        self.listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listenerSocket.bind((self.host, self.port))
        self.listenerSocket.listen()
        print("Listening on {}".format((self.host, self.port)))
        self.listenerSocket.setblocking(False)

    def _acceptConnectionWrapper(self, sock):
        # Here is when I Accept the connection, so I have to prepare
        # the data to send it to the database
        conn, addr = self.listenerSocket.accept() # Should be ready to read
        print("Accepted connection from {}.".format(addr))
        conn.setblocking(False)
        message = PiMessage(self._controller, self.multiplexor, conn, addr, self.port)
        self.multiplexor.register(conn, selectors.EVENT_READ, data = message)

    def startMonitoringSocket(self):
        try:
            while True:
                self._homeWindowClosed = False
                self._events = self.multiplexor.select(timeout = 1)
                
                if self._homeWindowClosed:
                    break

                for key, mask in self._events:
                    if key.data is None:
                        self._acceptConnectionWrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.processPiEvents(mask)
                        except Exception:
                            print("Main: Error: exception for {}:\n{}".format(message.addr, traceback.format_exc()))
                            message.closePiConnection()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting!")
        finally:
            self.multiplexor.close()
            print("Server Connection closed!")

    def getMultiplexor(self):
        self._homeWindowClosed = True
        return self.multiplexor

    def getListenerSocket(self):
        return self.listenerSocket

    def getEvents(self):
        return self._events