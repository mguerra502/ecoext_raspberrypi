import requests
import json
import pprint

class APIConnection():
    def __init__(self):
        self._url = 'http://192.168.0.41:8888/api'

    def storeTransactionInDatabase(self, transaction):
        
        transactionStr = self._jsonToCleanString(transaction)
        
        mutation = """
            mutation addTransaction {
                addTransaction(
                    %s
                ) {
                    transaction_id
                }
            }
        """ % (transactionStr)

        jsonMutation = {
            'query' : mutation
        }
        
        response = requests.post(url = self._url, json = jsonMutation)
        
        jsonResponse = json.loads(response.text)
        return (json.dumps(jsonResponse, indent = 4, sort_keys = False))

    def _jsonToCleanString(self, jsonVar):
        jsonVar = json.dumps(jsonVar)
        jsonVar = jsonVar[1:len(jsonVar) - 1]
        jsonVar = jsonVar.replace("\"label\"", "label")
        jsonVar = jsonVar.replace("\"description\"", "description")
        jsonVar = jsonVar.replace("\"items\"", "items")
        jsonVar = jsonVar.replace("\"product\"", "product")
        jsonVar = jsonVar.replace("\"price\"", "price")
        jsonVar = jsonVar.replace("\"quantity\"", "quantity")
        jsonVar = jsonVar.replace("\"tax\"", "tax")
        jsonVar = jsonVar.replace("\"keys\"", "keys")
        jsonVar = jsonVar.replace("\"ipv4\"", "ipv4")
        jsonVar = jsonVar.replace("\"port\"", "port")
        jsonVar = jsonVar.replace("\\", "")

        return jsonVar