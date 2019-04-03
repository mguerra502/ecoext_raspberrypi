from threading import Thread

from RaspAppPi.Controller.HomeWindowController import HomeWindowController

class MainController():
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._homeController = HomeWindowController(self)
        # Set references of the view and the controller in the model
        self._model.getRaspberryPi().setViewController(self._view, self._homeController)
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