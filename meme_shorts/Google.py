import pickle
import os
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print("insid create services >>>>>")
    print("scopes >>>>", scopes)
    pickle_file = f'token_{api_name}_{api_version}.pickle'
    print("pickle_file >>>>>", pickle_file)

    credentials = None

    if os.path.exists(pickle_file):
        print("Loading credentials from file...")
        with open(pickle_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing access token...")
            credentials.refresh(Request())
        else:
            print("Fetching new tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            credentials = flow.run_local_server(port=0)

        with open(pickle_file, 'wb') as token:
            print("Saving credentials for future use...")
            pickle.dump(credentials, token)

    service = build(api_name, api_version, credentials=credentials)
    print("youtube service created successfully")
    return service
