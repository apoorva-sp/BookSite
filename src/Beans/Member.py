class Member:

    def __init__(self, name: str, phone: str, password: str, addressline1: str, addressline2: str, city: str,
                 state: str, pincode: str, preference1: str,
                 preference2: str, preference3: str):
        self.name = name
        self.phone = phone
        self.password = password
        self.addressLine1 = addressline1
        self.addressLine2 = addressline2
        self.city = city
        self.pincode = pincode
        self.state = state
        self.preference1 = preference1
        self.preference2 = preference2
        self.preference3 = preference3

    def display(self):
        print(f"name {self.name}")
        print(f"phone {self.phone}")
        print(f"password {self.password}")
        print(f"addressline 1 {self.addressLine1}")
        print(f"addressline 2 {self.addressLine2}")
        print(f"city {self.city}")
        print(f"state {self.state}")
        print(f"pincode {self.pincode}")
        print(f"preference1 {self.preference1}")
        print(f"preference2 {self.preference2}")
        print(f"preference3 {self.preference3}")
