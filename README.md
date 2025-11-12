# 🚀 OSHIT Web3 Data Visualization

一个基于 **Streamlit** 和 **Google Sheets** 的实时数据可视化仪表板，用于分析和展示 OSHIT Web3 生态的多维数据指标。

## 📋 项目概述

本项目是一个交互式数据分析平台，集成了 Google Sheets 数据源，通过 Streamlit 提供实时、多维度的数据分析和可视化功能。支持 **TS 交易数据**、**POS 数据**、**SHIT Code 数据**、**Staking 数据** 和 **SOL 收入** 等多个数据板块。

## ✨ 核心功能

### 📊 五大数据板块

#### 1️⃣ **TS Data（交易数据）**
- 交易总笔数 & 环比变化
- 交易领取数（排除 Reference）
- 交易金额统计
- 地址参与数
- 平均/中位数交易次数
- 时间间隔分析
- Reference 等级分布（独狼、一级、二级）
- 重复领取排行榜（过去7天）

#### 2️⃣ **POS Data（销售数据）**
- 交易笔数
- 总交易金额
- 最大/最小交易金额
- 多次交易地址统计

#### 3️⃣ **SHIT Code Data（空投数据）**
- 领取次数
- 领取金额
- 地址参与数
- 地址重复率（vs 昨天）
- 用户获利分析

#### 4️⃣ **Staking Data（质押数据）**
- 质押总额
- 质押次数
- 奖励领取数
- 奖励领取金额

#### 5️⃣ **SOL Revenue（收入汇总）**
- TS 收入
- POS 收入
- Staking 收入
- SHIT Code 收入

### 🎯 核心特性

- 📅 **日期选择器** - 快速切换不同日期的数据视图
- 🔄 **数据缓存** - 首次加载后自动缓存，切换导航栏无需重新加载
- 🔁 **刷新按钮** - 手动刷新数据，重新读取 Google Sheets
- 📊 **环比展示** - 每个指标都显示与前一天的对比变化
- 📈 **排行榜** - 支持查看重复领取排行
- 🎨 **响应式设计** - Wide layout，适配大屏展示

## 🛠️ 技术栈

| 组件 | 说明 |
|------|------|
| **Python** | 3.12 |
| **Streamlit** | 交互式 Web 框架 |
| **Pandas** | 数据处理和分析 |
| **Google Sheets API** | 数据源 |
| **gspread** | Google Sheets Python 客户端 |
| **google-auth** | Google 认证 |

## 📦 项目结构

```
OSHIT_Data_Visualization/
├── app.py                                    # 主应用入口，UI 层
├── data_process.py                           # 数据处理函数，业务逻辑层
├── requirement.txt                           # 项目依赖
├── .streamlit/
│   └── secrets.toml                          # Streamlit 配置（需自行创建）
├── oshit-data-visualization-dd0ed1145527.json # Google 服务账号密钥
├── .gitignore                                # Git 忽略文件
├── test.py                                   # 测试文件
└── README.md                                 # 本文件
```

## 🚀 快速开始

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone <repository_url>
cd OSHIT_Data_Visualization

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirement.txt
```

### 2️⃣ Google Sheets 配置

#### 获取服务账号密钥

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Google Sheets API**
4. 创建 **Service Account**
5. 创建 **Service Account Key**（JSON 格式）
6. 下载 JSON 文件，放入项目根目录

#### 配置 `.streamlit/secrets.toml`

创建 `.streamlit/secrets.toml` 文件（如不存在）：

```toml
[google]
service_account = """{"type": "service_account", "project_id": "...", ...}"""
sheet_id = "YOUR_GOOGLE_SHEET_ID"
```

**生成正确格式的 JSON 字符串：**

```bash
python3 << 'EOF'
import json

with open('oshit-data-visualization-dd0ed1145527.json', 'r') as f:
    sa_json = json.load(f)

sa_json_str = json.dumps(sa_json)
print('service_account = """' + sa_json_str + '"""')
EOF
```

### 3️⃣ 给服务账号分配权限

1. 打开你的 Google Sheet
2. 点击 **共享** 按钮
3. 复制服务账号的邮箱（格式：`xxx@xxx.iam.gserviceaccount.com`）
4. 添加为协作者，权限为 **查看者**

### 4️⃣ 运行应用

```bash
streamlit run app.py
```

应用将在浏览器中打开，默认地址：`http://localhost:8501`

## 📊 数据处理流程

### 核心函数说明

