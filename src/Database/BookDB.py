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
        self.CDB = Category(con)

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
            cursor = self.con.cursor()
            sql = "INSERT INTO books (title, author, description,price,image,seller_id) VALUES (%s, %s,%s,%s,%s,%s)"
            values = (b.title, b.author, b.description, b.price, file_path, b.seller_id)
            cursor.execute(sql, values)
            book_id = self.GetBookID(b.title, b.seller_id)
            if book_id:
                self.status = self.CDB.AddBookCategory(book_id, b.tags)
                return self.status
            else:
                self.status = Status(Constants.status_id4, Constants.status_message4)
                return self.status
        except Exception as e:
            self.status = Status(Constants.status_id2, Constants.status_message2)
            print(e)
            return self.status

    def UpdatePrice(self, b: Books, NewPrice) -> Status:
        try:
            cursor = self.con.cursor()
            BookID = self.GetBookID(b.title, b.seller_id)
            if BookID:
                sql = """UPDATE books SET price = %s WHERE bId = %s"""
                values = (NewPrice, BookID)
                cursor.execute(sql, values)
            else:
                self.status = Status(Constants.status_id4, Constants.status_message4)
            return self.status
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status

    def DeleteBook(self, b: Books) -> Status:
        try:
            cursor = self.con.cursor()
            sql = """DELETE FROM books WHERE title = %s and seller_id = %s"""
            values = (b.title, b.seller_id)
            cursor.execute(sql, values)
            return self.status
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status

    def displayOneBook(self, b: Books):
        try:
            cursor = self.con.cursor()
            sql = """SELECT * FROM books WHERE title = %s and seller_id = %s"""
            values = (b.title, b.seller_id)
            cursor.execute(sql, values)
            result = cursor.fetchone()
            if result:
                return result
            else:
                self.status = Status(Constants.status_id4, Constants.status_message4)
        except Exception as e:
            self.status = Status(Constants.status_id5, Constants.status_message5)
            return self.status

    def displayPreferedBooks(self, preferences_list):
        cursor = self.con.cursor
        d = {0: "preferenceOne", 1: "preferenceTwo", 2: "preferenceThree"}
        preferences = []
        for i in range(3):
            sql = "SELECT * FROM books WHERE " + d[i] + "= (?)"
            cursor.execute(sql, (preferences_list[i]))
            result = cursor.fetchall()
            preferences.append(result)
        return preferences

    def displaySearch(self, text: str) -> Status:
        cursor = self.con.cursor()
        sql = "SELECT * FROM books WHERE name REGEXP %s ;"
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
