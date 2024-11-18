import mysql.connector
from hashlib import md5
from src.Beans.Member import Member
from src.Beans.Status import Status
from src.Database.Constants import Constants
from src.Database.dbconfig import dbConfig


class MemberDB:

    def __init__(self, con: mysql.connector.connect()):
        self.con = con
        self.status = Status()

    def insert_member(self, m: Member) -> Status:
        try:
            cursor = self.con.cursor()
            sql = ("INSERT INTO MEMBERS (phone,fullname,password,address_line_one,address_line_two,city," +
                   "state,pincode,preferenceOne,preferenceTwo,preferenceThree)" +
                   "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")
            password = md5(m.password.encode())
            values = (
                m.phone, m.name, password.hexdigest(), m.addressLine1, m.addressLine2, m.city, m.state,
                m.pincode, m.preference1, m.preference2, m.preference3)
            cursor.execute(sql, values)

        except Exception as e:
            self.status = Status(Constants.status_id51, Constants.status_message51)
            print(e)
        return self.status

    def update_preference(self, phone_number: str, preference_one: str, preference_two: str, preference_three: str):
        try:
            cursor = self.con.cursor()
            sql = ("UPDATE MEMBERS SET preferenceOne = (%s),preferenceTwo = (%s),preferenceThree = (%s)" +
                   " WHERE phone = (%s);")
            values = (preference_one, preference_two, preference_three, phone_number)
            cursor.execute(sql, values)
        except Exception as e:
            self.status = Status(Constants.status_id52, Constants.status_message52)
            print(e)
        return self.status

    def update_name(self, phone_number: str, new_name: str):
        try:
            cursor = self.con.cursor()
            sql = "UPDATE MEMBERS SET fullname = (%s) WHERE phone = (%s);"
            values = (new_name, phone_number)
            cursor.execute(sql, values)
        except Exception as e:
            self.status = Status(Constants.status_id53, Constants.status_message53)
            print(e)
        return self.status

    def update_password(self, phone_number: str, new_password: str):
        try:
            cursor = self.con.cursor()
            sql = "UPDATE MEMBERS SET password = (%s) WHERE phone = (%s);"
            password = md5(new_password.encode())
            values = (password.hexdigest(), phone_number)
            cursor.execute(sql, values)
        except Exception as e:
            self.status = Status(Constants.status_id54, Constants.status_message54)
            print(e)
        return self.status

    def update_address(self, phone_number: str, address_line_one: str, address_line_two: str, city: str, state: str,
                       pincode: str):
        try:
            cursor = self.con.cursor()
            sql = ("UPDATE MEMBERS SET address_line_one = (%s), address_line_two = (%s), city = (%s)" +
                   "state = (%s), pincode = (%s) WHERE phone = (%s);")
            values = (address_line_one, address_line_two, city, state, pincode, phone_number)
            cursor.execute(sql, values)
        except Exception as e:
            self.status = Status(Constants.status_id55, Constants.status_message55)
            print(e)
        return self.status

    def update_number(self, old_number: str, new_number: str):
        try:
            cursor = self.con.cursor()
            sql = "UPDATE MEMBERS SET phone = (%s) where phone = (%s);"
            cursor.execute(sql, (new_number, old_number))
        except Exception as e:
            print(e)
            self.status = Status(Constants.status_id56, Constants.status_message56)
            print(e)
        return self.status

    def login(self,number:str,password:str)->bool:
        try:
            hashed = md5(password.encode()).hexdigest()
            cursor = self.con.cursor()
            sql = """SELECT * FROM members WHERE phone = %s AND passkey = %s"""
            cursor.execute(sql,(number,hashed))
            return len(cursor.fetchall()) == 1
        except Exception as e:
            print(e)
            return False

    def getInfo(self,phone:str):
        cursor = self.con.cursor()
        sql = "SELECT * FROM members where phone = %s"
        cursor.execute(sql,(phone,))
        return cursor.fetchone()
    def get_mid(self,phone:str):
        cursor = self.con.cursor()
        sql = "select mID from members where phone = %s"
        cursor.execute(sql,(phone,))
        return cursor.fetchone()
# d = dbConfig()
# mdb = MemberDB(d.con)
# print(mdb.login("1234567890","securepassword123"))
# d.commit()