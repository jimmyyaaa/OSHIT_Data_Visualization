import streamlit as st
import pandas as pd
import logging
from data_process import (
    load_sheet_data,
    filter_df_by_date,
    num_all_tx_excluding_reference,
    mean_median_by_address,
    avg_time_interval_by_address,
    num_tx_by_reference_level,
    repeat_claim_rate_and_ranking,
    count_addresses_by_tx_count,
    address_repeat_rate_vs_yesterday,
    num_address_without_reference,
    num_lucky_draws,
    amount_lucky_draws,
    num_address_lucky_draws
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SHEET_NAMES = ["TS_Log", "POS_Log", "Staking_Log", "ShitCode_Log"]

@st.cache_data
def get_data_frames():
    return load_sheet_data(SHEET_NAMES)

def main():
    try:
        data_frames = get_data_frames()

        st.set_page_config(
            page_title="OSHIT Web3 Data",
            page_icon="💩",
            layout="wide",
        )

        # ✓ 添加刷新按钮
        if st.sidebar.button(
            "刷新数据",
            width="stretch"
            ):
            st.cache_data.clear()
            st.rerun()

        selected_date = st.sidebar.date_input("选择日期 (UTC +8):")
        
        section = st.sidebar.selectbox(
            "选择数据板块",
            ["TS Data", "POS Data", "SHIT Code Data", "Staking Data", "SOL Revenue"],
        )
        
        st.title("OSHIT Web3 Data Visualization")

        # Filter data for the selected date
        TS_df = data_frames["TS_Log"]
        TS_df_today = filter_df_by_date(TS_df, selected_date)
        TS_df_prev_day = filter_df_by_date(TS_df, selected_date - pd.Timedelta(days=1))
        POS_df = data_frames["POS_Log"]
        POS_df_today = filter_df_by_date(POS_df, selected_date)
        POS_df_prev_day = filter_df_by_date(POS_df, selected_date - pd.Timedelta(days=1))
        Staking_df = data_frames["Staking_Log"]
        Staking_df_today = filter_df_by_date(Staking_df, selected_date)
        Staking_df_prev_day = filter_df_by_date(Staking_df, selected_date - pd.Timedelta(days=1))
        ShitCode_df = data_frames["ShitCode_Log"]
        ShitCode_df_today = filter_df_by_date(ShitCode_df, selected_date)
        ShitCode_df_prev_day = filter_df_by_date(ShitCode_df, selected_date - pd.Timedelta(days=1))

        # TS Section
        if section == "TS Data":
            st.header("TS Data")

            if len(TS_df_today) > 0:

                TS_11, TS_12, TS_13, TS_14 = st.columns(4, gap="medium")
                TS_11.metric(
                    "交易总笔数",
                    f"{TS_df_today.shape[0]}",
                    delta = f"{TS_df_today.shape[0] - TS_df_prev_day.shape[0]}",
                    border = True
                )

                TS_12.metric(
                    "交易领取数（剔除Reference）",
                    f"{num_all_tx_excluding_reference(TS_df_today)}",
                    delta = f"{num_all_tx_excluding_reference(TS_df_today) - num_all_tx_excluding_reference(TS_df_prev_day)}",
                    border = True
                )

                TS_13.metric(
                    "交易金额",
                    f"{TS_df_today['SHIT Sent'].sum()}",
                    delta = f"{TS_df_today['SHIT Sent'].sum() - TS_df_prev_day['SHIT Sent'].sum()}",
                    border = True
                )

                TS_14.metric(
                    "地址参与数",
                    f"{num_address_without_reference(TS_df_today)}",
                    delta = f"{num_address_without_reference(TS_df_today) - num_address_without_reference(TS_df_prev_day)}",
                    border = True
                )

                TS_21, TS_22, TS_23 = st.columns(3, gap="medium")

                mean_tx, median_tx = mean_median_by_address(TS_df_today)
                mean_tx_prev, median_tx_prev = mean_median_by_address(TS_df_prev_day)
                TS_21.metric(
                    "每个地址平均领取次数",
                    f"{mean_tx:.2f}",
                    delta = f"{mean_tx - mean_tx_prev:.2f}",
                    border = True
                )

                TS_22.metric(
                    "每个地址领取中位数",
                    f"{median_tx}",
                    delta = f"{median_tx - median_tx_prev}",
                    border = True
                )

                TS_23.metric(
                    "一天内平均时间间隔（秒）",
                    f"{avg_time_interval_by_address(TS_df_today):.2f}",
                    delta = f"{avg_time_interval_by_address(TS_df_today) - avg_time_interval_by_address(TS_df_prev_day):.2f}",
                    border = True
                )

                TS_31, TS_32, TS_33 = st.columns(3, gap="medium")

                TS_0, TS_1, TS_2 = num_tx_by_reference_level(TS_df_today)
                TS_0_prev, TS_1_prev, TS_2_prev = num_tx_by_reference_level(TS_df_prev_day)
                TS_31.metric(
                    "独狼交易笔数",
                    f"{TS_0}",
                    delta = f"{TS_0 - TS_0_prev}",
                    border = True
                )

                TS_32.metric(
                    "一级Reference交易笔数",
                    f"{TS_1}",
                    delta = f"{TS_1 - TS_1_prev}",
                    border = True
                )

                TS_33.metric(
                    "二级Reference交易笔数",
                    f"{TS_2}",
                    delta = f"{TS_2 - TS_2_prev}",
                    border = True
                )
                
                TS_41, TS_42, TS_43 = st.columns(3, gap="medium")    
                TS_41.metric(
                    "抽奖总次数",
                    f"{num_lucky_draws(TS_df_today)}",
                    delta = f"{num_lucky_draws(TS_df_today) - num_lucky_draws(TS_df_prev_day)}",
                    border = True
                )

                TS_42.metric(
                    "抽奖总金额",
                    f"{amount_lucky_draws(TS_df_today)}",
                    delta = f"{amount_lucky_draws(TS_df_today) - amount_lucky_draws(TS_df_prev_day)}",
                    border = True
                )

                TS_43.metric(
                    "抽奖地址参与数",
                    f"{num_address_lucky_draws(TS_df_today)}",
                    delta = f"{num_address_lucky_draws(TS_df_today) - num_address_lucky_draws(TS_df_prev_day)}",
                    border = True
                )
                
                repeat_ranking = repeat_claim_rate_and_ranking(TS_df, selected_date)
                st.write("重复领取排行榜（过去7天）")
                if len(repeat_ranking) > 0:
                    st.dataframe(
                        repeat_ranking,
                        width='stretch',
                    )
                else:
                    st.info("当天无重复领取的地址")
                    
            else:
                st.info("当天无 TS 交易数据")
        
        # POS Section
        elif section == "POS Data":
            st.header("POS Data")

            if len(POS_df_today) > 0:
                
                POS_11, POS_12, POS_13, POS_14 = st.columns(4, gap="medium")
                POS_11.metric(
                    "交易笔数",
                    f"{POS_df_today.shape[0]}",
                    delta = f"{POS_df_today.shape[0] - POS_df_prev_day.shape[0]}",
                    border = True
                )

                POS_12.metric(
                    "总交易金额",
                    f"{POS_df_today['SHIT Sent'].sum():,.2f}",
                    delta = f"{POS_df_today['SHIT Sent'].sum() - POS_df_prev_day['SHIT Sent'].sum():,.2f}",
                    border = True
                )

                POS_13.metric(
                    "最大交易金额",
                    f"{POS_df_today['SHIT Sent'].max():,.2f}",
                    delta = f"{POS_df_today['SHIT Sent'].max() - POS_df_prev_day['SHIT Sent'].max():,.2f}",
                    border = True
                )

                POS_14.metric(
                    "最小交易金额",
                    f"{POS_df_today['SHIT Sent'].min():,.2f}",
                    delta = f"{POS_df_today['SHIT Sent'].min() - POS_df_prev_day['SHIT Sent'].min():,.2f}",
                    border = True
                )

                POS_duplicate_count, POS_duplicate_df = count_addresses_by_tx_count(POS_df_today, min_tx_count=1)
                POS_duplicate_count_prev, POS_duplicate_df_prev = count_addresses_by_tx_count(POS_df_prev_day, min_tx_count=1)
                st.metric(
                    "交易次数>1的地址数量",
                    f"{POS_duplicate_count}",
                    delta = f"{POS_duplicate_count - POS_duplicate_count_prev}",
                    border = True
                )

                if POS_duplicate_count > 0:
                    st.write("交易次数>1的地址列表：")
                    st.dataframe(
                        POS_duplicate_df.reset_index(drop=True),
                        width='stretch',
                    )

            else:
                st.info("当天无 POS 交易数据")
            
        # SHIT Code Section
        elif section == "SHIT Code Data":
            st.header("SHIT Code Data")

            if len(ShitCode_df_today) > 0:

                SC_11, SC_12, SC_13, SC_14 = st.columns(4, gap="medium")
                SC_11.metric(
                    "领取次数",
                    f"{ShitCode_df_today.shape[0]}",
                    delta = f"{ShitCode_df_today.shape[0] - ShitCode_df_prev_day.shape[0]}",
                    border = True
                )

                SC_12.metric(
                    "领取金额",
                    f"{ShitCode_df_today['SHIT Sent'].sum():,.2f}",
                    delta = f"{ShitCode_df_today['SHIT Sent'].sum() - ShitCode_df_prev_day['SHIT Sent'].sum():,.2f}",
                    border = True
                )

                SC_13.metric(
                    "地址参与数",
                    f"{ShitCode_df_today['Receiver Address'].nunique()}",
                    delta = f"{ShitCode_df_today['Receiver Address'].nunique() - ShitCode_df_prev_day['Receiver Address'].nunique()}",
                    border = True
                )

                SC_14.metric(
                    "地址重复率（vs昨天）",
                    f"{address_repeat_rate_vs_yesterday(ShitCode_df, selected_date) * 100:.2f}%",
                    delta = f"{address_repeat_rate_vs_yesterday(ShitCode_df, selected_date) * 100 - address_repeat_rate_vs_yesterday(ShitCode_df, selected_date - pd.Timedelta(days=1)) * 100:.2f}%",
                    border = True
                )

                st.metric(
                    "用户可获利",
                    f"place_holder",
                    delta = f"place_holder",
                    border = True
                )

            else:
                st.info("当天无 SHIT Code 交易数据")

        # Staking Section
        elif section == "Staking Data":
            st.header("Staking Data")

            if len(Staking_df_today) > 0:

                SK_11, SK_12, SK_13, SK_14 = st.columns(4, gap="medium")
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

                SK_13.metric(
                    "奖励领取数",
                    f"{Staking_df_today.shape[0]}",
                    delta = f"{Staking_df_today.shape[0] - Staking_df_prev_day.shape[0]}",
                    border = True
                )

                SK_14.metric(
                    "奖励领取金额",
                    f"{Staking_df_today['SHIT Sent'].sum():,.2f}",
                    delta = f"{Staking_df_today['SHIT Sent'].sum() - Staking_df_prev_day['SHIT Sent'].sum():,.2f}",
                    border = True
                )

            else:
                st.info("当天无 Staking 交易数据")
            
        # Revenue Section
        elif section == "SOL Revenue":
            st.header("SOL Revenue")

            SOL_11, SOL_12, SOL_13, SOL_14 = st.columns(4)
            if len(TS_df_today) > 0:
                SOL_11.metric(
                    "TS收入",
                    f"{TS_df_today['SOL_Received'].sum():,.4f}",
                    delta = f"{TS_df_today['SOL_Received'].sum() - TS_df_prev_day['SOL_Received'].sum():,.4f}",
                    border = True
                )
            else:
                st.info("当天无 TS 交易数据")

            if len(POS_df_today) > 0:
                SOL_12.metric(
                    "POS收入",
                    f"{POS_df_today['SOL Received'].sum():,.4f}",
                    delta = f"{POS_df_today['SOL Received'].sum() - POS_df_prev_day['SOL Received'].sum():,.4f}",
                    border = True
                )
            else:
                st.info("当天无 POS 交易数据")

            if len(Staking_df_today) > 0:
                SOL_13.metric(
                    "Staking收入",
                    f"{Staking_df_today['SOL Received'].sum():,.4f}",
                    delta = f"{Staking_df_today['SOL Received'].sum() - Staking_df_prev_day['SOL Received'].sum():,.4f}",
                    border = True
                )
            else:
                st.info("当天无 Staking 交易数据")

            if len(ShitCode_df_today) > 0:
                SOL_14.metric(
                    "SHIT Code收入",
                    f"{ShitCode_df_today['SOL Received'].sum():,.4f}",
                    delta = f"{ShitCode_df_today['SOL Received'].sum() - ShitCode_df_prev_day['SOL Received'].sum():,.4f}",
                    border = True
                )
            else:
                st.info("当天无 SHIT Code 交易数据")

    except Exception as e:
        st.error("Failed to load Google Sheets data. Please ensure the service account email has Viewer access and that service_account and sheet_id are configured in secrets. Error: " + str(e))

main()