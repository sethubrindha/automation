import datetime
import time
from Google import Create_Service
from googleapiclient.http import MediaFileUpload, HttpError

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def uploadYtvid(VIDEO_FILE_NAME='', title='', description='', tags=[], retries=3, pickle_file_path=CLIENT_SECRET_FILE):
    print("Inside upload video to YouTube...")
    print('CLIENT_SECRET_FILE :', pickle_file_path)
    service = Create_Service(pickle_file_path, API_NAME, API_VERSION, SCOPES)

    request_body = {
        'snippet': {
            'categoryId': '24',  # Category ID for 'Entertainment'
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

    upload_request = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    )

    response = None
    while response is None:
        try:
            print("Uploading file...")
            status, response = upload_request.next_chunk()
            if 'id' in response:
                print(f"Upload successful! Video ID: {response['id']}")
            else:
                print(f"Unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in [500, 502, 503, 504]:
                print(f"Retryable error occurred: {e}")
                time.sleep(5)
            else:
                print(f"Upload failed with error: {e}")
                break
        except TimeoutError as e:
            print(f"Timeout occurred: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e.args}")
            break
