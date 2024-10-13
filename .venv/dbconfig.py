import mysql.connector
from keywords import *

class dbConfig:
    def __init__(self):
        self.con = mysql.connector.connect(host=keywords.host, user=keywords.username, password=keywords.password, port=keywords.port,database=keywords.database)
        self.cur = con.cursor()


    def initialize():
        con = mysql.connector.connect(host=keywords.host, user=keywords.username, password=keywords.password, port=keywords.port)
        cur = con.cursor()
        sql =[]
        sql.append("CREATE DATABASE BOOKSITE;")
        sql.append( "CREATE Table members(mID int primary key," +
                    "username varchar(20) unique not null,"+
                    "phone varchar(20) unique not null,"+
                    "email varchar(30) unique not null,"+
                    "password varchar(32) not null,"+
                    "AddressLineOne varchar(30) not null,"+
                    "AddressLineTwo varchar(30) not null,"+
                    "City varchar(30) not null,"+
                    "State varchar(30) not null,"+
                    "Country varchar(30) not null,"+
                    "pincode varchar(10) not null;")
        cur.execute(sql)
        con.commit()


    def dropDatabase(self):
        sql = "DROP DATABASE BOOKSITE;"
        self.cur.execute(sql)
        self.con.commit()

    def commit(self):
        self.con.commit();
        self.con.close()

    def rollback(self):
        self.con.rollback()
        self.con.close()


# dbConfig.initialize()