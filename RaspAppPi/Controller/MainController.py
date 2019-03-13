from HomeWindowController import HomeWindowController

class MainController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._homeController = HomeWindowController(self)