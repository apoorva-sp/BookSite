from src.Beans.Books import Books
from src.Beans.Status import Status
from src.Database.Constants import Constants
import mysql.connector
from src.Database.categoryDB import Category
from src.Database.dbconfig import dbConfig
import os


class BookDB:
    def __init__(self, con: mysql.connector.connect()):
        self.con = con
        self.status = Status()

    def GetBookID(self, title, seller_id):
        try:
            cursor = self.con.cursor()
            query = "SELECT bID FROM books WHERE title = %s AND seller_id = %s"
            cursor.execute(query, (title, seller_id))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(e)
            self.status = Status(Constants.status_id8, Constants.status_message8)

    def insertBook(self, b: Books, file_path) -> Status:
        try:
            dbTemp1 = dbConfig()
            tempcur = dbTemp1.con.cursor()
            sql = "INSERT INTO books (title, author, description,price,image,seller_id) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (b.title, b.author, b.description, b.price, file_path, b.seller_id)
            tempcur.execute(sql, values)
            dbTemp1.commit()
            book_id = self.GetBookID(b.title, b.seller_id)
            print("bookid extracted successfully", book_id)
            if book_id:
                dbTemp = dbConfig()
                CDB = Category(dbTemp.con)
                print("bid: ",book_id,"tags: ",b.tags)
                self.status = CDB.AddBookCategory(book_id,b.tags)
                print("Adding BOOK CATEGrY",self.status.message)
                if self.status.statusId == 0:
                    dbTemp.commit()
                    print("here")
                else:
                    self.status = Status(1001010,"INSERTING BOOK_CATEGORY ERROR")
                    dbTemp.rollback()
            else:
                self.status = Status(Constants.status_id4, Constants.status_message4)
        except Exception as e:
            self.status = Status(Constants.status_id2, Constants.status_message2)
            print(e)
        return self.status
    def updateimage(self, bookid, filepath)->Status:
        try:
            cursor = self.con.cursor()
            sql = "update books set image = %s where bID = %s "
            values = (filepath, bookid)
            cursor.execute(sql,values)
            return self.status
        except Exception as e:
            self.status = Status(512,"error occured while updating the database")
            return self.status


    def UpdatePrice(self, bookid, NewPrice) -> Status:
        try:
            cursor = self.con.cursor()
            sql = """UPDATE books SET price = %s WHERE bID = %s"""
            values = (NewPrice, bookid)
            cursor.execute(sql, values)
            return self.status
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status

    def DeleteBook(self, bookid,seller) -> Status:
        try:
            cursor = self.con.cursor()
            sql = """DELETE FROM books WHERE bID = %s and seller_id = %s"""
            values = (bookid,seller)
            cursor.execute(sql, values)
            return self.status
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status

    def displayOneBook(self, bid):
        try:
            cursor = self.con.cursor()
            sql = """SELECT bID, title, author,price,image FROM books WHERE bID = %s"""
            values = (bid,)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return None

    def displaySearch(self, text: str) -> Status:
        cursor = self.con.cursor()
        sql = "SELECT * FROM books WHERE title REGEXP %s ;"
        cursor.execute(sql, (text,))
        result = cursor.fetchall()
        return result

    def displayAll(self):
        try:
            cursor = self.con.cursor()
            sql = """SELECT * FROM books"""
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status.message

    def mybooks(self,buyerid):
        try:
            cursor = self.con.cursor()
            sql = """SELECT * FROM books where seller_id =%s"""
            cursor.execute(sql,(buyerid,))
            result = cursor.fetchall()
            return result

        except Exception as e:
            print(e)
            self.status = Status(600, "listing my books failed")
            return self.status.message

    def getSellerId(self, BookId):
        cur = self.con.cursor()
        sql = """
            SELECT seller_id from books where bID = %s;
        """
        cur.execute(sql, (BookId,))
        return cur.fetchone()[0]

    def deleteBookOnId(self, bookid) -> Status:
        try:
            cursor = self.con.cursor()
            sql = """DELETE FROM books WHERE bID = %s;"""
            values = (bookid,)
            cursor.execute(sql, values)
        except Exception as e:
            print(e)
            self.status = Status(Constants.status_id5, Constants.status_message5)
        return self.status

# dbcon = dbConfig()
#
# b=Books("u","u","7",7,1,["fiction"])
# bdb = BookDB(dbcon.con)
# print(bdb.insertBook(b,"static/Book_Images/1/1.jpg"))
# dbcon.commit()
# print(bdb.displayPreferedBooks(["horror","children","science"]))
# status=bdb.DeleteBook(b)
# print(status.message)

