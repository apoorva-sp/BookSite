from src.Beans.Books import Books
from src.Beans.Status import Status
from src.Database.Constants import Constants
import mysql.connector
from src.Database.categoryDB import Category
from src.Database.dbconfig import dbConfig
import os

class CartDB:
    def __init__(self, con: mysql.connector.connect()):
        self.con = con
        self.status = Status()

    def add_to_cart(self,book_id,buyer_id)->Status:
        try:
            cursor=self.con.cursor()
            sql = "insert into cart (buyerID , bookID) values ( %s , %s)"
            values= (buyer_id,book_id)
            cursor.execute(sql, values)
        except Exception as e:
            print(e)
            self.status = Status(500,"ADDING TO CART FAILED")
        return self.status

    def get_bookids(self,buyer_id):
        try:
            cursor=self.con.cursor()
            sql = "select bookID from cart where buyerID= %s"
            cursor.execute(sql,(buyer_id,))
            bookids= cursor.fetchall()
            if bookids:
                print(bookids)
                return bookids
            else:
                self.status = Status(503,"no books found")
                return None
        except Exception as e:
            print(e)
            self.status = Status(504,"book id retrival failed")
            return None

    def delete_from_cart(self,bookid,buyer_id)->Status:
        try:
            cursor=self.con.cursor()
            sql= "delete from cart where bookID = %s and buyerID= %s"
            cursor.execute(sql,(bookid,))

        except Exception as e:
            print(e)
            self.status = Status(505,"book deletion failed")
        return self.status
# db=dbConfig()
# crb=CartDB(db.con)
# print(crb.get_bookids(1))

