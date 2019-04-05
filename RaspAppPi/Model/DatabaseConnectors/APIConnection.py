import requests
import json
import pprint

class APIConnection():
    def __init__(self):
        self._url = 'http://10.250.1.250:8888/api'

    def storeTransactionInDatabase(self, transaction):
        
        transactionStr = self._jsonToCleanString(transaction)
        
        mutation = """
            mutation addTransaction {
                addTransaction(
                    %s
                ) {
                    token_id
                }
            }
        """ % (transactionStr)

        jsonMutation = {
            'query' : mutation
        }
        
        response = requests.post(url = self._url, json = {'query': mutation})
        
        jsonResponse = json.loads(response.text)
        
        return jsonResponse["data"]["addTransaction"]["token_id"]

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
        jsonVar = jsonVar.replace("\"socketInfo\"", "socketInfo")
        jsonVar = jsonVar.replace("\"paymentInfo\"", "paymentInfo")
        jsonVar = jsonVar.replace("\"payment_type\"", "payment_type")
        jsonVar = jsonVar.replace("\"ammount\"", "ammount")
        jsonVar = jsonVar.replace("\"ipv4\"", "ipv4")
        jsonVar = jsonVar.replace("\"port\"", "port")
        jsonVar = jsonVar.replace("\\", "")

        return jsonVar