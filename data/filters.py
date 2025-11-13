import pandas as pd
import logging

logger = logging.getLogger(__name__)

def filter_df_by_date_range(df, start_date, end_date):
    """
    Filter the DataFrame for rows 'Timestamp(UTC+8)' within the date range [start_date, end_date].
    Both dates are inclusive.
    """
    if df.empty:
        return df  
    
    filtered_df = df[
        (df['Timestamp(UTC+8)'].dt.date >= start_date) & 
        (df['Timestamp(UTC+8)'].dt.date <= end_date)
    ]
    return filtered_df

def filter_df_by_date_range_pos(df, start_date, end_date):
    """
    Filter the POS DataFrame for rows 'Timestamp(UTC+8)' (adjusted by -12h) within the date range [start_date, end_date].
    Both dates are inclusive. The -12h adjustment groups midnight-noon data with the previous day.
    """
    if df.empty:
        return df
    
    adjusted_date = (df['Timestamp(UTC+8)'] + pd.Timedelta(hours=12)).dt.date
    filtered_df = df[
        (adjusted_date >= start_date) & 
        (adjusted_date <= end_date)
    ]
    return filtered_df
