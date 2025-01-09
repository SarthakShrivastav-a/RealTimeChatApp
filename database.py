from flask import current_app
from datetime import datetime
from bson import ObjectId
import app

def get_db():
    return app.get_mongo().db

def insert_user(username, hashed_password):
    user = {
        'username': username,
        'password': hashed_password,
        'created_at': datetime.utcnow(),
        'auth_type': 'local'
    }
    return get_db().users.insert_one(user)

def insert_google_user(email, google_id, name):
    user = {
        'email': email,
        'google_id': google_id,
        'name': name,
        'created_at': datetime.utcnow(),
        'auth_type': 'google'
    }
    return get_db().users.insert_one(user)

def find_user_by_google_id(google_id):
    return get_db().users.find_one({'google_id': google_id})

def find_user_by_email(email):
    return get_db().users.find_one({'email': email})