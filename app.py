from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from datetime import timedelta
from auth_routes import auth_bp

app = Flask(__name__)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ChatApp'
app.config['JWT_SECRET_KEY'] = 'b877tta76td765dav89db'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)