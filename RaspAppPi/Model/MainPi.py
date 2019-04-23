"""Imports of the dependencies of this class."""
import sys
from RaspAppPi.Model.RaspberryPi.Pi import Pi

"""Class definition for the Main Litening side of the Application."""
class MainPi():
    """Class for the Main Listening App."""

    def __init__(self, host, port):
        """Use to Instatiante the Main Listening Application."""
        self._raspberryPi = Pi(host, port)

    def getRaspberryPi(self):
        """Getter of the Main Listening App."""
        return self._raspberryPi