# 📊 Shopify 销售数据看板

基于 6 万条 Shopify 交易数据的交互式销售分析看板，使用 Python + Streamlit + Plotly 构建。

## 🔍 项目背景

对零售销售数据进行多维度分析，挖掘品类、区域、流量来源、折扣策略等对营收和利润的影响，为业务决策提供数据支撑。

## ✨ 功能亮点

- **KPI 指标卡**：总营收、总利润、订单数、客单价、平均评分一目了然
- **交互式筛选**：按品类、国家、流量来源实时过滤
- **7 大分析模块**：
  - 📈 月度营收与利润趋势
  - 🥧 品类营收与利润率分析
  - 🗺️ 区域销售对比
  - 🔗 流量来源转化分析
  - 💵 折扣率对利润率的影响（含趋势线）
  - 💳 支付方式与退货率分析
  - ⭐ 评分分布与营收关系
- **每个图表配有数据洞察**，直接输出可落地的业务建议

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 开发语言 |
| Pandas | 数据清洗与聚合 |
| Streamlit | Web 看板框架 |
| Plotly | 交互式可视化 |

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行看板

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

## 📁 项目结构

```
sales-dashboard/
├── app.py                      # 主程序（页面布局与组装）
├── components/
│   ├── __init__.py
│   ├── data_loader.py          # 数据加载与预处理
│   ├── aggregations.py         # 聚合计算（月度/品类/区域等）
│   ├── charts.py               # 图表生成（统一配色与样式）
│   └── insights.py             # 数据洞察（自动生成业务建议）
├── sales_data.csv              # 数据集
├── requirements.txt            # 依赖清单
└── README.md                   # 项目说明
```

## 📊 数据说明

| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | int | 订单ID |
| order_date | datetime | 下单日期 |
| customer_id | int | 客户ID |
| product_id | int | 产品ID |
| product_category | str | 产品品类 |
| product_price | float | 产品原价 |
| discount_percent | float | 折扣率 (%) |
| quantity | int | 购买数量 |
| customer_country | str | 客户国家 |
| traffic_source | str | 流量来源 |
| payment_method | str | 支付方式 |
| shipping_cost | float | 运费 |
| rating | float | 评分 (1-5) |
| is_returned | int | 是否退货 |
| discounted_price | float | 折后价 |
| revenue | float | 营收 |
| profit | float | 利润 |

## 🔑 关键分析结论

1. **营收≠利润**：高营收品类利润率未必最高，需关注成本结构
2. **折扣警戒线**：折扣超过 30% 利润率显著下降，退货率上升
3. **区域定价差异**：部分高营收国家利润率偏低，运费/折扣是主因
4. **流量质量**：订单量最大的渠道未必客单价最高，应平衡量与价

## 📄 License

MIT
