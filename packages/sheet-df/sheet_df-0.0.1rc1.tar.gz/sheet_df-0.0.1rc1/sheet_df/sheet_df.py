import pickle
import os
import os.path

import pandas as pd
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()


def read_google_sheet_into_dataframe(sheet_id, range_name):
    creds = None
    token_path = "token.pickle"
    credentials_path = "credentials.json"

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                ["https://www.googleapis.com/auth/spreadsheets.readonly"],
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])

    if not values:
        print("No data found in the Google Sheet.")
        return None

    df = pd.DataFrame(values[1:], columns=values[0])
    return df


if __name__ == "__main__":
    sheet_id = os.environ.get("SHEET_ID")
    range_name = os.environ.get("RANGE_NAME")
    df = read_google_sheet_into_dataframe(sheet_id, range_name)
    print(df)
