import mysql.connector
from keywords import *

class dbConfig:
    def __init__(self):
        self.con = mysql.connector.connect(host=keywords.host, user=keywords.username, password=keywords.password, port=keywords.port,database=keywords.database)
        self.cur = self.con.cursor()


    def initialize():
        con = mysql.connector.connect(host=keywords.host, user=keywords.username, password=keywords.password, port=keywords.port)
        cur = con.cursor()
        sql =[]
        sql.append("CREATE DATABASE IF NOT EXISTS BOOKSITE;")
        sql.append("USE BOOKSITE;")
        sql.append("""
        CREATE TABLE IF NOT EXISTS members(
            mID INT PRIMARY KEY,
            username VARCHAR(20) UNIQUE NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(30) UNIQUE NOT NULL,
            password VARCHAR(32) NOT NULL,
            AddressLineOne VARCHAR(30) NOT NULL,
            AddressLineTwo VARCHAR(30),
            City VARCHAR(30) NOT NULL,
            State VARCHAR(30) NOT NULL,
            Country VARCHAR(30) NOT NULL,
            pincode VARCHAR(10) NOT NULL
        );
        """)
        for statement in sql:
            cur.execute(statement)
        con.commit()


    def dropDatabase(self):
        sql = "DROP DATABASE IF EXISTS BOOKSITE;"
        self.cur.execute(sql)
        self.con.commit()

    def commit(self):
        self.con.commit()
        self.con.close()

    def rollback(self):
        self.con.rollback()
        self.con.close()


dbConfig.initialize()