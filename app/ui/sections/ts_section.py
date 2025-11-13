import streamlit as st
from data.calculations import (
    num_all_tx_excluding_reference,
    mean_median_by_address,
    avg_time_interval_by_address,
    num_tx_by_reference_level,
    repeat_claim_ranking_by_address,
    num_address_without_reference,
    num_lucky_draws,
    amount_lucky_draws,
    num_address_lucky_draws,
)
import logging

logger = logging.getLogger(__name__)

def render_ts_section(TS_df_current, TS_df_prev, TS_DC_df_current, TS_DC_df_prev, shit_price_avg_current, shit_price_avg_prev):
    """渲染 TS Data section"""
    
    logger.info("Rendering TS Data section")
    st.header("TS Data")

    if len(TS_df_current) > 0:

        TS_11, TS_12, TS_13, TS_14 = st.columns(4, gap="medium")
        TS_11.metric(
            "交易总笔数",
            f"{TS_df_current.shape[0]:,}",
            delta = f"{(TS_df_current.shape[0] - TS_df_prev.shape[0])/TS_df_prev.shape[0]:.2%}" if TS_df_prev.shape[0] != 0 else "N/A",
            border = True
        )

        TS_12.metric(
            "TS领取数（剔除Reference）",
            f"{num_all_tx_excluding_reference(TS_df_current):,}",
            delta = f"{(num_all_tx_excluding_reference(TS_df_current) - num_all_tx_excluding_reference(TS_df_prev)) / num_all_tx_excluding_reference(TS_df_prev):.2%}" if num_all_tx_excluding_reference(TS_df_prev) != 0 else "N/A",
            border = True
        )

        TS_13.metric(
            "TS交易总金额",
            f"{TS_df_current['SHIT Sent'].sum():,}",
            delta = f"{(TS_df_current['SHIT Sent'].sum() - TS_df_prev['SHIT Sent'].sum())/TS_df_prev['SHIT Sent'].sum():.2%}" if TS_df_prev['SHIT Sent'].sum() != 0 else "N/A",
            border = True
        )

        TS_14.metric(
            "地址参与数",
            f"{num_address_without_reference(TS_df_current):,}",
            delta = f"{(num_address_without_reference(TS_df_current) - num_address_without_reference(TS_df_prev)) / num_address_without_reference(TS_df_prev):.2%}" if num_address_without_reference(TS_df_prev) != 0 else "N/A",
            border = True
        )

        TS_21, TS_22, TS_23 = st.columns(3, gap="medium")

        mean_tx, median_tx = mean_median_by_address(TS_df_current)
        mean_tx_prev, median_tx_prev = mean_median_by_address(TS_df_prev)
        TS_21.metric(
            "每个地址平均领取次数",
            f"{mean_tx:.2f}",
            delta = f"{mean_tx - mean_tx_prev:.2f}",
            border = True
        )

        TS_22.metric(
            "每个地址领取中位数",
            f"{int(median_tx)}",
            delta = f"{int(median_tx - median_tx_prev)}",
            border = True
        )

        TS_23.metric(
            "一天内平均时间间隔（分）",
            f"{avg_time_interval_by_address(TS_df_current):.2f}",
            delta = f"{avg_time_interval_by_address(TS_df_current) - avg_time_interval_by_address(TS_df_prev):.2f}",
            border = True
        )

        TS_31, TS_32, TS_33 = st.columns(3, gap="medium")

        TS_0, TS_1, TS_2 = num_tx_by_reference_level(TS_df_current)
        TS_0_prev, TS_1_prev, TS_2_prev = num_tx_by_reference_level(TS_df_prev)
        TS_31.metric(
            "独狼交易笔数",
            f"{TS_0:,}",
            delta = f"{(TS_0 - TS_0_prev) / TS_0_prev:.2%}" if TS_0_prev != 0 else "N/A",
            border = True
        )

        TS_32.metric(
            "存在一个上级交易笔数",
            f"{TS_1:,}",
            delta = f"{(TS_1 - TS_1_prev) / TS_1_prev:.2%}" if TS_1_prev != 0 else "N/A",
            border = True
        )

        TS_33.metric(
            "存在两个上级交易笔数",
            f"{TS_2:,}",
            delta = f"{(TS_2 - TS_2_prev) / TS_2_prev:.2%}" if TS_2_prev != 0 else "N/A",
            border = True
        )
        
        TS_41, TS_42, TS_43 = st.columns(3, gap="medium")    
        TS_41.metric(
            "抽奖总次数",
            f"{num_lucky_draws(TS_df_current):,}",
            delta = f"{(num_lucky_draws(TS_df_current) - num_lucky_draws(TS_df_prev)) / num_lucky_draws(TS_df_prev):.2%}" if num_lucky_draws(TS_df_prev) !=0 else "N/A",
            border = True
        )

        TS_42.metric(
            "抽奖总金额",
            f"{amount_lucky_draws(TS_df_current):,}",
            delta = f"{(amount_lucky_draws(TS_df_current) - amount_lucky_draws(TS_df_prev)) / amount_lucky_draws(TS_df_prev):.2%}" if amount_lucky_draws(TS_df_prev) !=0 else "N/A",
            border = True
        )

        TS_43.metric(
            "抽奖地址参与数",
            f"{num_address_lucky_draws(TS_df_current):,}",
            delta = f"{(num_address_lucky_draws(TS_df_current) - num_address_lucky_draws(TS_df_prev)) / num_address_lucky_draws(TS_df_prev):.2%}" if num_address_lucky_draws(TS_df_prev) !=0 else "N/A",
            border = True
        )
        
        TS_51, TS_52, TS_53 = st.columns(3, gap="medium")

        TS_SOL_Revenue_without_reward_current = TS_df_current['SOL_Received'].sum()
        TS_SOL_Revenue_without_reward_prev = TS_df_prev['SOL_Received'].sum()
        TS_51.metric(
            "TS收入（SOL): 不含奖励",
            f"{TS_SOL_Revenue_without_reward_current:,.4f}",
            delta = f"{(TS_SOL_Revenue_without_reward_current - TS_SOL_Revenue_without_reward_prev) / TS_SOL_Revenue_without_reward_prev:.2%}" if TS_SOL_Revenue_without_reward_prev !=0 else "N/A",
            border = True
        )

        SHIT_Cost_without_reward_current = TS_df_current['SHIT Sent'].sum() * shit_price_avg_current
        SHIT_Cost_without_reward_prev = TS_df_prev['SHIT Sent'].sum() * shit_price_avg_prev
        TS_52.metric(
            "付出SHIT成本(SOL): 不含奖励",
            f"{SHIT_Cost_without_reward_current:.4f}",
            delta = f"{(SHIT_Cost_without_reward_current - SHIT_Cost_without_reward_prev) / SHIT_Cost_without_reward_prev:.2%}" if SHIT_Cost_without_reward_prev !=0 else "N/A",
            border = True
        )

        TS_ROI_current = TS_SOL_Revenue_without_reward_current / SHIT_Cost_without_reward_current if SHIT_Cost_without_reward_current != 0 else 0
        TS_ROI_prev = TS_SOL_Revenue_without_reward_prev / SHIT_Cost_without_reward_prev if SHIT_Cost_without_reward_prev != 0 else 0
        TS_53.metric(
            "ROI: 不含奖励",
            f"{TS_ROI_current:.2f}",
            delta = f"{(TS_ROI_current - TS_ROI_prev) / TS_ROI_prev:.2%}" if TS_ROI_prev != 0 else "N/A",
            border = True
        )

        TS_61, TS_62, TS_63 = st.columns(3, gap="medium")

        Num_reward_current = TS_DC_df_current["SHIT Code Sent"].sum()
        Num_reward_prev = TS_DC_df_prev["SHIT Code Sent"].sum()
        TS_61.metric(
            "奖励总次数",
            f"{Num_reward_current:,}",
            delta = f"{(Num_reward_current - Num_reward_prev) / Num_reward_prev:.2%}" if Num_reward_prev != 0 else "N/A",
            border = True
        )

        Reward_Cost_current = Num_reward_current * 5000 * shit_price_avg_current
        Reward_Cost_prev = Num_reward_prev * 5000 * shit_price_avg_prev
        TS_62.metric(
            "奖励成本（SOL）",
            f"{Reward_Cost_current:.4f}",
            delta = f"{(Reward_Cost_current - Reward_Cost_prev) / Reward_Cost_prev:.2%}" if Reward_Cost_prev !=0 else "N/A",
            border = True
        )

        TS_ROI_with_reward_current = (TS_SOL_Revenue_without_reward_current + Reward_Cost_current * 0.13) / (SHIT_Cost_without_reward_current + Reward_Cost_current) if (SHIT_Cost_without_reward_current + Reward_Cost_current) != 0 else 0
        TS_ROI_with_reward_prev = (TS_SOL_Revenue_without_reward_prev + Reward_Cost_prev * 0.13) / (SHIT_Cost_without_reward_prev + Reward_Cost_prev) if (SHIT_Cost_without_reward_prev + Reward_Cost_prev) != 0 else 0
        TS_63.metric(
            "ROI: 含奖励",
            f"{TS_ROI_with_reward_current:.2f}",
            delta = f"{(TS_ROI_with_reward_current - TS_ROI_with_reward_prev) / TS_ROI_with_reward_prev:.2%}" if TS_ROI_with_reward_prev != 0 else "N/A",
            border = True
        )

        repeat_ranking = repeat_claim_ranking_by_address(TS_df_current)
        st.write("重复领取排行榜")
        if len(repeat_ranking) > 0:
            st.dataframe(
                repeat_ranking,
                width='stretch',
            )
        else:
            st.info("当前范围内无重复领取的地址")
                
    else:
        st.info("当前范围内无 TS 交易数据")
