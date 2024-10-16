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
        sql.append("""
        CREATE TABLE IF NOT EXISTS books(
            bID INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            description VARCHAR(100) NOT NULL,
            price INT NOT NULL,
            image VARCHAR(100) NOT NULL,
            seller_id INT,
            FOREIGN KEY (seller_id) REFERENCES members(mID)
        );
        """)
        sql.append(""" 
        CREATE TABLE IF NOT EXISTS orders(
            orderID INT AUTO_INCREMENT PRIMARY KEY,
            buyerID int,
            sellerID int,
            bookID int,
            orderDate DATE NOT NULL,
            amount int NOT NULL,
            ShippingAddress VARCHAR(256) NOT NULL,
            DeliveryAddress VARCHAR(256) NOT NULL,
            FOREIGN KEY (buyerID) REFERENCES members(mID),
            FOREIGN KEY (sellerID) REFERENCES members(mID),
            FOREIGN KEY (bookID) REFERENCES books(bID)
            );
                   """)
        sql.append("""
        CREATE TABLE IF NOT EXISTS cart(
            CartId INT AUTO_INCREMENT PRIMARY KEY,
            buyerID int,
            bookID int,
            FOREIGN KEY (buyerID) REFERENCES members(mID),
            FOREIGN KEY (bookID) REFERENCES books(bID)
            );
            """)
        sql.append("""
        CREATE TABLE IF NOT EXISTS category (
            cID INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50) NOT NULL
            );
            """)
        sql.append("""
        CREATE TABLE IF NOT EXISTS book_category(
            BookCID INT AUTO_INCREMENT PRIMARY KEY,
            bookID int,
            categoryID int,
            FOREIGN KEY (bookID) REFERENCES books(bID),
            FOREIGN KEY (categoryID) REFERENCES category(cID)
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