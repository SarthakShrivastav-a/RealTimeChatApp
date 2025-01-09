from flask import Blueprint, request, jsonify
from auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

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