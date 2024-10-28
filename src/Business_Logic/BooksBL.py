from src.Beans.Books import Books
from src.Database.dbconfig import dbConfig
from src.Beans.Status import Status
from src.Database.Constants import Constants
from werkzeug.utils import secure_filename
import os
from src.Database.BookDB import BookDB

class BooksBL:
    def __init__(self):
        self.status = Status()
        self.c=Constants()
        db = dbConfig()
        bdb = BookDB(db.con)

    def addBook(self,b1:Books,image)->Status:
        if image.filename == '':
            self.status= Status(self.c.status_id1,self.c.status_message1)
            return self.status
        if image:
            filename=secure_filename(image.filename)
            UPLOAD_FOLDER = 'Images'

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            file_path = os.path.join(UPLOAD_FOLDER, filename)
            base, extension = os.path.splitext(file_path)
            i=1
            while os.path.exists(file_path):
                file_path = f"{base}_{i}{extension}"  
                i += 1
            image.save(file_path)

            self.status=self.bdb.insertBook(b1,file_path)
            return self.status
        
        self.status= Status(self.c.status_id3,self.c.status_message3)
        return self.status

    def UpdatePrice(self,b:Books,NewPrice)->Status:
        if NewPrice:
            self.status=self.bdb.UpdatePrice(b,NewPrice)
            if self.status.statusId==0:
                self.con.commit()
            else:
                self.con.rollback()
            return self.status
        else:
            self.status = Status(self.c.status_id9,self.c.status_message9)
            return self.status

    def DeleteBook(self,b:Books)->Status:
        self.status=self.bdb.DeleteBook(b)
        if self.status.statusId==0:
            self.con.commit()
        else:
            self.con.rollback()
        return self.status


