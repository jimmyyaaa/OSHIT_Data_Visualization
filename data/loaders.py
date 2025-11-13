import json
import streamlit as st
import gspread
import pandas as pd
import logging
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

def load_sheet_data(sheet_names):
    """
    Open Google Sheet by SHEET_ID and load sheets listed in sheet_names.
    Returns a dictionary of DataFrames keyed by sheet name.
    """
    
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    
    sa_str = st.secrets["google"]["service_account"]
    sa_json = json.loads(sa_str)
    creds = Credentials.from_service_account_info(sa_json, scopes=SCOPES)
    gc = gspread.authorize(creds)

    SHEET_ID = st.secrets["google"]["sheet_id"]
    sh = gc.open_by_key(SHEET_ID)
    
    result = {}
    for sheet_name in sheet_names:
        ws = sh.worksheet(sheet_name)
        records = ws.get_all_records()
        df = pd.DataFrame(records)
        # 转换日期列
        if 'Timestamp(UTC+8)' in df.columns:
            df['Timestamp(UTC+8)'] = pd.to_datetime(df['Timestamp(UTC+8)'])

        result[sheet_name] = df
        logger.info(f"Loaded sheet: {sheet_name}")
    
    return result
