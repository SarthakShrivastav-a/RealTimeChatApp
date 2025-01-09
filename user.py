from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, password, user_id=None, created_at=None):
        self.username = username
        self.password = password
        self.id = ObjectId(user_id) if user_id else ObjectId()
        self.created_at = created_at or datetime.utcnow()

    @staticmethod
    def from_db_object(db_user):
        if db_user is None:
            return None
        return User(
            username=db_user['username'],
            password=db_user['password'],
            user_id=str(db_user['_id']),
            created_at=db_user['created_at']
        )

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }