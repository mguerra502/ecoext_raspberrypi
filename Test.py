"""Imports of the dependencies of this class."""
import unittest
import json

from RaspAppPi.Model.DatabaseConnectors.APIConnection import APIConnection

"""Class definition for the Application Tests"""
class ApplicationTests(unittest.TestCase):
    """Class for the App Tests"""

    def testSendTransactionToAPITokenLength(self):
        """Tets that a Transaction can be stored in database and Retrives a 128 Characters Token."""
        # First, we load the json file that represents the transaction from the folder fixtures
        with open(r"Tests\Unit\Fixtures\data.json") as f:
            message = json.load(f)
            
        # Instance of the API connection
        apiConnector = APIConnection()

        # Sending transaction to the API
        apiResponse = apiConnector.storeTransactionInDatabase(message["transaction"], "192.168.0.41", 31000)

        # Here, we assert if the token received has a length of 128 characteres
        # It is difficult to test the partterns in the token given that is pseudo randomly
        # created in the API. The length is the only thing that we want to ensure is 128.
        self.assertEqual(len(apiResponse["data"]["addTransaction"]["token_id"]), 128)

    def testSendBadDataToAPI(self):
        """Tets that a Trasaction has to have a Structure in the file data.json if not it can be sent to API."""
        # First, we load the json file that represents the transaction from the folder fixtures
        with open(r"Tests\Unit\Fixtures\badData.json") as f:
            message = json.load(f)
            
        # Instance of the API connection
        apiConnector = APIConnection()

        # Sending transaction to the API
        # As well as we have to access the "transaction" index in the message to be able to send that data to API
        # If not a exeption is raised
        apiResponse = apiConnector.storeTransactionInDatabase(message["transaction"], "192.168.0.41", 31000)

        with self.assertRaises(TypeError):
            token = apiResponse["data"]["addTransaction"]["token_id"]

if __name__ == '__main__':
    unittest.main()
