import pandas as pd

def delta_percent(current, prev, default="N/A"):
    """Format delta as percentage."""
    if prev == 0 or pd.isna(prev):
        return default
    return ((current - prev) / prev)