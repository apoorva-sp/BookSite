from src.Beans.Member import Member
from src.Beans.Status import Status
from src.Database.MembersDB import MemberDB
from src.Database.dbconfig import dbConfig

class MemberBL:

    def __init__(self):
        self.status = Status()

    def addMember(self, m1: Member) -> Status:
        db = dbConfig()
        MDB = MemberDB(db.con)

        if (len(m1.name) < 3 or len(m1.name) > 20):
            self.status = Status(2, "Name is too short")
            return self.status
        elif len(m1.phone) != 10:
            self.status = Status(3, "Invalid Phone number")
            return self.status
        else:
            self.status = MDB.insertMember(m1)

        if (self.status.statusId == 0):
            db.commit()
        else:
            db.rollback()

        return self.status
