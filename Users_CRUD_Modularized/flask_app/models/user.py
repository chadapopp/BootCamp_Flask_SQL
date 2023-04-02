from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-A]+$')

class User:
    DB = 'users_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) <= 0:
            flash("First Name Is Required.")
            is_valid = False
        if len(user['last_name']) <= 0:
            flash("Last Name Is Required.")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Email Is Required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalive email address.")
            is_valid = False
        return is_valid
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    @classmethod
    def save(cls, data):
        db = 'users_schema'
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        print(query, data)
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = """UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM users WHERE id = %(id)s;
        """
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query,data)
    