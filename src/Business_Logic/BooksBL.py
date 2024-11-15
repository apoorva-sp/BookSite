from src.Beans.Books import Books
from src.Database.dbconfig import dbConfig
from src.Beans.Status import Status
from src.Database.Constants import Constants
from werkzeug.utils import secure_filename
import os
from src.Database.BookDB import BookDB
from src.Database.categoryDB import Category

class BooksBL:
    def __init__(self):
        self.status = Status()
        self.c=Constants()
        self.db = dbConfig()
        self.bdb = BookDB(self.db.con)
        self.cdb = Category(self.db.con)

    def addBook(self, b1: Books, image,flag = False) -> Status:
        try:
            if image.filename == '':
                self.status = Status(self.c.status_id1, self.c.status_message1)
                return self.status

            if image:
                filename = secure_filename(image.filename)
                UPLOAD_FOLDER = 'Book_Images'
                id_of_user = b1.seller_id

                user_folder = os.path.join(UPLOAD_FOLDER, str(id_of_user))
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)

                file_path = os.path.join(user_folder, filename)
                base, extension = os.path.splitext(file_path)
                i = 1
                while os.path.exists(file_path):
                    file_path = f"{base}_{i}{extension}"
                    i += 1
                image.save(file_path)

                # Insert book details into the database
                if flag:
                    dbTemp = dbConfig()
                    CDB = Category(dbTemp.con)
                    self.status = CDB.AddCategory(b1.tags)
                    if self.status.statusId == 0:
                        dbTemp.commit()
                    else:
                        print("ADDING CATEGORY ERROR")
                        dbTemp.rollback()

                if self.status.statusId == 0:
                    self.status = self.bdb.insertBook(b1, file_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    print(f"Image at {file_path} deleted due to failure")

            else:
                self.status = Status(self.c.status_id3, self.c.status_message3)
        except Exception as e:
            print(f"Error: {e}")
            self.status = Status(self.c.status_id10, self.c.status_message10)
        return self.status

    def search(self,name):
        if name == "":
            self.status = Status(Constants.status_id11,Constants.status_message11)
        else:
            self.status = self.bdb.displaySearch(name)
        return self.status


    def UpdatePrice(self,b:Books,NewPrice)->Status:
        if NewPrice:
            self.status=self.bdb.UpdatePrice(b,NewPrice)
            if self.status.statusId==0:
                self.db.commit()
            else:
                self.db.rollback()
            return self.status
        else:
            self.status = Status(self.c.status_id9,self.c.status_message9)
            return self.status

    def DeleteBook(self,b:Books)->Status:
        self.status=self.bdb.DeleteBook(b)
        if self.status.statusId==0:
            self.db.commit()
        else:
            self.db.rollback()
        return self.status


