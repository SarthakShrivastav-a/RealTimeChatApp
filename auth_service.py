import bcrypt
from database import insert_user, find_user_by_username
from user import User
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register(username, password):
        if find_user_by_username(username):
            return False, "Username already exists"
        
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Create new user
        user_id = insert_user(username, hashed_password)
        return True, "User registered successfully"

    @staticmethod
    def login(username, password):
        user_data = find_user_by_username(username)
        if not user_data:
            return False, "Invalid username or password"

        user = User.from_db_object(user_data)
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return False, "Invalid username or password"

        # Generate token
        access_token = create_access_token(identity=str(user.id))
        return True, {'token': access_token}