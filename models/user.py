class User:
    def __init__(self, id, username, password, email, p_picture = None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.p_picture = p_picture
        self.card = {"UserID": id, "Username": username, "Password":password, "Email": email}

    def dump_user(self):
        return self.card