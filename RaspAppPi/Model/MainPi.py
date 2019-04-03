import sys
from RaspAppPi.Model.RaspberryPi.Pi import Pi

class MainPi():
    def __init__(self, host, port):
        self._raspberryPi = Pi(host, port)

    def getRaspberryPi(self):
        return self._raspberryPi