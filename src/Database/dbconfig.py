import mysql.connector
from keywords import Keywords

class dbConfig:
    def __init__(self):
        self.con = mysql.connector.connect(host=Keywords.host, user=Keywords.username, password=Keywords.password,
                                           port=Keywords.port, database=Keywords.database)
        self.cur = self.con.cursor()

    @staticmethod
    def initialize():
        try:
            con = mysql.connector.connect(host=Keywords.host, user=Keywords.username, password=Keywords.password,
                                          port=Keywords.port)
            cur = con.cursor()
            sql = []
            sql.append("CREATE DATABASE IF NOT EXISTS BOOKSITE;")
            sql.append("USE BOOKSITE;")
            sql.append(""" 
                        CREATE TABLE IF NOT EXISTS members(
                            mID INT PRIMARY KEY AUTO_INCREMENT,
                            phone VARCHAR(20) UNIQUE NOT NULL,
                            fullname VARCHAR(20) NOT NULL,
                            passkey VARCHAR(32) NOT NULL,
                            addressLineOne VARCHAR(30) NOT NULL,
                            addressLineTwo VARCHAR(30),
                            city VARCHAR(30) NOT NULL,
                            state VARCHAR(30) NOT NULL,
                            pincode VARCHAR(10) NOT NULL,
                            preferenceOne VARCHAR(20) NOT NULL,
                            preferenceTwo VARCHAR(20) NOT NULL,
                            preferenceThree VARCHAR(20) NOT NULL
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
                            seller_id INT NOT NULL,
                            FOREIGN KEY (seller_id) REFERENCES members(mID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE
                        );
                        """)
            sql.append(""" 
                        CREATE TABLE IF NOT EXISTS orders(
                            orderID INT AUTO_INCREMENT PRIMARY KEY,
                            buyerID INT NOT NULL, 
                            sellerID INT NOT NULL,
                            bookID INT NOT NULL,
                            orderDate TEXT NOT NULL,
                            amount INT NOT NULL,
                            ShippingAddress VARCHAR(256) NOT NULL,
                            DeliveryAddress VARCHAR(256) NOT NULL,
                            FOREIGN KEY (buyerID) REFERENCES members(mID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE,
                            FOREIGN KEY (sellerID) REFERENCES members(mID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE
                        );
                        """)
            sql.append(""" 
                        CREATE TABLE IF NOT EXISTS cart(
                            CartId INT AUTO_INCREMENT PRIMARY KEY,
                            buyerID INT,
                            bookID INT,
                            FOREIGN KEY (buyerID) REFERENCES members(mID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE,
                            FOREIGN KEY (bookID) REFERENCES books(bID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE
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
                            bookID INT,
                            categoryID INT,
                            FOREIGN KEY (bookID) REFERENCES books(bID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE,
                            FOREIGN KEY (categoryID) REFERENCES category(cID) 
                                ON DELETE CASCADE 
                                ON UPDATE CASCADE
                        );
                        """)

            for statement in sql:
                cur.execute(statement)
            con.commit()
            print("Initialized Successfully")
        except Exception as e:
            print(e)

    @staticmethod
    def destroyAll():
        try:
            con = mysql.connector.connect(host=Keywords.host, user=Keywords.username, password=Keywords.password,
                                          port=Keywords.port)
            cur = con.cursor()
            sql = "DROP DATABASE IF EXISTS BOOKSITE;"
            cur.execute(sql)
            con.commit()
            print("Successfully Destroyed Alll Data")
        except Exception as e:
            print(e)

    def commit(self):
        try:
            self.con.commit()
            self.con.close()
        except Exception as e:
            print(e)

    def rollback(self):
        try:
            self.con.rollback()
            self.con.close()
        except Exception as e:
            print(e)


# dbConfig.destroyAll()
# dbConfig.initialize()