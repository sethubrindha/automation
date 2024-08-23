import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def uploadYtvid(VIDEO_FILE_NAME='',
                title='',
                description=''):
    print("inside upload video yt >>>..")
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    request_body = {
        'snippet': {
            'categoryI': 19,
            'title': title,
            'description': description,
            'tags': ['Travel', 'video test', 'Travel Tips']
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(VIDEO_FILE_NAME)
    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    print("upload_sucessfull >>>>>")

# service.thumbnails().set(
#     videoId=response_upload.get('id'),
#     media_body=MediaFileUpload('thumbnail.png')
# ).execute()

# uploadYtvid(VIDEO_FILE_NAME='', title='test', description='test')