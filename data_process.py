import streamlit as st
import json
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_sheet_data(sheet_names):
    """
    Open Google Sheet by SHEET_ID and load sheets listed in sheet_names.
    Returns a dictionary of DataFrames keyed by sheet name.
    """
    
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    
    # with open('oshit-data-visualization-dd0ed1145527.json', 'r') as f:
    #     sa_json = json.load(f)
    #     print(sa_json)
    #     print(type(sa_json))
    sa_str = st.secrets["google"]["service_account"]
    sa_json = json.loads(sa_str)
    # print(sa_str)
    # print(type(sa_str))
    # sa_json = json.loads(sa_str)
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

def filter_df_by_date(df, date):
    """
    Filter the DataFrame for rows 'Timestamp(UTC+8)' matching the given date.
    """
    filtered_df = df[df['Timestamp(UTC+8)'].dt.date == date]
    return filtered_df

def filter_df_by_date_pos(df, date):
    """
    Filter the POS DataFrame for rows 'Date' matching the given date.
    """
    filtered_df = df[(df['Timestamp(UTC+8)'] + pd.Timedelta(hours=12)).dt.date == date]
    return filtered_df

def num_all_tx_excluding_reference(df):
    """
    Calculate the number of all transactions excluding 'Reference'.
    """
    filtered_df = df[df['TS_Category'] == 0]
    total_tx = filtered_df.shape[0]
    return total_tx

def mean_median_by_address(df):
    """
    Exclude 'Reference' rows, then
    Group by 'Receiver Address' and calculate mean of number of transactions and the median.
    """
    filtered_df = df[df['TS_Category'] == 0]
    grouped = filtered_df.groupby('Receiver Address').size()
    mean_tx = grouped.mean()
    median_tx = grouped.median()
    return mean_tx, median_tx

def avg_time_interval_by_address(df):
    """
    Calculate average time interval between transactions for each address.
    Only include addresses with 5+ transactions on that day.
    Returns the overall average time interval across all valid addresses.
    """
    # 按地址和日期分组
    df_sorted = df.sort_values('Timestamp(UTC+8)')
    
    intervals = []
    
    for address in df['Receiver Address'].unique():
        # 该地址的所有交易
        addr_df = df_sorted[df_sorted['Receiver Address'] == address]
        
        # 只考虑一天内有 5+ 交易的地址
        if len(addr_df) >= 5:
            # 计算相邻两次交易的时间间隔
            timestamps = addr_df['Timestamp(UTC+8)'].values
            for i in range(len(timestamps) - 1):
                interval = (timestamps[i + 1] - timestamps[i]) / pd.Timedelta(minutes=1)  # 转成分钟
                intervals.append(interval)
    
    if len(intervals) == 0:
        return 0
    
    avg_interval = pd.Series(intervals).mean()
    return avg_interval

def num_address_without_reference(df):
    """
    Count the number of unique addresses excluding 'Reference' transactions.
    """
    filtered_df = df[df['TS_Category'] == 0]
    unique_addresses = filtered_df['Receiver Address'].nunique()
    return unique_addresses

def num_lucky_draws(df):
    """
    Count the number of lucky draws (TS_Category == 3).
    """
    lucky_draws = df[df['TS_Category'] == 3].shape[0]
    return lucky_draws

def amount_lucky_draws(df):
    """
    Calculate the total amount of lucky draws (TS_Category == 3).
    """
    lucky_draws = df[df['TS_Category'] == 3]
    return lucky_draws['SHIT Sent'].sum()

def num_address_lucky_draws(df):
    """
    Count the number of unique addresses participating in lucky draws (TS_Category == 3).
    """
    lucky_draws = df[df['TS_Category'] == 3]
    return lucky_draws['Receiver Address'].nunique()

