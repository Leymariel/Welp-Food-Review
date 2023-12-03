from .db_operations import db_operations
class User:
    def __init__(self, username, password, email, p_picture = None, id = None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
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

    def checkPassword(self, password):
        return self.password == password
    
    def getID(self):
        return self.id

    def createNew(self):
        db_ops = db_operations()
        query = f"INSERT INTO Users (Username, Password, Email) VALUES ('{self.username}', '{self.password}', '{self.email}');"
        db_ops.send_query(query)