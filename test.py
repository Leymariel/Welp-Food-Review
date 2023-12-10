from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import io

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def service_account_login():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

@app.route('/upload-to-drive', methods=['POST'])
def upload_to_drive():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        service = service_account_login()
        file_metadata = {'name': file.filename}
        media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return 'File ID: %s' % file.get('id')

if __name__ == '__main__':
    app.run(debug=True)