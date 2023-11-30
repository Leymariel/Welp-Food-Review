from .db_operations import db_operations
class Business:
    def __init__(self, businessName, address, phone, password, email, description):
        self.businessName = businessName
        self.address = address
        self.phone = phone
        self.password = password
        self.email = email
        self.description = description

    @staticmethod
    def getBusinessByEmail(email):
        db_ops = db_operations()
        if not db_ops.exists("Businesses", "Email", email):
            return None
    
        user_row = db_ops.get_row("Businesses", "Email", email)
        return user_row

    def checkPassword(self, password):
        return self.password == password
    
    
    def createNew(self):
        db_ops = db_operations()
        query = f"INSERT INTO Businesses (BusinessName, Address, Phone, Password, Email, Description) VALUES ('{self.businessName}', '{self.address}', '{self.phone}', '{self.password}', '{self.email}', '{self.description}');"
        db_ops.send_query(query)