import selectors
import socket
import traceback

from ServerMessage import ServerMessage

class Server():
    def __init__(self, host, port):
        self.multiplexor = selectors.DefaultSelector()
        self.host, self.port = host, port
        self._setListenerSocket()
        self.multiplexor.register(self.listenerSocket, selectors.EVENT_READ, data = None)

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
        message = ServerMessage(self.multiplexor, conn, addr)
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
                            message.processServerEvents(mask)
                        except Exception:
                            print("Main: Error: exception for {}:\n{}".format(message.addr, traceback.format_exc()))
                            message.closeServerConnection()
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