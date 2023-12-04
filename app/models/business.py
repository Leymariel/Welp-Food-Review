from .db_operations import db_operations
class Business:
    def __init__(self, id, businessName, address, phone, email, description, password, rating=None, website=None, hoursOfOp=None, photo = None):
        self.businessName = businessName
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.description = description
        self.rating = rating

        self.website = website
        self.hoursOfOp = hoursOfOp
        self.photo = photo

    @staticmethod
    def getBusinessByEmail(email):
        db_ops = db_operations()
        if not db_ops.exists("Businesses", "Email", email):
            return None
    
        business_row = db_ops.get_row("Businesses", "Email", email)
        return business_row

    def getPhoto(self):
        return self.photo

    def setPhoto(self, newPhoto):
        db_ops = db_operations()
        query = f"UPDATE Businesses SET BusinessPhoto = {newPhoto} WHERE id = '{self.id}'"
        db_ops.send_query(query)


    def getBusinessByID(ID):
        db_ops = db_operations()
        if not db_ops.exists("Businesses", "BusinessID", ID):
            return None
    
        business_row = db_ops.get_row("Businesses", "BusinessID", ID)
        return business_row

    def checkPassword(self, password):
        return self.password == password
    
    
    def createNew(self):
        db_ops = db_operations()
        query = f"INSERT INTO Businesses (BusinessName, Address, Phone, Password, Email, Description) VALUES ('{self.businessName}', '{self.address}', '{self.phone}', '{self.password}', '{self.email}', '{self.description}');"
        db_ops.send_query(query)

    @staticmethod
    def getAll():
        db_ops = db_operations()
        return db_ops.get_all("Businesses")
    
    @staticmethod
    def search(query):
        db_ops = db_operations()
        # Perform your search logic based on the query using db_ops
        # For example, searching for businesses with a matching name
        search_query = f"SELECT * FROM Businesses WHERE BusinessName LIKE '%{query}%'"
        results = db_ops.get_all_query(search_query)

        return results