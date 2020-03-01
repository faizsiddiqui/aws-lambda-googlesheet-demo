from __future__ import print_function

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_sheets():
    credentials = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
    return service.spreadsheets()


def read_sheet(sheet_id, sheet_name):
    sheets = get_sheets()
    return sheets.values().get(
        spreadsheetId=sheet_id,
        range='{}!A1:Z'.format(sheet_name)
    ).execute()


def update_sheet(sheet_id, sheet_name, sheet_range, rows):
    sheets = get_sheets()

    # Clear the sheet
    sheets.values().clear(
        spreadsheetId=sheet_id,
        range='{}!A1:Z'.format(sheet_name),
        body={}
    ).execute()

    # Update the sheet
    body = {
        'values': rows
    }
    result = sheets.values().update(
        spreadsheetId=sheet_id,
        range='{}!{}'.format(sheet_name, sheet_range),
        valueInputOption='RAW',
        body=body
    ).execute()
    return '{0} : {1} cells updated'.format(sheet_id, result.get('updatedCells'))
