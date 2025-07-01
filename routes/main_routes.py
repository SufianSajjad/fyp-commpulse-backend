from flask import Blueprint, jsonify

# Create a blueprint for the main routes
main_routes_bp = Blueprint('main_routes', __name__)

@main_routes_bp.route('/', methods=['GET'])
def welcome():
    return jsonify({'message': 'Welcome to the CommPulse API'})
