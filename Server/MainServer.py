import sys

from Server import Server


def MainServer():

    server = Server(sys.argv[1], int(sys.argv[2]))
    server.startMonitoringSocket()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <host> <port>".format(sys.argv[0]))
        sys.exit(1)

    MainServer()
