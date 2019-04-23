"""Imports of the dependencies of this class."""
from RaspAppPi.Model.MainPi import MainPi
from RaspAppPi.View.WindowCreator import WindowCreator
from RaspAppPi.Controller.MainController import MainController

"""Class definition for the Main Pi Application."""
class MainApp():
    """Class for the Main Pi App."""

    def __init__(self, host, port):
        """Use to Instatiante for the Main Pi Application."""
        self._listener = MainPi(host, port)
        self._windows = WindowCreator(self._listener)
        self._controllers = MainController(self._listener, self._windows)

    def getListener(self):
        """Getter for the listener of the App."""
        return self._listener

    def getWindows(self):
        """Getter for the windows of the App."""
        return self._windows

    def getControllers(self):
        """Getter for the controllers of the App."""
        return self._controllers