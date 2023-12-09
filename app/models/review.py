from .db_operations import db_operations
from datetime import date


class Review:
    def __init__(self, userID, businessID, score, text):
        self.userID = userID
        self.businessID = businessID
        self.score = score
        self.text = text
        self.date = date.today()

    def addReview(self):
        db_ops = db_operations()
        query = "INSERT INTO Reviews (BusinessID, userID, Rating, ReviewText, ReviewDate) VALUES (%s, %s, %s, %s, %s);"
        params = (self.userID, self.businessID, self.score, self.text, self.date)
        db_ops.send_query(query, params)

     