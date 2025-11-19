import streamlit as st
import pandas as pd
from data.calculations import (
    address_repeat_rate_vs_yesterday,
)
import logging

logger = logging.getLogger(__name__)

def render_shitcode_section(ShitCode_df_current, ShitCode_df_prev, ShitCode_df, start_date, shit_price_avg_current, shit_price_avg_prev):
    """渲染 SHIT Code Data section"""

    logger.info("Rendering SHIT Code Data section")
    st.header("SHIT Code Data")

    if len(ShitCode_df_current) > 0:

        SC_11, SC_12, SC_13, SC_14 = st.columns(4, gap="medium")
        SC_11.metric(
            "领取次数",
            f"{ShitCode_df_current.shape[0]:,}",
            delta = f"{(ShitCode_df_current.shape[0] - ShitCode_df_prev.shape[0]) / ShitCode_df_prev.shape[0]:.2%}" if ShitCode_df_prev.shape[0] != 0 else "N/A",
            border = True
        )

        SC_12.metric(
            "领取金额",
            f"{ShitCode_df_current['SHIT Sent'].sum():,}",
            delta = f"{(ShitCode_df_current['SHIT Sent'].sum() - ShitCode_df_prev['SHIT Sent'].sum())/ShitCode_df_prev['SHIT Sent'].sum():.2%}" if ShitCode_df_prev['SHIT Sent'].sum() != 0 else "N/A",
            border = True
        )

        SC_13.metric(
            "地址参与数",
            f"{ShitCode_df_current['Receiver Address'].nunique():,}",
            delta = f"{(ShitCode_df_current['Receiver Address'].nunique() - ShitCode_df_prev['Receiver Address'].nunique())/ShitCode_df_prev['Receiver Address'].nunique():.2%}" if ShitCode_df_prev['Receiver Address'].nunique() != 0 else "N/A",
            border = True
        )

        SC_14.metric(
            "地址重复率（vs昨天）",
            f"{address_repeat_rate_vs_yesterday(ShitCode_df, start_date) * 100:.2f}%",
            delta = f"{(address_repeat_rate_vs_yesterday(ShitCode_df, start_date) - address_repeat_rate_vs_yesterday(ShitCode_df, start_date - pd.Timedelta(days=1)))/address_repeat_rate_vs_yesterday(ShitCode_df, start_date - pd.Timedelta(days=1)):.2%}" if address_repeat_rate_vs_yesterday(ShitCode_df, start_date - pd.Timedelta(days=1)) != 0 else "N/A",
            border = True
        )

        st.metric(
            "用户可获利 (SOL)",
            f"{shit_price_avg_current * 4350:.6f}",
            delta = f"{(shit_price_avg_current - shit_price_avg_prev)/shit_price_avg_prev:.2%}" if shit_price_avg_prev != 0 else "N/A",
            border = True
        )
        
        
        SC_address_df = ShitCode_df_current.groupby('Receiver Address').size().reset_index()
        SC_address_df.columns = ['Receiver Address', 'Transaction Count']
        SC_address_df = SC_address_df.sort_values(by='Transaction Count', ascending=False)
        st.write("每个地址领取次数分布")
        st.dataframe(
            SC_address_df.reset_index(drop=True),
            width='stretch',
        )
        

    else:
        st.info("当天无 SHIT Code 交易数据")
