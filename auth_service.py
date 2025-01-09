import bcrypt
from database import (
    insert_user, find_user_by_username, insert_google_user,
    find_user_by_google_id, find_user_by_email
)
from user import User
from flask_jwt_extended import create_access_token
from google.oauth2 import id_token
from google.auth.transport import requests
from flask import current_app

class AuthService:
    @staticmethod
    def register(username, password):
        if find_user_by_username(username):
            return False, "Username already exists"
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        user_id = insert_user(username, hashed_password)
        return True, "User registered successfully"

    @staticmethod
    def login(username, password):
        user_data = find_user_by_username(username)
        if not user_data:
            return False, "Invalid username or password"

        user = User.from_db_object(user_data)
        
        if not bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return False, "Invalid username or password"

        access_token = create_access_token(identity=str(user.id))
        return True, {'token': access_token}

    @staticmethod
    def verify_google_token(token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                current_app.config['GOOGLE_CLIENT_ID']
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            return idinfo

        except ValueError:
            return None

    @staticmethod
    def handle_google_login(google_user_data):
        google_id = google_user_data['sub']
        email = google_user_data['email']
        name = google_user_data.get('name', '')

        # Check if user exists
        user = find_user_by_google_id(google_id)
        if not user:
            # Check if email exists but not linked to Google
            email_user = find_user_by_email(email)
            if email_user:
                return False, "Email already exists with different authentication method"
            
            # Create new user
            user_id = insert_google_user(email, google_id, name)
            user = find_user_by_google_id(google_id)

        # Generate token
        access_token = create_access_token(identity=str(user['_id']))
        return True, {'token': access_token, 'user': {'email': email, 'name': name}}
