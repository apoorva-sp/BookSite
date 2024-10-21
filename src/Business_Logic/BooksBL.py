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

    def addBook(self,b1:Books,image)->Status:
        db =dbConfig()
        BDB=BookDB(db.con)

        if image.filename == '':
            self.status= Status(self.c.statusID2,self.c.statusMessage2)
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

            self.status=BDB.insertBook(b1,file_path)

            self.status = Status()
            return self.status
        
        self.status= Status(self.c.statusID2,self.c.statusMessage2)
        return self.status
