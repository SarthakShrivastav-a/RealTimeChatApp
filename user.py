# user.py
from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, 
                 username=None, 
                 password=None, 
                 email=None,
                 google_id=None,
                 name=None,
                 user_id=None, 
                 created_at=None,
                 auth_type='local'):
        self.username = username
        self.password = password
        self.email = email
        self.google_id = google_id
        self.name = name
        self.id = ObjectId(user_id) if user_id else ObjectId()
        self.created_at = created_at or datetime.utcnow()
        self.auth_type = auth_type

    @staticmethod
    def from_db_object(db_user):
        if db_user is None:
            return None
        
        return User(
            username=db_user.get('username'),
            password=db_user.get('password'),
            email=db_user.get('email'),
            google_id=db_user.get('google_id'),
            name=db_user.get('name'),
            user_id=str(db_user['_id']),
            created_at=db_user['created_at'],
            auth_type=db_user.get('auth_type', 'local')
        )

    def to_dict(self):
        user_dict = {
            'created_at': self.created_at,
            'auth_type': self.auth_type
        }
        
        # Add traditional auth fields
        if self.username:
            user_dict['username'] = self.username
        if self.password:
            user_dict['password'] = self.password
            
        # Add Google auth fields
        if self.email:
            user_dict['email'] = self.email
        if self.google_id:
            user_dict['google_id'] = self.google_id
        if self.name:
            user_dict['name'] = self.name
            
        return user_dict

    def is_google_user(self):
        return self.auth_type == 'google'

    def get_identifier(self):
        """Returns the primary identifier for the user (email for Google users, username for local users)"""
        return self.email if self.is_google_user() else self.username