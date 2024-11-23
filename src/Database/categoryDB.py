from src.Beans.Books import Books
from src.Beans.Status import Status
from src.Database.Constants import Constants
import mysql.connector
from src.Database.dbconfig import dbConfig

class Category:
    def __init__(self,con:mysql.connector.connect()):
        self.con = con
        self.status=Status()

    def AddCategory(self,categoryList)->Status:
        try:
            cursor = self.con.cursor()
            sql="""select category from category"""
            cursor.execute(sql)
            data = cursor.fetchall()
            existing_categories = {row[0] for row in data}
            new_Category=[category for category in categoryList if category not in existing_categories]
            if new_Category:
                sql = "INSERT INTO category (category) VALUES (%s)"
                cursor.executemany(sql,[(cat,) for cat in new_Category])
            else:
                self.status=Status(Constants.status_id6,Constants.status_message6)
        except Exception as e:
            self.status=Status(Constants.status_id2,Constants.status_message2)
        return self.status

    def GetCategoryId(self, category):
        try:
            cursor = self.con.cursor()
            sql = "SELECT cID FROM category WHERE category = %s"
            cursor.execute(sql, (category,))
            category_id = cursor.fetchone()
            if category_id:

                return category_id[0]
            else:
                return None
        except Exception as e:
            # Set status with the error message if needed
            self.status = Status(Constants.status_id5, Constants.status_message5)
            print(f"Error retrieving category ID: {e}")
            return None

    def AddBookCategory(self,book_id,CategoryList:list):
        try:
            cursor = self.con.cursor()
            for category in CategoryList:
                cat=self.GetCategoryId(category)
                print("category id retrieved is ",cat)
                if cat:
                    sql = "INSERT INTO book_category (bookId,categoryId) VALUES (%s,%s)"
                    cursor.execute(sql,(book_id,cat))
                else:
                    self.status=Status(Constants.status_id7,Constants.status_message7)
                    return self.status
        except Exception as e:
            self.status=Status(Constants.status_id2,Constants.status_message2)  
        return self.status

    def getAllCategories(self):
        cursor = self.con.cursor()
        sql = "SELECT category FROM category;"
        cursor.execute(sql)
        return cursor.fetchone()




# db = dbConfig()
# Cat = Category(db.con)
# S = Cat.AddCategory(["maths","arithmatic"])
# # print(Cat.GetCategoryId("mystery"))
# S = Cat.AddBookCategory(52,["maths","arithmatic"])
# if(S.statusId == 0):
#     db.commit()
# else:
#     db.rollback()

