import streamlit as st
import logging

logger = logging.getLogger(__name__)

def render_revenue_section(TS_df_current, TS_df_prev, POS_df_current, POS_df_prev, Staking_df_current, Staking_df_prev, ShitCode_df_current, ShitCode_df_prev):
    """渲染 SOL Revenue section"""

    logger.info("Rendering SOL Revenue section")
    st.header("SOL Revenue")

    # Initialize revenue variables
    TS_Revenue_current = TS_Revenue_prev = 0
    POS_Revenue_current = POS_Revenue_prev = 0
    Staking_Revenue_current = Staking_Revenue_prev = 0
    ShitCode_Revenue_current = ShitCode_Revenue_prev = 0

    SOL_11, SOL_12, SOL_13, SOL_14 = st.columns(4)
    if len(TS_df_current) > 0:
        TS_Revenue_current = TS_df_current['SOL_Received'].sum()
        TS_Revenue_prev = TS_df_prev['SOL_Received'].sum()
        SOL_11.metric(
            "TS收入",
            f"{TS_Revenue_current:,.6f}",
            delta = f"{(TS_Revenue_current - TS_Revenue_prev) / TS_Revenue_prev:,.2%}" if TS_df_prev.shape[0] != 0 else "N/A",
            border = True
        )
    else:
        st.info("当天无 TS 交易数据")

    if len(POS_df_current) > 0:
        POS_Revenue_current = POS_df_current['SOL Received'].sum()
        POS_Revenue_prev = POS_df_prev['SOL Received'].sum()
        SOL_12.metric(
            "POS收入",
            f"{POS_Revenue_current:,.6f}",
            delta = f"{(POS_Revenue_current - POS_Revenue_prev) / POS_Revenue_prev:,.2%}" if POS_df_prev.shape[0] != 0 else "N/A",
            border = True
        )
    else:
        st.info("当天无 POS 交易数据")

    if len(Staking_df_current) > 0:
        Staking_Revenue_current = Staking_df_current['SOL Received'].sum()
        Staking_Revenue_prev = Staking_df_prev['SOL Received'].sum()
        SOL_13.metric(
            "Staking收入",
            f"{Staking_Revenue_current:,.6f}",
            delta = f"{(Staking_Revenue_current - Staking_Revenue_prev) / Staking_Revenue_prev:,.2%}" if Staking_df_prev.shape[0] != 0 else "N/A",
            border = True
        )
    else:
        st.info("当天无 Staking 交易数据")

    if len(ShitCode_df_current) > 0:
        ShitCode_Revenue_current = ShitCode_df_current['SOL Received'].sum()
        ShitCode_Revenue_prev = ShitCode_df_prev['SOL Received'].sum()
        SOL_14.metric(
            "SHIT Code收入",
            f"{ShitCode_Revenue_current:,.6f}",
            delta = f"{(ShitCode_Revenue_current - ShitCode_Revenue_prev)/ShitCode_Revenue_prev:,.2%}" if ShitCode_df_prev.shape[0] != 0 else "N/A",
            border = True
        )
    else:
        st.info("当天无 SHIT Code 交易数据")

    st.metric(
        "总收入", 
        f"{TS_Revenue_current + POS_Revenue_current + Staking_Revenue_current + ShitCode_Revenue_current:,.6f}",
        delta = f"{((TS_Revenue_current + POS_Revenue_current + Staking_Revenue_current + ShitCode_Revenue_current) - (TS_Revenue_prev + POS_Revenue_prev + Staking_Revenue_prev + ShitCode_Revenue_prev))/(TS_Revenue_prev + POS_Revenue_prev + Staking_Revenue_prev + ShitCode_Revenue_prev):,.2%}" if (TS_Revenue_prev + POS_Revenue_prev + Staking_Revenue_prev + ShitCode_Revenue_prev) != 0 else "N/A",
        border = True
    )
