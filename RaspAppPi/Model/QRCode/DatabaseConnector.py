import mysql.connector

class DatabaseConnector:
    
    def __init__(self):
        self.__ecoExtDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="keysdb"
        )
        
    def retriveFromDatabase(self, keysID):
        cursor = self.__ecoExtDatabase.cursor()
        mysqlQuery = "SELECT keyAES, keyIV FROM keys_stored WHERE idkeys = %s"
        condition = (keysID, )
        cursor.execute(mysqlQuery, condition)
        result = cursor.fetchone()
        return bytes(result[0]), bytes(result[1])
    
    def storeInDatabase(self, keysID, keyI, keyII):
        cursor = self.__ecoExtDatabase.cursor()
        mysqlQuery = "INSERT INTO keys_stored (idkeys, keyAES, keyIV) VALUES (%s, %s, %s)"
        values = (keysID, keyI, keyII)
        cursor.execute(mysqlQuery, values)
        self.__ecoExtDatabase.commit()
        