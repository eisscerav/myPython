from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SAMPLE_SPREADSHEET_ID = r'1DKiKX6T9hnK0mZ6SRNNUlTC9x7KM-cI7hOisbhWQf4o'
SAMPLE_RANGE_NAME = 'A1:E1'

def demo():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive.file']
    creds = Credentials.from_authorized_user_file('data/credential.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    print('done demo')


def main():
    demo()


if __name__ == '__main__':
    main()
