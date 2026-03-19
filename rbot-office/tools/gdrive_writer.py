"""
FILE: gdrive_writer.py
PURPOSE: Authenticates with the Google Drive API using a headless OAuth refresh token 
         and uploads a dynamically generated text file (Markdown) directly into a 
         secure, hardcoded Google Drive folder.
INPUTS:  title (str): The name of the file to create (e.g., 'architecture_doc.md')
         content (str): The actual text content to write inside the file
OUTPUTS: str: A success message containing the Google Drive File ID, or an error message.
"""

import os
import io

# We import the specific classes needed for Google authentication and API execution.
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

def save_to_drive(title: str, content: str) -> str:
    """
    Creates a new text document in the specified Google Drive folder.
    """
    
    # 1. RETRIEVE SECRETS FROM ENVIRONMENT
    # os.getenv() safely reads variables from our .env file. If the variable is missing, 
    # it returns 'None' instead of crashing the program.
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    folder_id = os.getenv("ROSS_BRAIN_FOLDER_ID")

    # Security check: Ensure we actually have all the keys before attempting to connect.
    if not all([client_id, client_secret, refresh_token, folder_id]):
        return "Error: Missing Google Drive credentials in the .env file."

    try:
        # 2. HEADLESS AUTHENTICATION
        # Instead of opening a web browser to log in, we construct a 'Credentials' object 
        # using the refresh token we generated earlier. The Google library will automatically 
        # use this to fetch a temporary, 1-hour access token in the background.
        creds = Credentials(
            token=None,                  # We don't have an active token right now...
            refresh_token=refresh_token, # ...but we have the master key to get a new one.
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token" # The Google server that hands out tokens
        )

        # 3. BUILD THE API SERVICE
        # The 'build' function constructs the specific API client we want. 
        # 'drive' is the API name, 'v3' is the version, and we pass our credentials.
        service = build('drive', 'v3', credentials=creds)

        # 4. PREPARE THE FILE METADATA
        # A dictionary (JSON object) telling Google the name of the file and exactly 
        # which folder to put it in. We pass the folder_id inside a list because 
        # Google allows a file to live in multiple folders at once.
        file_metadata = {
            'name': title,
            'parents':[folder_id] 
        }

        # 5. IN-MEMORY FILE HANDLING
        # Normally, you read a file from a hard drive. But our AI generated the 'content' 
        # as a string in RAM. We use 'io.BytesIO()' to trick Google into thinking 
        # our string is an actual physical file. 
        # We must `.encode('utf-8')` to turn the Python string into raw bytes.
        file_buffer = io.BytesIO(content.encode('utf-8'))
        
        # We wrap our fake file in a MediaIoBaseUpload object so the Google API can stream it.
        # mimetype='text/markdown' tells Google Drive exactly what kind of text this is.
        media = MediaIoBaseUpload(file_buffer, mimetype='text/markdown', resumable=True)

        # 6. EXECUTE THE UPLOAD
        # We call files().create(), pass our metadata and our fake file, and execute the HTTP request.
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        # If successful, Google returns a dictionary containing the new file's unique ID.
        file_id = file.get('id')
        return f"Success: File '{title}' has been securely saved to the 'rbot' Google Drive folder (ID: {file_id})."

    except Exception as e:
        # If anything goes wrong (e.g., bad token, no internet), we catch the Exception 
        # and return it as a string so the AI can read the error and tell you in Slack.
        return f"Failed to write to Google Drive: {str(e)}"
