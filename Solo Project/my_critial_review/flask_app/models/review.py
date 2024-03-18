from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Review:

    DB = "my_critical_review"

    def __init__(self, data):

        self.id = data ['id']
        self.tittle = data ['tittle']
        self.media = data ['media']
        self.rating = data ['rating']
        self.comments = data ['comments']
        self.created_at = data ['created_at']

        self.owner = None

    @classmethod
    def get_by_id(cls, id):
        query = """SELECT * FROM 
        reviews WHERE 
        reviews.id = %(id)s;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id":id})
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM 
        reviews LEFT JOIN 
        users ON users.id = reviews.user_id """
        results = MySQLConnection(cls.DB).query_db(query)

        all = []
        for row in results:
            review = cls(row)
            review.owner = User({
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
            })
            all.append(review)
        return all
    
    @classmethod
    def get_all_by_id(cls, id):
        query = """ SELECT * FROM reviews 
        LEFT JOIN users ON users.id = reviews.user_id 
        WHERE reviews.id = %(id)s;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id":id})

        all = []
        for row in results:
            print(row)
            review = cls(row)
            review.owner = User({
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
            })
            all.append(review)
        return all


    @classmethod
    def add(cls,data):
        query = """INSERT INTO 
        reviews (tittle, media, rating, comments, user_id) 
        VALUES (%(tittle)s, %(media)s, %(rating)s, %(comments)s, %(user_id)s)"""
        results = MySQLConnection(cls.DB).query_db(query,data)
        if not results:
            flash("Could not add rating")
        return results
    
    @classmethod
    def edit(cls,data):
        query = """UPDATE reviews SET 
            tittle = %(tittle)s, 
            media = %(media)s, 
            rating = %(rating)s, 
            comments = %(comments)s
            WHERE reviews.id = %(id)s;"""
        return MySQLConnection(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM 
        reviews WHERE 
        id=%(id)s;"""
        return MySQLConnection(cls.DB).query_db(query, {"id":id})

    @staticmethod
    def validate(data):
        is_valid = True

        if data['tittle'] == "":
            flash("A tittle needs to be entered.")
            is_valid = False

        if data['media'] == "":
            flash("The media needs to be entered.")
            is_valid = False

        if data['rating'] == "":
            flash("Need to enter a rating between 1 and 5.")
            is_valid = False
        elif int(data['rating']) < 1 or int(data['rating']) >5:
            flash("The rating must be between 1 and 5.")
            is_valid = False

        if data['comments'] == "":
            flash("Please add your comments for the tittle.")
            is_valid = False
        elif len(data['comments']) > 75:
            flash("Comments cannot be longer than 75 digits.")
            is_valid = False

        return is_valid