from flask import Blueprint, jsonify, request
from db.user_queries import create_user, get_user_by_username
import hashlib

user_routes_bp = Blueprint('user_routes', __name__, url_prefix='/user')

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register Route
@user_routes_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check for existing user
    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    # Create a new user
    hashed_pwd = hash_password(password)
    new_user = create_user(username, hashed_pwd)

    return jsonify({
        'message': f'User {new_user[1]} registered successfully',
        'user_id': new_user[0]
    }), 201

# Login Route
@user_routes_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    hashed_pwd = hash_password(password)
    if hashed_pwd != user[2]:
        return jsonify({'error': 'Invalid username or password'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user[0]}), 200
