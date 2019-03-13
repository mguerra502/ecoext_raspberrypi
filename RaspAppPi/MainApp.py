from RaspAppPi.Model.MainPi import MainPi
from RaspAppPi.View.WindowCreator import WindowCreator
from RaspAppPi.Controller.MainController import MainController

class MainApp():
    def __init__(self, host, port):
        self.listener = MainPi(host, port)
        self.windows = WindowCreator(self.listener)
        self.controllers = MainController(self.listener, self.windows)
        
        