from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os

from routes import main_routes, user_routes, meeting_routes

# Load the environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    # Register the blueprints
    app.register_blueprint(main_routes.main_routes_bp)
    app.register_blueprint(user_routes.user_routes_bp)
    app.register_blueprint(meeting_routes.meeting_routes_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()

    # get host and port from environment variables
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    APP_ID = os.getenv('APP_ID')


    # Run the app
    app.run(debug=True, host=host , port=port)


import webbrowser
from msal import PublicClientApplication

# Replace with your actual application ID and required permissions
app_id = '03fa8ff7-455c-4637-8a1c-c41bb55fa189'
SCOPES = ['OnlineMeetings.ReadWrite', 'OnlineMeetingTranscript.Read.All', 'Calendars.ReadWrite']

# Create a PublicClientApplication instance
client = PublicClientApplication(client_id=app_id)

# Start device flow for authentication
flow = client.initiate_device_flow(scopes=SCOPES)
print("User code: ", flow["user_code"])

# Open the verification URI in the browser for the user to authenticate
webbrowser.open(flow['verification_uri'])

# Wait for the user to authenticate and acquire the access token
token_response = client.acquire_token_by_device_flow(flow)

# Check if the token was acquired successfully
if 'access_token' in token_response:
    access_token = token_response['access_token']
    print("Access token: ", access_token)
else:
    print("Failed to acquire access token.")
    print("Error:", token_response.get('error'))
    print("Error description:", token_response.get('error_description'))

