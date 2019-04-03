from RaspAppPi.Model.MainPi import MainPi
from RaspAppPi.View.WindowCreator import WindowCreator
from RaspAppPi.Controller.MainController import MainController

class MainApp():
    def __init__(self, host, port):
        self._listener = MainPi(host, port)
        self._windows = WindowCreator(self._listener)
        self._controllers = MainController(self._listener, self._windows)

    def getListener(self):
        return self._listener

    def getWindows(self):
        return self._windows

    def getControllers(self):
        return self._controllers