def num_tx_by_reference_level(df):
    """
    Count the number of transactions by reference level.
    """
    TS_2 = df[df['TS_Category'] == 2].shape[0]
    TS_1 = df[df['TS_Category'] == 1].shape[0] - TS_2
    TS_0 = df[df['TS_Category'] == 0].shape[0] - TS_1 - TS_2
    return TS_0, TS_1, TS_2

def count_addresses_by_tx_count(df, min_tx_count=1):
    """
    Count the number of addresses with transaction count > min_tx_count.
    """
    # 按地址分组，计算每个地址的交易次数
    address_tx_count = df.groupby('Receiver Address').size()
    
    # 统计交易次数 > min_tx_count 的地址数
    result = (address_tx_count > min_tx_count).sum()
    result_df = address_tx_count[address_tx_count > min_tx_count].reset_index()
    result_df.columns = ['Receiver Address', 'Transaction Count']
    return result, result_df

def address_repeat_rate_vs_yesterday(full_df, selected_date):
    """
    Calculate address repeat rate: (addresses in selected_date AND yesterday) / (addresses in yesterday)
    Returns repeat_rate (0-1)
    """
    from datetime import timedelta
    
    yesterday = selected_date - timedelta(days=1)
    
    # 获取昨天和当天的数据
    df_today = full_df[full_df['Timestamp(UTC+8)'].dt.date == selected_date]
    df_yesterday = full_df[full_df['Timestamp(UTC+8)'].dt.date == yesterday]
    
    if len(df_yesterday) == 0:
        return 0
    
    # 获取地址集合
    today_addresses = set(df_today['Receiver Address'].unique())
    yesterday_addresses = set(df_yesterday['Receiver Address'].unique())
    
    # 计算重复地址（交集）
    repeat_addresses = today_addresses & yesterday_addresses
    
    # 重复率 = 重复地址数 / 昨天地址数
    repeat_rate = len(repeat_addresses) / len(yesterday_addresses) if len(yesterday_addresses) > 0 else 0
    
    return repeat_rate

def repeat_claim_rate_and_ranking(full_df, selected_date):
    """
    Exclude 'Reference' rows, then
    Calculate ranking of addresses by claim count in past 7 days.
    Only show addresses that appear on selected_date.
    Returns: ranking DataFrame with columns [Receiver Address, 过去7天领取次数]
    """
    from datetime import timedelta
    
    # 只考虑非 Reference 的数据
    full_df_filtered = full_df[full_df['TS_Category'] == 0]
    
    # 获取过去 7 天的日期范围
    start_date = selected_date - timedelta(days=6)
    end_date = selected_date
    
    # 过滤过去 7 天的数据
    df_7days = full_df_filtered[
        (full_df_filtered['Timestamp(UTC+8)'].dt.date >= start_date) & 
        (full_df_filtered['Timestamp(UTC+8)'].dt.date <= end_date)
    ].copy()
    
    # 只看当天的数据
    df_today = full_df_filtered[full_df_filtered['Timestamp(UTC+8)'].dt.date == selected_date].copy()
    
    if len(df_today) == 0:
        return pd.DataFrame()
    
    # 当天出现的地址
    today_addresses = set(df_today['Receiver Address'].unique())
    
    # 过去 7 天每个地址的领取次数
    ranking = df_7days.groupby('Receiver Address').size().reset_index(name='过去7天领取次数')
    
    # ✓ 只保留当天出现的地址
    ranking = ranking[ranking['Receiver Address'].isin(today_addresses)]
    
    # 按过去 7 天领取次数从高到低排序
    ranking = ranking.sort_values('过去7天领取次数', ascending=False).reset_index(drop=True)
    
    # ✓ 只返回排行榜
    return ranking

def shit_price_day(df):
    """
    Calculate the SHIT price on a specific day in SOL.
    """
    if df.empty:
        return 0

    # Calculate the average SHIT price
    shit_price = df['SOL Received']/ (df['SHIT Sent']*0.13)
    return shit_price.mean()
