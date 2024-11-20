from src.Beans.Member import Member
from src.Beans.Status import Status
from src.Database.Constants import Constants
from src.Database.MembersDB import MemberDB
from src.Database.dbconfig import dbConfig
from src.Database.CartDB import CartDB
from src.Database.BookDB import BookDB


class CartBL:

    def __init__(self):
        self.status = Status()
        self.db = dbConfig()
        self.CRB = CartDB(self.db.con)

    def AddToCart(self,BID,buyer_id)->Status:
        try:
            if BID=="" or buyer_id=="":
                self.status=Status(501,"book id or buyer id not found")
            else:
                self.status = self.CRB.add_to_cart(BID,buyer_id)
                if self.status.statusId ==0:
                    self.db.commit()
                else:
                    self.db.rollback()
        except Exception as e:
            print(e)
            self.db.rollback()
            self.status = Status(502," ERROR OCCURED WHILE ADDING TO CART ")
        return self.status

    def get_books(self,buyer_id):
        try:
            bookids = self.CRB.get_bookids(buyer_id)
            book_list=[]
            BDB=BookDB(self.db.con)
            for id in bookids:
                res= BDB.displayOneBook(id[0])
                result = list(res)
                book_list.append(result)
            return book_list
        except Exception as e:
            print(e)
            self.status = Status(502," ERROR OCCURED WHILE retriving books for cart ")
    def delete_from_cart(self,bookid,buyer_id):
        try:
            self.status= self.CRB.add_to_cart(bookid,buyer_id)
            if self.status ==0:
                self.db.commit()
            else:
                self.db.rollback()

        except Exception as e:
            print(e)
            self.db.rollback()
            self.status = Status(506," ERROR OCCURED WHILE deleting books from cart ")

# cbl=CartBL()
#print(cbl.AddToCart(23,1))
# print(cbl.get_books(1))
