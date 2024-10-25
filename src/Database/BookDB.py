from src.Beans.Books import Books
from src.Beans.Status import Status
from Constants import Constants
import mysql.connector


class BookDB:
    def __init__(self,con:mysql.connector.connect()):
        self.con = con
        self.status=Status()

    def insertBook(self, b:Books, file_path)->Status:
        try:
            cursor = self.con.cursor()
            sql="""INSERT INTO books (title, author, description,price,image,seller_id) VALUES (%s, %s,%s,%s,%s,%s)"""
            values=(b.title,b.author,b.description,b.price,file_path,b.seller_id)
            cursor.execute(sql,values)
            self.con.commit()
            return self.status
        except Exception as e:
            self.status = Status(Constants.stausId1, Constants.statusMessage1)
            print(e)
        return self.status
    