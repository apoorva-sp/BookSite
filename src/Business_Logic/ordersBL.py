from src.Beans.Status import Status
from src.Database.BookDB import BookDB
from src.Database.dbconfig import dbConfig
from src.Database.ordersDB import OrdersDB


class OrdersBL:
    def __init__(self):
        self.db = dbConfig()
        self.status = Status()

    def placeOrder(self,BuyerId,BookId):

        ODB = OrdersDB(self.db.con)
        BDB = BookDB(self.db.con)
        if BuyerId == BDB.getSellerId(BookId):
            self.status = Status(80,"Seller and Buyer cant be same person")
        else:
            self.status = ODB.insertOrder(BuyerId,BookId)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()
        return self.status

    def placeOrders(self,BuyerId,booksIds):
        ODB = OrdersDB(self.db.con)
        BDB = BookDB(self.db.con)
        for BookId in booksIds:
            if BuyerId == BDB.getSellerId(BookId):
                self.status = Status(81,"Seller and Buyer cant be same person")
            else:
                self.status = ODB.insertOrder(BuyerId,BookId)
            if self.status.statusId != 0:
                break
        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()
            self.status = Status(82, "Book Adding to Cart error")

# OBL = OrdersBL()
# print(OBL.placeOrder(2,1))
