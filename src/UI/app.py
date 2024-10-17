from src.Beans.Member import Member
from src.Business_Logic.MemberBL import MemberBL

m1 = Member("Aditya Natarajan", "8861343874", "abcd1234", "2nd main Ranganathpura",
            "Kamakshipalya", "Bangalore", "Karnataka",
            "560079", "Science", "Fiction", "Novel")

q = MemberBL()
print(q.addMember(m1).message)
print(q.addMember(m1).statusId)


