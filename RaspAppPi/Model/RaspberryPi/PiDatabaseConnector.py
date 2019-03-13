import mysql.connector
import datetime

class PiDatabaseConnector:
    
    def __init__(self):
        self.__ecoExtDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ecoextv1"
        )
    
    def storeInDatabase(self, data):
        cursor = self.__ecoExtDatabase.cursor()
        mysqlQuery = "INSERT INTO transactions (label, date, description) VALUES (%s, %s, %s)"
        values = (data["transactions"][0]["label"], datetime.datetime.now(), data["transactions"][0]["description"])
        cursor.execute(mysqlQuery, values)
        self.__ecoExtDatabase.commit()
        