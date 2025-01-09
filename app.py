from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from datetime import timedelta
from auth_routes import auth_bp
import os

app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/auth_system'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Google OAuth config
app.config['GOOGLE_CLIENT_ID'] = os.getenv("CLIENT_ID")
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv("CLIENT_SECRET")
app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'

# Initialize extensions
mongo = PyMongo(app)

def get_mongo():
    return mongo

jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)