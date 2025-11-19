# 🚀 OSHIT Web3 Data Visualization

一个基于 **Streamlit** 和 **Google Sheets** 的实时数据可视化仪表板，用于分析和展示 OSHIT Web3 生态的多维数据指标。

## 📋 项目概述

本项目是一个交互式数据分析平台，集成了 Google Sheets 数据源，通过 Streamlit 提供实时、多维度的数据分析和可视化功能。支持 **TS 交易数据**、**POS 数据**、**SHIT Code 数据**、**Staking 数据**、**SOL 收入** 和 **DeFi 数据** 等多个数据板块。

## ✨ 核心功能

### 📊 六大数据板块

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
- 交易金额分布图

#### 3️⃣ **SHIT Code Data（空投数据）**
- 领取次数
- 领取金额
- 地址参与数
- 地址重复率（vs 昨天）
- 用户获利分析（SHIT 价格）

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
- 总收入统计

#### 6️⃣ **DeFi Data（去中心化交易）**
- 买入/卖出交易统计
- 交易金额分析
- TS 区间卖出分析
- 交易地址和金额排行榜

### 🎯 核心特性

- 📅 **日期范围选择器** - 支持选择开始和结束日期，自动计算环比
- 🔄 **数据缓存** - 首次加载后自动缓存，切换导航栏无需重新加载
- 🔁 **刷新按钮** - 手动刷新数据，重新读取 Google Sheets
- 📊 **环比展示** - 每个指标都显示与前一时期的对比变化
- 📈 **排行榜** - 支持查看重复领取排行和交易详情
- 🎨 **响应式设计** - Wide layout，适配大屏展示
- 📱 **模块化架构** - 代码结构清晰，易于维护和扩展
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
| **NumPy** | 数值计算 |
| **Matplotlib** | 数据可视化 |
| **Google Sheets API** | 数据源 |
| **gspread** | Google Sheets Python 客户端 |
| **google-auth** | Google 认证 |

## 📦 项目结构

```
OSHIT_Data_Visualization/
├── streamlit_app.py                    # 主应用入口
├── requirements.txt                    # 项目依赖
├── oshit-data-visualization-dd0ed1145527.json  # Google 服务账号密钥
├── app/                                # 应用主目录
│   ├── __init__.py
│   ├── main.py                         # 主应用逻辑
│   ├── config.py                       # 配置常量
│   └── ui/
│       ├── __init__.py
│       └── sections/                   # UI 模块
│           ├── __init__.py
│           ├── ts_section.py           # TS 数据板块
│           ├── pos_section.py          # POS 数据板块
│           ├── shitcode_section.py     # SHIT Code 数据板块
│           ├── staking_section.py      # Staking 数据板块
│           ├── revenue_section.py      # 收入汇总板块
│           └── defi_section.py         # DeFi 数据板块
├── data/                               # 数据处理层
│   ├── __init__.py
│   ├── loaders.py                      # 数据加载
│   ├── filters.py                      # 数据过滤
│   └── calculations.py                 # 数据计算
├── utils/                              # 工具函数
│   ├── __init__.py
│   └── helpers.py                      # 辅助函数
├── .streamlit/
│   └── secrets.toml                    # Streamlit 配置
├── __pycache__/                        # Python 缓存
└── README.md                           # 本文件
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
streamlit run streamlit_app.py
```

应用将在浏览器中打开，默认地址：`http://localhost:8501`

## 📊 数据处理流程

### 核心函数说明

| 模块 | 函数名 | 说明 | 返回值 |
|------|-------|------|--------|
| `data.loaders` | `load_sheet_data()` | 加载 Google Sheet 数据 | `dict[DataFrame]` |
| `data.filters` | `filter_df_by_date()` | 按日期筛选数据 | `DataFrame` |
| `data.filters` | `filter_df_by_date_range()` | 按日期范围筛选数据 | `DataFrame` |
| `data.calculations` | `num_all_tx_excluding_reference()` | 排除 Reference 的交易数 | `int` |
| `data.calculations` | `mean_median_by_address()` | 地址交易数统计 | `(float, float)` |
| `data.calculations` | `avg_time_interval_by_address()` | 平均交易时间间隔 | `float` |
| `data.calculations` | `num_tx_by_reference_level()` | Reference 等级分布 | `(int, int, int)` |
| `data.calculations` | `repeat_claim_ranking_by_address()` | 重复领取排行榜 | `DataFrame` |
| `data.calculations` | `address_repeat_rate_vs_yesterday()` | 地址重复率 | `float` |
| `data.calculations` | `count_addresses_by_tx_count()` | 多次交易地址统计 | `int` |
| `data.calculations` | `shit_price_avg()` | SHIT 平均价格 | `float` |

