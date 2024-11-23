from src.Beans.Member import Member
from src.Beans.Status import Status
from src.Database.Constants import Constants
from src.Database.MembersDB import MemberDB
from src.Database.dbconfig import dbConfig


class MemberBL:

    def __init__(self):
        self.status = Status()
        self.db = dbConfig()
        self.mdb = MemberDB(self.db.con)

    def signUp(self, m1: Member) -> Status:
        if len(m1.phone) != 10:
            self.status = Status(Constants.status_id57, Constants.status_message57)
        elif m1.preference1 == "":
            self.status = Status(Constants.status_id58, Constants.status_message58)
        else:
            self.status = self.mdb.insert_member(m1)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status

    def update_preference(self, phone: str, preference1: str, preference2: str, preference3: str) -> Status:
        if preference1 == "":
            self.status = Status(Constants.status_id58, Constants.status_message58)
        elif preference2 == preference1 or preference1 == preference3 or preference2 == preference3:
            self.status = Status(Constants.status_id59, Constants.status_message59)
        else:
            self.status = self.mdb.update_preference(phone, preference1, preference2, preference3)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status

    def update_address(self, phone_number: str, address_line_one: str, address_line_two: str, city: str, state: str,
                       pincode: str) -> Status:
        if address_line_one == "" or state == "" or city == "" or pincode == "":
            self.status = Status(Constants.status_id60, Constants.status_message60)
        else:
            self.status = self.mdb.update_address(phone_number, address_line_one, address_line_two, city, state,
                                                  pincode)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status

    def update_password(self, new_password: str, old_password: str, phone: str) -> Status:
        if old_password == new_password:
            self.status = Status(Constants.status_id61, Constants.status_message61)
        elif new_password == "":
            self.status = Status(Constants.status_id62, Constants.status_message62)
        else:
            self.status = self.mdb.update_password(phone, new_password)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status

    def update_number(self, new_phone: str, old_phone: str) -> Status:
        if old_phone == new_phone:
            self.status = Status(Constants.status_id63, Constants.status_message63)
        elif len(new_phone) != 10:
            self.status = Status(Constants.status_id64, Constants.status_message64)
        else:
            self.status = self.mdb.update_number(old_phone, new_phone)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status

    def update_name(self, phone: str, new_name: str) -> Status:
        if new_name == "":
            self.status = Status(Constants.status_id65, Constants.status_message65)
        else:
            self.status = self.mdb.update_name(phone, new_name)

        if self.status.statusId == 0:
            self.db.commit()
        else:
            self.db.rollback()

        return self.status


    def login(self,number:str,password:str):
        if len(number) != 10 or len(password)<8:
            self.status = Status(2000,"ENTER NAME AND PASSWORD OF ATLEAST 8 CHARACTERS")
            print(self.status)
            return False
        else:
            return self.mdb.login(number,password)

    def getpreferences(self,number:str):
        data = self.mdb.getInfo(number)
        return [data[-3],data[-2],data[-1]]
    def get_mid(self,phone:str):
        data = self.mdb.get_mid(phone)
        return data

    def get_info(self,phone:str):
        data = self.mdb.getInfo(phone)
        return data
# m=Member( 'John Doe','1234567890', 'securepassword123', '123 Main St', 'Apt 4B', 'New York', 'NY', '10001', 'Fiction', 'Non-Fiction', 'Science Fiction')
# m1=Member( 'Ramsey','1234567891', 'abcd1234', '123 Main St', 'Apt 4A', 'Texas', 'Texas', '10001', 'Fiction', 'Non-Fiction', 'Science')
# mbl=MemberBL()
# print(mbl.add_member(m1))
# print(mbl.login("1234567890","securepassword123"))
