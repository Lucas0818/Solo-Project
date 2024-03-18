import re
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    DB = "my_critical_review"

    def __init__(self, data):

        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']


    @classmethod
    def create(cls,data):
        query = """INSERT INTO 
        users (first_name, last_name, email, password) 
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"""
        return MySQLConnection(cls.DB).query_db(query, data)


    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = MySQLConnection(cls.DB).query_db(query, {"email":email})
        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def get_by_id(cls, id):
        query = """SELECT * FROM 
        users WHERE 
        users.id = %(id)s;"""
        results = MySQLConnection(cls.DB).query_db(query, {"id":id})
        if results:
            return cls(results[0])
        else:
            return False


    @staticmethod
    def validate_new_user(data):
        is_valid = True
        
        if len(data["first_name"]) < 2:
            flash("First name must have atleast 2 digits")
            is_valid = False

        if len(data["last_name"]) < 2:
            flash("Last name must have atleast 2 digits")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email format")
            is_valid = False

        elif User.get_by_email(data["email"]):
            flash("Email already in use")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Password and Confirm Password do not match.")
            is_valid = False

        return is_valid