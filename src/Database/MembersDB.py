import mysql.connector
from hashlib import md5
from src.Beans.Member import Member
from src.Beans.Status import Status
from src.Database.Constants import Constants

class MemberDB:

    def __init__(self, con: mysql.connector.connect()):
        self.con = con
        self.status = Status()

    def insertMember(self, m: Member) -> Status:
        try:
            cursor = self.con.cursor()
            sql = ("INSERT INTO MEMBERS (phone,fullname,password,addressLineOne,addressLineTwo,city," +
                   "state,pincode,preferenceOne,preferenceTwo,preferenceThree)" +
                   "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            password = md5(m.password.encode())
            values = (
                m.phone, m.name, password.hexdigest(), m.addressLine1, m.addressLine2, m.city, m.state,
                m.pincode, m.preference1, m.preference2, m.preference3)

            cursor.execute(sql, values)

        except Exception as e:
            self.status = Status(Constants.statusId1, Constants.statusMessage1)
            print(e)
        return self.status
