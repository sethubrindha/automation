import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def Create_Service(client_secret_file, api_name, api_version, scopes):
    pickle_file = f'token_{api_name}_{api_version}.pickle'
    credentials = None

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            credentials = flow.run_local_server(port=0)

        with open(pickle_file, 'wb') as token:
            pickle.dump(credentials, token)

    return build(api_name, api_version, credentials=credentials)

def uploadYtShort(VIDEO_FILE_NAME='', title='', description='', tags=[]):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    title = title + ' #Shorts'
    
    request_body = {
        'snippet': {
            'categoryId': '22',
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    print(f"YouTube Short uploaded successfully. Video ID: {response_upload.get('id')}")

# # Example usage
# final_video_file = "D:\\sethu\\automation\\meme_shorts\\videos\\final_video.mp4"
# uploadYtShort(
#     VIDEO_FILE_NAME=final_video_file, 
#     title="Tamil Dank Memes: Prepare for Uncontrollable Laughter!", 
#     description='',
#     tags=['#shorts']
# )
