import streamlit as st
import logging

logger = logging.getLogger(__name__)

def render_staking_section(Staking_df, Staking_df_current, Staking_df_prev):
    """渲染 Staking Data section"""
    
    logger.info("Rendering Staking Data section")
    st.header("Staking Data")

    if len(Staking_df) > 0:

        SK_11, SK_12 = st.columns(2, gap="medium")
        SK_11.metric(
            "质押总额",
            f"place_holder",
            delta = f"place_holder",
            border = True
        )

        SK_12.metric(
            "质押次数",
            f"place_holder",
            delta = f"place_holder",
            border = True
        )

        SK_21, SK_22 = st.columns(2, gap="medium")
        SK_21.metric(
            "奖励领取数",
            f"{Staking_df_current.shape[0]:,}",
            delta = f"{(Staking_df_current.shape[0] - Staking_df_prev.shape[0]) / Staking_df_prev.shape[0]:.2%}" if len(Staking_df_prev) != 0 else "N/A",
            border = True
        )

        SK_22.metric(
            "奖励领取金额",
            f"{Staking_df_current['SHIT Sent'].sum():,.2f}",
            delta = f"{(Staking_df_current['SHIT Sent'].sum() - Staking_df_prev['SHIT Sent'].sum()) / Staking_df_prev['SHIT Sent'].sum():.2%}" if len(Staking_df_prev) != 0 else "N/A",
            border = True
        )

    else:
        st.info("当天无 Staking 交易数据")
