import streamlit as st
import pandas as pd
import logging
from app.config import SHEET_NAMES, PAGE_CONFIG, MIN_DATE, MAX_DATE
from data.loaders import load_sheet_data
from app.ui.sections.ts_section import render_ts_section
from app.ui.sections.pos_section import render_pos_section
from app.ui.sections.shitcode_section import render_shitcode_section
from app.ui.sections.staking_section import render_staking_section
from app.ui.sections.revenue_section import render_revenue_section
from data.filters import filter_df_by_date_range, filter_df_by_date_range_pos
from data.calculations import shit_price_avg
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def get_data_frames():
    return load_sheet_data(SHEET_NAMES)

def main():
    try:
        data_frames = load_sheet_data(SHEET_NAMES)

        st.set_page_config(**PAGE_CONFIG)

        if st.sidebar.button(
            "刷新数据",
            width="stretch"
        ):
            st.cache_data.clear()
            st.rerun()

        start_date = st.sidebar.date_input("选择开始日期 (UTC +8):", value="today", min_value=MIN_DATE, max_value=MAX_DATE)
        end_date = st.sidebar.date_input("选择结束日期 (UTC +8):", value="today", min_value=start_date, max_value=MAX_DATE)

        section = st.sidebar.selectbox(
            "选择数据板块",
            ["TS Data", "POS Data", "SHIT Code Data", "Staking Data", "SOL Revenue"],
            index=0
        )
        
        st.title("OSHIT Web3 Data Visualization")

        # Calculate the date range length
        date_range_length = (end_date - start_date).days + 1
        prev_start_date = start_date - pd.Timedelta(days=date_range_length)
        prev_end_date = start_date - pd.Timedelta(days=1)

        # Filter data for the selected date range
        TS_df = data_frames["TS_Log"]
        TS_df_current = filter_df_by_date_range(TS_df, start_date, end_date)
        TS_df_prev = filter_df_by_date_range(TS_df, prev_start_date, prev_end_date)
        
        # POS 有特殊的时间范围（GMT + 8 中午12点为基准）
        POS_df = data_frames["POS_Log"]
        POS_df_current = filter_df_by_date_range_pos(POS_df, start_date, end_date)
        POS_df_prev = filter_df_by_date_range_pos(POS_df, prev_start_date, prev_end_date)
        
        Staking_df = data_frames["Staking_Log"]
        Staking_df_current = filter_df_by_date_range(Staking_df, start_date, end_date)
        Staking_df_prev = filter_df_by_date_range(Staking_df, prev_start_date, prev_end_date)
        
        ShitCode_df = data_frames["ShitCode_Log"]
        ShitCode_df_current = filter_df_by_date_range(ShitCode_df, start_date, end_date)
        ShitCode_df_prev = filter_df_by_date_range(ShitCode_df, prev_start_date, prev_end_date)
        
        TS_DC_df = data_frames["TS_Discord"]
        TS_DC_df_current = filter_df_by_date_range(TS_DC_df, start_date, end_date)
        TS_DC_df_prev = filter_df_by_date_range(TS_DC_df, prev_start_date, prev_end_date)

        # Calculate Avg SHIT Price in SOL
        shit_price_avg_current = shit_price_avg(ShitCode_df_current)
        shit_price_avg_prev = shit_price_avg(ShitCode_df_prev)

        # TS Section
        if section == "TS Data":
            render_ts_section(TS_df_current, TS_df_prev, TS_DC_df_current, TS_DC_df_prev, shit_price_avg_current, shit_price_avg_prev)
        
        # POS Section
        elif section == "POS Data":
            render_pos_section(POS_df_current, POS_df_prev)

        # SHIT Code Section
        elif section == "SHIT Code Data":
            render_shitcode_section(ShitCode_df_current, ShitCode_df_prev, ShitCode_df, start_date, shit_price_avg_current, shit_price_avg_prev)

        # Staking Section
        elif section == "Staking Data":
            render_staking_section(Staking_df, Staking_df_current, Staking_df_prev)
            
        # Revenue Section
        elif section == "SOL Revenue":
            render_revenue_section(TS_df_current, TS_df_prev, POS_df_current, POS_df_prev, Staking_df_current, Staking_df_prev, ShitCode_df_current, ShitCode_df_prev)

    except Exception as e:
        st.error("Error: " + str(e))

main()