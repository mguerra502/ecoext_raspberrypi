"""Imports of the dependencies of this class."""
from sys import exit, argv
import sys
from RaspAppPi.MainApp import MainApp

"""Method to run the Pi Application."""
def QRGeneratorApp():
    """Here, the Main App is instatiated."""
    MainApp(sys.argv[1], int(sys.argv[2]))
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <host> <port>".format(sys.argv[0]))
        sys.exit(1)

    QRGeneratorApp()