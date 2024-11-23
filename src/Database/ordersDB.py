import mysql.connector

from src.Beans.Status import Status
from src.Database.BookDB import BookDB
from src.Database.MembersDB import MemberDB
from src.Database.dbconfig import dbConfig


class OrdersDB:
    def __init__(self, con: mysql.connector.connect()):
        self.con = con
        self.status = Status()
        self.db = dbConfig()

    def insertOrder(self, buyerID: int, bookID: int):
        try:
            cursor = self.con.cursor()
            mdb = MemberDB(self.db.con)
            values = mdb.getOrderDetails(bookID, buyerID)
            print(bookID,values)
            sql = """INSERT INTO orders(buyerID,sellerID,bookID,amount,orderDate,ShippingAddress,DeliveryAddress) 
                VALUES(%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(sql, values)
            bdb = BookDB(self.con)
            s = bdb.deleteBookOnId(bookID)
            if s.statusId == 0:
                self.db.commitWithoutClosing()
            else:
                print("DELETING PROBLEM")
                self.db.rollback()
        except Exception as e:
            print(e)
            self.status = Status(70, "Order Insertion Error")
        return self.status


# db = dbConfig()
# odb = OrdersDB(db.con)
# print(odb.insertOrder(1,5))
# db.commit()