### 数据处理层级

```
Google Sheets (Operational + DeFi)
    ↓
data.loaders.load_sheet_data()  (缓存 @st.cache_data)
    ↓
raw_dataframes
    ↓
data.filters.filter_df_by_date_range()
    ↓
date_filtered_data
    ↓
data.calculations.* (各类聚合函数)
    ↓
app.ui.sections.* (各板块渲染)
    ↓
Streamlit UI (展示)
```

## 📱 UI 交互

### 侧边栏控制

```
🔄 刷新数据          ← 手动刷新，清空缓存重新加载
📅 选择开始日期 (UTC+8) ← 选择日期范围的开始日期
📅 选择结束日期 (UTC+8) ← 选择日期范围的结束日期
📊 选择数据板块       ← 切换不同的分析视图
```

### 主界面布局

- **宽屏模式** - 使用 `layout="wide"` 充分利用屏幕空间
- **4 列指标卡** - 展示主要指标和环比变化
- **环比显示** - 每个指标显示 `delta`（与前一时期对比）
- **数据表格** - 可交互式数据表格，支持排序和格式化
- **图表展示** - Matplotlib 生成的分布图
- **模块化渲染** - 每个数据板块独立渲染函数

## 🔍 常见问题

### Q: 为什么表格行数和地址参与数不匹配？

**A:** 因为一个地址可能有多笔交易。例如：
- 总交易笔数 = 4
- 地址参与数 = 3（可能是 A 地址有 2 笔、B、C 各 1 笔）
- 排行榜行数 = 3（每个地址一行）

### Q: 数据多久更新一次？

**A:** 数据从 Google Sheets 读取。首次加载后会缓存，点击"刷新数据"按钮可重新加载。

### Q: 日期范围选择有什么作用？

**A:** 支持选择开始和结束日期，系统会自动计算该时间段的数据，并与前一个相同长度的时间段进行环比比较。

### Q: DeFi 数据和其他数据有什么区别？

**A:** DeFi 数据来自独立的 Google Sheet，包含买入/卖出交易详情。其他数据来自 Operational Sheet。

### Q: 可以添加其他日期范围的分析吗？

**A:** 可以。修改 `app/main.py` 中的日期选择逻辑，或在 `data/calculations.py` 中添加新的聚合函数。

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

1. **在 `data/calculations.py` 中添加计算函数：**

```python
def my_new_metric(df):
    """描述函数功能"""
    result = df[...].calculate()
    return result
```

2. **在相应的 section 文件中导入并使用：**

```python
from data.calculations import my_new_metric

# 在 render_xxx_section() 函数中使用
col.metric(
    "指标名称",
    f"{my_new_metric(df_current)}",
    delta=f"{...}",
    border=True
)
```

### 添加新的数据板块

1. **创建新的 section 文件：** `app/ui/sections/new_section.py`

```python
def render_new_section(df_current, df_prev):
    st.header("New Section")
    
    col1, col2 = st.columns(2)
    col1.metric("指标1", "...")
    col2.metric("指标2", "...")
```

2. **在 `app/main.py` 中导入和使用：**

```python
from app.ui.sections.new_section import render_new_section

# 在主逻辑中添加
elif section == "New Section":
    render_new_section(df_current, df_prev)
```

3. **更新 `app/config.py` 中的 SHEET_NAMES：**

```python
SHEET_NAMES = ["TS_Log", "POS_Log", "Staking_Log", "ShitCode_Log", "DeFi_Log", "New_Log"]
```

### 修改 Google Sheet 源

编辑 `app/config.py` 中的：

```python
SHEET_NAMES = ["TS_Log", "POS_Log", "Staking_Log", "ShitCode_Log", "DeFi_Log"]
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

**Last Updated:** 2025-11-18  
**Version:** 2.0.0