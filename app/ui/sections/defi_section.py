import streamlit as st
import logging

logger = logging.getLogger(__name__)

def render_defi_section(df_current, df_prev):
    """渲染 DeFi Data section"""

    logger.info("Rendering DeFi Data section")
    st.header("DeFi Data")
    
    if len(df_current) > 0:

        buy_df_current = df_current[df_current["Activity"] == "BUY"]
        buy_df_prev = df_prev[df_prev["Activity"] == "BUY"]

        sell_df_current = df_current[df_current["Activity"] == "SELL"]
        sell_df_prev = df_prev[df_prev["Activity"] == "SELL"]

        defi_11, defi_12 = st.columns(2, gap="medium")
        defi_11.metric(
            "买入SHIT量",
            f"{buy_df_current['SHIT Change'].abs().sum():,.2f}",
            delta = f"{(buy_df_current['SHIT Change'].abs().sum() - buy_df_prev['SHIT Change'].abs().sum()) / buy_df_prev['SHIT Change'].abs().sum():.2%}" if buy_df_prev['SHIT Change'].abs().sum() != 0 else "N/A",
            border = True
        )
        
        defi_12.metric(
            "卖出SHIT量",
            f"{sell_df_current['SHIT Change'].abs().sum():,.2f}",
            delta = f"{(sell_df_current['SHIT Change'].abs().sum() - sell_df_prev['SHIT Change'].abs().sum()) / sell_df_prev['SHIT Change'].abs().sum():.2%}" if sell_df_prev['SHIT Change'].abs().sum() != 0 else "N/A",
            border = True
        )

        defi_21, defi_22 = st.columns(2, gap="medium")
        defi_21.metric(
            "买入总笔数",
            f"{buy_df_current.shape[0]:,}",
            delta = f"{(buy_df_current.shape[0] - buy_df_prev.shape[0]) / buy_df_prev.shape[0]:.2%}" if buy_df_prev.shape[0] != 0 else "N/A",
            border = True
        )

        defi_22.metric(
            "卖出总笔数",
            f"{sell_df_current.shape[0]:,}",
            delta = f"{(sell_df_current.shape[0] - sell_df_prev.shape[0]) / sell_df_prev.shape[0]:.2%}" if sell_df_prev.shape[0] != 0 else "N/A",
            border = True
        )

        defi_31, defi_32 = st.columns(2, gap="medium")
        defi_31.metric(
            "总买入金额（USDT）",
            f"{buy_df_current['USDT Change'].abs().sum():,.2f}",
            delta = f"{(buy_df_current['USDT Change'].abs().sum() - buy_df_prev['USDT Change'].abs().sum()) / buy_df_prev['USDT Change'].abs().sum():.2%}" if buy_df_prev['USDT Change'].abs().sum() != 0 else "N/A",
            border = True
        )

        defi_32.metric(
            "卖出总金额（USDT）",
            f"{sell_df_current['USDT Change'].abs().sum():,.2f}",
            delta = f"{(sell_df_current['USDT Change'].abs().sum() - sell_df_prev['USDT Change'].abs().sum()) / sell_df_prev['USDT Change'].abs().sum():.2%}" if sell_df_prev['USDT Change'].abs().sum() != 0 else "N/A",
            border = True
        )

        ts_sell_df_current = sell_df_current[(13e3 <= sell_df_current["SHIT Change"]) & (sell_df_current["SHIT Change"] <= 2e4)]
        ts_sell_df_prev = sell_df_prev[(13e3 <= sell_df_prev["SHIT Change"]) & (sell_df_prev["SHIT Change"] <= 2e4)]

        defi_41, defi_42 = st.columns(2, gap="medium")
        defi_41.metric(
            "TS卖出SHIT量",
            f"{ts_sell_df_current['SHIT Change'].abs().sum():,.2f}",
            delta = f"{(ts_sell_df_current['SHIT Change'].abs().sum() - ts_sell_df_prev['SHIT Change'].abs().sum()) / ts_sell_df_prev['SHIT Change'].abs().sum():.2%}" if ts_sell_df_prev['SHIT Change'].abs().sum() != 0 else "N/A",
            border = True
        )

        defi_42.metric(
            "TS卖出总金额（USDT）",
            f"{ts_sell_df_current['USDT Change'].abs().sum():,.2f}",
            delta = f"{(ts_sell_df_current['USDT Change'].abs().sum() - ts_sell_df_prev['USDT Change'].abs().sum()) / ts_sell_df_prev['USDT Change'].abs().sum():.2%}" if ts_sell_df_prev['USDT Change'].abs().sum() != 0 else "N/A",
            border = True
        )
        
        # BUY
        buy_table = buy_df_current[['FromAddress', 'SHIT Change']].copy()
        buy_table['SHIT Change'] = buy_table['SHIT Change'].abs()  # 取绝对值
        buy_table = buy_table.sort_values('SHIT Change', ascending=False)
        st.write("Buy Transactions")
        st.dataframe(
            buy_table.reset_index(drop=True),
            column_config={
                "SHIT Change": st.column_config.NumberColumn(
                    "SHIT Change",
                    format="accounting",
                ),
            },
            width = "stretch"
        )

        # SELL
        sell_table = sell_df_current[['FromAddress', 'SHIT Change']].copy()
        sell_table['SHIT Change'] = sell_table['SHIT Change'].abs()  # 取绝对值
        sell_table = sell_table.sort_values('SHIT Change', ascending=False)
        st.write("Sell Transactions")
        st.dataframe(
            sell_table.reset_index(drop=True),
            column_config={
                "SHIT Change": st.column_config.NumberColumn(
                    "SHIT Change",
                    format="accounting",
                ),
            },
            width = "stretch"
        )

    else:
        st.info("No DeFi data available for the selected date range.")