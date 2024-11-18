class Status:
    def __init__(self, statusId=0, message="All good"):
        self.statusId = statusId
        self.message = message

    def __str__(self):
        return f"ID: {self.statusId}\nMSG:{self.message}"