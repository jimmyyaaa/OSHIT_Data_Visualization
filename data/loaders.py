import json
import streamlit as st
import gspread
import pandas as pd
import logging
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

@st.cache_data
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

    OPERATIONAL_SHEET_ID = st.secrets["google"]["operational_sheet_id"]
    op_sh = gc.open_by_key(OPERATIONAL_SHEET_ID)
    DEFI_SHEET_ID = st.secrets["google"]["defi_sheet_id"]
    df_sh = gc.open_by_key(DEFI_SHEET_ID)

    result = {}
    for i, sheet_name in enumerate(sheet_names):
        # 前5个表从operational sheet加载，最后一个表从defi sheet加载
        if i < 5:
            ws = op_sh.worksheet(sheet_name)
        else:
            ws = df_sh.worksheet(sheet_name)
            
        records = ws.get_all_records()
        df = pd.DataFrame(records)
        # 转换日期列
        if 'Timestamp(UTC+8)' in df.columns:
            df['Timestamp(UTC+8)'] = pd.to_datetime(df['Timestamp(UTC+8)'])

        result[sheet_name] = df
        logger.info(f"Loaded sheet: {sheet_name} from {'operational' if i < 5 else 'defi'} sheet")

    return result