| 函数名 | 说明 | 返回值 |
|-------|------|--------|
| `load_sheet_data()` | 加载 Google Sheet 数据 | `dict[DataFrame]` |
| `filter_df_by_date()` | 按日期筛选数据 | `DataFrame` |
| `num_all_tx_excluding_reference()` | 排除 Reference 的交易数 | `int` |
| `mean_median_by_address()` | 地址交易数统计 | `(float, float)` |
| `avg_time_interval_by_address()` | 平均交易时间间隔 | `float` |
| `num_tx_by_reference_level()` | Reference 等级分布 | `(int, int, int)` |
| `repeat_claim_rate_and_ranking()` | 重复领取排行榜 | `DataFrame` |
| `address_repeat_rate_vs_yesterday()` | 地址重复率 | `float` |
| `count_addresses_by_tx_count()` | 多次交易地址统计 | `int` |

### 数据处理层级

```
Google Sheets
    ↓
load_sheet_data()  (缓存 @st.cache_data)
    ↓
raw_dataframes
    ↓
filter_df_by_date()
    ↓
daily_filtered_data
    ↓
[各类聚合函数]
    ↓
metrics (展示)
```

## 📱 UI 交互

### 侧边栏控制

```
🔄 刷新数据          ← 手动刷新，清空缓存重新加载
📅 选择日期 (UTC+8)   ← 选择要查看的日期
📊 选择数据板块       ← 切换不同的分析视图
```

### 主界面布局

- **宽屏模式** - 使用 `layout="wide"` 充分利用屏幕空间
- **4 列指标卡** - 展示主要指标和环比变化
- **环比显示** - 每个指标显示 `delta`（与前一天对比）
- **排行榜表格** - 可交互式数据表格

## 🔍 常见问题

### Q: 为什么表格行数和地址参与数不匹配？

**A:** 因为一个地址可能有多笔交易。例如：
- 总交易笔数 = 4
- 地址参与数 = 3（可能是 A 地址有 2 笔、B、C 各 1 笔）
- 排行榜行数 = 3（每个地址一行）

### Q: 数据多久更新一次？

**A:** 数据从 Google Sheets 读取。首次加载后会缓存，点击"刷新数据"按钮可重新加载。

### Q: 可以添加其他日期范围的分析吗？

**A:** 可以。修改 `app.py` 中的日期选择逻辑，或在 `data_process.py` 中添加新的聚合函数。

### Q: Google Sheet 需要什么格式？

**A:** 必要列：
- `Timestamp(UTC+8)` - 时间戳
- `Receiver Address` - 接收地址
- `SHIT Sent` - 发送金额
- `SOL Received` - 接收 SOL
- `TS_Category` - 分类（0=普通, 1=一级Reference, 2=二级Reference, 3=Lucky Draw）

## 🔒 安全性说明

- ✅ `.gitignore` 已配置，自动忽略敏感文件：
  - `.streamlit/secrets.toml`
  - `oshit-data-visualization-dd0ed1145527.json`
- ✅ 服务账号权限为"查看者"，只读 Google Sheet
- ✅ 建议定期轮换服务账号密钥

## 📝 开发指南

### 添加新的指标

1. **在 `data_process.py` 中添加计算函数：**

```python
def my_new_metric(df):
    """描述函数功能"""
    result = df[...].calculate()
    return result
```

2. **在 `app.py` 中导入并使用：**

```python
from data_process import my_new_metric

# 在相应的 section 中调用
col.metric(
    "指标名称",
    f"{my_new_metric(df_today)}",
    delta=f"{...}",
    border=True
)
```

### 修改 Google Sheet 源

编辑 `app.py` 中的：

```python
SHEET_NAMES = ["TS_Log", "POS_Log", "Staking_Log", "ShitCode_Log"]
```

## 🐛 故障排查

| 问题 | 解决方案 |
|------|--------|
| `JSONDecodeError` | 检查 `secrets.toml` 中 JSON 格式是否正确 |
| `KeyError: 'google'` | 确保 `secrets.toml` 中有 `[google]` 部分 |
| 数据加载失败 | 检查服务账号是否有 Google Sheet 访问权限 |
| 缓存问题 | 点击"🔄 刷新数据"按钮或重启应用 |

## 📚 相关链接

- [Streamlit 文档](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [gspread 文档](https://docs.gspread.org/)
- [Pandas 文档](https://pandas.pydata.org/docs/)

## 👨‍💻 作者

OSHIT Web3 Team

## 📄 许可证

MIT License

---

**Last Updated:** 2025-11-11  
**Version:** 1.0.0