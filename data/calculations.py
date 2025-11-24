import pandas as pd
import logging

logger = logging.getLogger(__name__)

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
    lucky_draws = df[df['TS_Category'] == 3]
    return lucky_draws.shape[0]

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
    Count the number of addresses with transaction count > min_tx_count per day.
    Date is calculated by: Timestamp(UTC+8) - 12 hours (so midnight-noon is grouped with previous day).
    Returns: (count, DataFrame with columns [Receiver Address, Date, Transaction Count])
    Only shows records where transaction count > min_tx_count.
    """
    if df.empty:
        return pd.DataFrame(columns=['Receiver Address', 'Date', 'Transaction Count'])
    
    # 调整日期（减12小时作为分界线）
    df = df.copy()
    df['adjusted_date'] = (df['Timestamp(UTC+8)'] + pd.Timedelta(hours=12)).dt.date
    
    # 按地址和调整后的日期分组，计算每组的交易笔数
    grouped = df.groupby(['Receiver Address', 'adjusted_date']).size().reset_index(name='Transaction Count')
    
    # 筛选交易笔数 > min_tx_count 的记录
    result_df = grouped[grouped['Transaction Count'] > min_tx_count].copy()
    result_df.columns = ['Receiver Address', 'Date', 'Transaction Count']
    
    # 按日期和交易次数排序
    result_df = result_df.sort_values(['Date', 'Transaction Count'], ascending=[False, False]).reset_index(drop=True)
    
    return result_df

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

def repeat_claim_ranking_by_address(df):
    """
    Exclude 'Reference' rows, then
    Calculate ranking of addresses by claim count.
    Returns: ranking DataFrame with columns [Receiver Address, 领取次数]
    """
    # 只考虑非 Reference 的数据
    df_filtered = df[df['TS_Category'] == 0]
    
    # 每个地址的领取次数
    ranking = df_filtered.groupby('Receiver Address').size().reset_index(name='领取次数')
    
    # 按领取次数从高到低排序
    ranking = ranking.sort_values('领取次数', ascending=False).reset_index(drop=True)
    
    # ✓ 只返回排行榜
    return ranking

def shit_price_avg(df):
    """
    Calculate the SHIT price on a specific day in SOL.
    """
    if df.empty:
        return 0
    return df['Price'].mean()
