from .db_operations import db_operations
from datetime import date

class User:
    def __init__(self, id, username, password, email, dateJoined, p_picture):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.dateJoined = dateJoined
        self.p_picture = p_picture
        self.card = {"UserID": id, "Username": username, "Password":password, "Email": email}


    def dump_user(self):
        return self.card
    
    @staticmethod
    def createUser(info):
        return User(info[0], info[1], info[2], info[3])

    @staticmethod
    def getUserByEmail(email):
        db_ops = db_operations()
        if not db_ops.exists("Users", "Email", email):
            return None
    
        user_row = db_ops.get_row("Users", "Email", email)
        return user_row

    @staticmethod
    def getUserByID(ID):
        db_ops = db_operations()
        if not db_ops.exists("Users", "UserID", ID):
            return None
    
        user_row = db_ops.get_row("Users", "UserID", ID)
        return user_row

    def checkPassword(self, password):
        return self.password == password
    
    def getID(self):
        return self.id

    @staticmethod
    def createNew(username, password, email):
        db_ops = db_operations()
        query = f"INSERT INTO Users (Username, Password, Email, DateJoined) VALUES ('{username}', '{password}', '{email}', '{date.today()}');"
        db_ops.send_query(query)