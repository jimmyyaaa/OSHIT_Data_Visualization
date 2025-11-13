import streamlit as st
import matplotlib.pyplot as plt
from data.calculations import (
    count_addresses_by_tx_count,
)
import logging

logger = logging.getLogger(__name__)

def render_pos_section(POS_df_current, POS_df_prev):
    """渲染 POS Data section"""
    
    logger.info("Rendering POS Data section")
    st.header("POS Data")

    if len(POS_df_current) > 0:
        
        POS_11, POS_12 = st.columns(2, gap="medium")
        POS_11.metric(
            "交易笔数",
            f"{POS_df_current.shape[0]:,}",
            delta = f"{(POS_df_current.shape[0] - POS_df_prev.shape[0]) / POS_df_prev.shape[0]:.2%}" if POS_df_prev.shape[0] != 0 else "N/A",
            border = True
        )

        POS_12.metric(
            "总交易金额",
            f"{POS_df_current['SHIT Sent'].sum():,.2f}",
            delta = f"{(POS_df_current['SHIT Sent'].sum() - POS_df_prev['SHIT Sent'].sum()) / POS_df_prev['SHIT Sent'].sum():.2%}" if POS_df_prev['SHIT Sent'].sum() != 0 else "N/A",
            border = True
        )

        POS_21, POS_22 = st.columns(2, gap="medium")
        POS_21.metric(
            "最大交易金额",
            f"{POS_df_current['SHIT Sent'].max():,.2f}",
            delta = f"{(POS_df_current['SHIT Sent'].max() - POS_df_prev['SHIT Sent'].max()) / POS_df_prev['SHIT Sent'].max():.2%}" if POS_df_prev['SHIT Sent'].max() != 0 else "N/A",
            border = True
        )

        POS_22.metric(
            "最小交易金额",
            f"{POS_df_current['SHIT Sent'].min():,.2f}",
            delta = f"{(POS_df_current['SHIT Sent'].min() - POS_df_prev['SHIT Sent'].min()) / POS_df_prev['SHIT Sent'].min():.2%}" if POS_df_prev['SHIT Sent'].min() != 0 else "N/A",
            border = True
        )

        st.write("交易金额分布")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        n, bins, patches = ax.hist(POS_df_current['SHIT Sent']/1000, bins=20, color='#7FBA00', edgecolor='gray', alpha=0.7)

        ax.set_xticks(bins)
        ax.set_xticklabels([f'{int(x)}' for x in bins], rotation=45, ha='right')
        
        ax.set_xlabel('Amount (in thousands)', fontsize=12, color='gray')
        ax.set_ylabel('Frequency', fontsize=12, color='gray')
        ax.set_title('Transaction Amount Distribution', fontsize=14, fontweight='bold', color='gray')
        ax.tick_params(colors='gray')  # 刻度标签颜色灰色
        ax.spines['left'].set_visible(False)   # 左边框隐藏
        ax.spines['bottom'].set_visible(False) # 下边框隐藏
        ax.spines['top'].set_visible(False)   # 隐藏上边框
        ax.spines['right'].set_visible(False) # 隐藏右边框
        ax.grid(axis='y', alpha=0.2, color='gray')
        st.pyplot(fig, transparent=True)
        plt.close(fig)
        

        st.write("每日交易次数>1的地址列表：")
        POS_duplicate_df = count_addresses_by_tx_count(POS_df_current, min_tx_count=1)
        if len(POS_duplicate_df) > 0:
            st.dataframe(
                POS_duplicate_df.reset_index(drop=True),
                width='stretch',
            )
        else:
            st.info("一切正常！所选时间范围内无交易次数>1的地址")

    else:
        st.info("当天无 POS 交易数据")
