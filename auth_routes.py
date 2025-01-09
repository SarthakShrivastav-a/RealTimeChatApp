from flask import Blueprint, request, jsonify, url_for, redirect, current_app
from auth_service import AuthService
from google_auth_oauthlib.flow import Flow
import os

auth_bp = Blueprint('auth', __name__)

# Create a Flow object for Google OAuth
def create_google_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": current_app.config['GOOGLE_CLIENT_ID'],
                "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5000/auth/google/callback"]
            }
        },
        scopes=['openid', 'email', 'profile']
    )

@auth_bp.route('/google')
def google_login():
    flow = create_google_flow()
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)

@auth_bp.route('/google/callback')
def google_callback():
    flow = create_google_flow()
    
    # Get authorization code from the callback request
    code = request.args.get('code')
    flow.fetch_token(code=code)

    # Get user info from Google
    credentials = flow.credentials
    id_token = credentials.id_token
    user_info = AuthService.verify_google_token(id_token)

    if not user_info:
        return jsonify({'error': 'Failed to verify Google token'}), 400

    # Handle Google login
    success, result = AuthService.handle_google_login(user_info)
    if success:
        return jsonify(result), 200
    return jsonify({'error': result}), 400

# Keep existing routes
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    success, message = AuthService.register(username, password)
    if success:
        return jsonify({'message': message}), 201
    return jsonify({'error': message}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    success, result = AuthService.login(username, password)
    if success:
        return jsonify({'token': result['token']}), 200
    return jsonify({'error': result}), 401