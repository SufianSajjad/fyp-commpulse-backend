import os
from flask import Blueprint, request, jsonify
import requests
from msal import PublicClientApplication

# Environment variables
APP_ID = os.getenv('APP_ID')  # Add APP_ID to your .env file
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# In-memory storage for meetings (convert this to a DB table later)
meetings = []

# Blueprint
meeting_routes_bp = Blueprint('meeting_routes', __name__, url_prefix='/meeting')

# MSAL app instance
msal_app = PublicClientApplication(client_id=APP_ID)

# Route to create a meeting
@meeting_routes_bp.route('/create', methods=['POST'])
def create_meeting():
    try:
        # Extract access token from the request header
        access_token = request.headers.get('Authorization')

        if not access_token:
            return jsonify({'error': 'Access token is required'}), 400

        # Remove 'Bearer ' prefix from token if it exists
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]

        # Set request headers for creating the meeting
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # Meeting details (you can dynamically add more details as per the user)
        meeting_body = {
            "subject": "New API Meeting",
            "startDateTime": "2024-11-12T12:00:00Z",
            "endDateTime": "2024-11-12T13:00:00Z",
            "participants": {
                "attendees": [
                    {
                        "identity": {
                            "user": {
                                "id": "24876d41-668b-44ba-b4cb-8fc92e25514d"  # Replace with actual user ID
                            }
                        }
                    }
                ]
            },
            "isOnlineMeeting": True,
            "onlineMeetingProvider": "teamsForBusiness"  # Required for Teams meetings
        }

        # Make the API call to create the meeting
        response = requests.post(
            GRAPH_ENDPOINT + '/me/onlineMeetings',
            headers=headers,
            json=meeting_body
        )

        if response.status_code == 201:
            meeting_data = response.json()

            # Store meeting properties in the in-memory list
            meetings.append({
                "id": meeting_data["id"],
                "subject": meeting_data["subject"],
                "start_time": meeting_data["startDateTime"],
                "end_time": meeting_data["endDateTime"],
                "join_url": meeting_data["joinUrl"],
            })

            # Return the meeting link
            return jsonify({
                "message": "Meeting created successfully",
                "join_url": meeting_data["joinUrl"]
            }), 201
        else:
            return jsonify({
                "error": "Failed to create meeting",
                "details": response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500