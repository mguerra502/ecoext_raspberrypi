from threading import Thread

from RaspAppPi.Controller.HomeWindowController import HomeWindowController
from RaspAppPi.Controller.QRWindowController import QRWindowController

class MainController():
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._homeController = HomeWindowController(self)
        self._QRController = None
        # Set references of the view and the controller in the model
        self._model.getRaspberryPi().setViewController(self._view, self)
        # Set a reference controller in the view
        # TODO

        # Start sockets Thread
        self._listenerThreat = Thread(target = self._model.getRaspberryPi().startMonitoringSocket)
        self._listenerThreat.start()
        # Start main loop for the GUI
        self._view.getHomeWindow().mainloop()   

    def getModel(self):
        return self._model

    def getView(self):
        return self._view

    def getHomeController(self):
        return self._homeController

    def getQRController(self):
        return self._QRController

    def createQRController(self):
        self._QRController = QRWindowController(self)