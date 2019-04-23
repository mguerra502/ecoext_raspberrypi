import mysql.connector
import datetime

class ServerDatabaseConnector():
    
    def __init__(self):
        self._ecoExtDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecoextv1"
        )
    
    def storeTransactionInDatabase(self, data):
        cursor = self._ecoExtDatabase.cursor()
        mysqlQuery = "INSERT INTO transactions (label, date, description) VALUES (%s, %s, %s)"
        values = (data["label"], datetime.datetime.now(), data["description"])
        cursor.execute(mysqlQuery, values)
        self._ecoExtDatabase.commit()
        # Get last inserted ID and 
        return self._returnLastTransactionIDSaved()

    def _returnLastTransactionIDSaved(self):
        cursor = self._ecoExtDatabase.cursor()
        mysqlQuery = "SELECT LAST_INSERT_ID()"
        cursor.execute(mysqlQuery)

        return cursor.fetchone()
        
    def storeKeysInDatabase(self, keysID, keyI, keyII, piPort, piAddr):
        cursor = self._ecoExtDatabase.cursor()
        mysqlQuery = "INSERT INTO keystable (id, keyaes, keyiv, ipv4, port) VALUES (%s, %s, %s, %s, %s)"
        values = (keysID, keyI, keyII, piAddr, piPort)
        cursor.execute(mysqlQuery, values)
        self._ecoExtDatabase.commit()

    def closeConnection(self):
        self._ecoExtDatabase.close()