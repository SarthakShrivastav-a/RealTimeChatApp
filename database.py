from flask import current_app
from datetime import datetime
from bson import ObjectId

def insert_user(username, hashed_password):
    user = {
        'username': username,
        'password': hashed_password,
        'created_at': datetime.utcnow()
    }
    return current_app.mongo.db.users.insert_one(user)

def find_user_by_username(username):
    return current_app.mongo.db.users.find_one({'username': username})

def find_user_by_id(user_id):
    return current_app.mongo.db.users.find_one({'_id': ObjectId(user_id)})