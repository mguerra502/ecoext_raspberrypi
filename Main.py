from sys import exit, argv
import sys
from RaspAppPi.MainApp import MainApp

def QRGeneratorApp():
    MainApp(sys.argv[1], int(sys.argv[2]))
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <host> <port>".format(sys.argv[0]))
        sys.exit(1)

    QRGeneratorApp()