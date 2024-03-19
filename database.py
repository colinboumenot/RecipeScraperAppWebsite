import sqlite3
import mysql.connector

class SQL:
    

    mydb = mysql.connector.connect(
        host = "localhost:3306",
        user="root",
        password="Sr1k@r36",
        database="orders"

    )
    cursor = mydb.cursor()
    sql = "INSERT INTO Pets (petID, petName, kind, gender, age, ownerID, adoptionID) VALUES(R3-7551, 'Keller', 'Parrot', 'female', '2', 7908, NULL);"
    cursor = mydb.cursor(sql)

    def __init__(self, petID = 0, petName = 0, kind = 0, gender = 0, age = 0, ownerID = 0, adoptionID = 0) -> None:
        #add in the database
        sql = "USE orders; INSERT INTO Pets (petID, petName, kind, gender, age, ownerID, adoptionID) VALUES(R3-7551, 'Keller', 'Parrot', 'female', '2', 7908, NULL);"
        

    def add(self):
        sql = "INSERT INTO Pets (petID, petName, kind, gender, age, ownerID, adoptionID) VALUES(R3-7551, 'Keller', 'Parrot', 'female', '2', 7908, NULL);"

    def insert(self, column, value):
        pass

    def delete(self, row):
        pass

    def update(self, column, value):
        pass

    def select(self, column, value):
        pass
