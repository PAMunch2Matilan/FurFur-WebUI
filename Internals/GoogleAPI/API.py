# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from Utilities import constant as const


def check_token_api_file():
    if os.path.exists("Resources\\credentials.json"):
        return True

    else:
        return False
        pass


class DriveAPI:
    global SCOPES

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):

        # Variable self.creds will
        # store the user access token.
        # If no valid token found
        # we will create one.
        self.creds = None

        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.

        # Check if file token.pickle exists
        if os.path.exists('Resources/token.json'):
            # Read the token from the file and
            # store it in the variable self.creds
            with open('Resources/token.json', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        if not self.creds or not self.creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'Resources/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open('Resources/token.json', 'wb') as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds, static_discovery=False)

    def get_file_id_by_name(self, name):
        id_list = []

        results = self.service.files().list(
            pageSize=1000, fields="files(id, name)").execute()
        items = results.get('files', [])

        for i in items:
            id_list.append(i["id"])

            if name == i["name"]:
                return i["id"]

    def download_file(self, file_name):
        file_id = self.get_file_id_by_name(file_name)

        if file_id is not None:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()

            # Initialise a downloader object to download the file
            downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
            done = False

            try:
                # Download the data in chunks
                while not done:
                    status, done = downloader.next_chunk()

                fh.seek(0)

                # Write the received data to the file
                with open(const.DOWNLOAD_FOLDER + file_name, 'wb') as f:
                    shutil.copyfileobj(fh, f)

                const.success_message("File Successfully downloaded")
                # Return True if file Downloaded successfully
                return True

            except Exception as e:
                # Return False if something went wrong
                const.error_exception("Error: ", e)
                return False
        else:
            const.error_message("Error: File Not Found")

    def upload_file(self, filepath):

        # Extract the file name out of the file path
        name = filepath.split('/')[-1]

        # Find the MimeType of the file
        mimetype = MimeTypes().guess_type(name)[0]

        # create file metadata
        file_metadata = {'name': name}

        media = MediaFileUpload(filepath, mimetype=mimetype)

        # Create a new file in the Drive storage
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()


if __name__ == "__main__":
    obj = DriveAPI()