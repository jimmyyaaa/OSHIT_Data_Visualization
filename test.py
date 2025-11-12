import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import json

# Read Sheet Data from Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


with open('oshit-data-visualization-dd0ed1145527.json', 'r') as f:
    sa_json = json.load(f)
sa_info = sa_json
print("Service account info loaded successfully.")
creds = Credentials.from_service_account_info(sa_info, scopes=SCOPES)
gc = gspread.authorize(creds)

SHEET_ID = st.secrets["google"]["sheet_id"]
sh = gc.open_by_key(SHEET_ID)
ws = sh.get_worksheet(0)
records = ws.get_all_records()
df = pd.DataFrame(records)

print("Loaded read-only Google Sheet:")
print(df)

