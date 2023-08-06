from time import sleep

import gspread
from gspread.exceptions import APIError
from oauth2client.service_account import ServiceAccountCredentials

from settings import SETTINGS


def retry_req(func: callable, *args):
    sleepy_time = 1
    for _ in range(20):
        sleepy_time *= 2
        try:
            return func(*args)
        except APIError as e:
            res = e.response.json()["error"]
            if "status" in res and res.get("code", None) == 429:
                sleep(15)
                continue
            raise
        except Exception as e:
            print(f"Error in Gsheet with error '{e}'")


def get_spreadsheet_by_url(url) -> gspread.models.Spreadsheet:
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        SETTINGS.GOOGLE_CONFIG, scope
    )
    client = gspread.authorize(creds)
    return retry_req(client.open_by_url, url)


def get_worksheet_from_spreadsheet(
    sheet: gspread.models.Spreadsheet, work_sheet_name: str
) -> gspread.models.Worksheet:
    return retry_req(sheet.worksheet, work_sheet_name)


def bulk_update(sheet, data):
    return retry_req(sheet.update, data)


def update_cell(sheet, row, col, value):
    return retry_req(sheet.update_cell, row, col, value)
