import streamlit as st
import pandas as pd
import plotly.express as px

# ========== 页面配置 ==========
st.set_page_config(page_title="Shopify销售数据看板", page_icon="📊", layout="wide")

# ========== 读取数据 ==========
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["Month"] = df["order_date"].dt.to_period("M").astype(str)
    df["Year"] = df["order_date"].dt.year
    df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(2)
    return df

df = load_data()

# ========== 侧边栏筛选器 ==========
st.sidebar.header("🔍 筛选条件")
categories = st.sidebar.multiselect("选择品类", df["product_category"].unique(), df["product_category"].unique())
countries = st.sidebar.multiselect("选择国家", df["customer_country"].unique(), df["customer_country"].unique())
sources = st.sidebar.multiselect("流量来源", df["traffic_source"].unique(), df["traffic_source"].unique())

filtered = df[
    (df["product_category"].isin(categories))
    & (df["customer_country"].isin(countries))
    & (df["traffic_source"].isin(sources))
]

# ========== 标题 ==========
st.title("📊 Shopify 销售数据看板")
st.caption("基于 6 万条交易数据的零售销售分析 | Python + Streamlit + Plotly")
st.markdown("---")

# ========== KPI 指标卡 ==========
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 总营收", f"${filtered['revenue'].sum():,.0f}")
col2.metric("📈 总利润", f"${filtered['profit'].sum():,.0f}")
col3.metric("🛒 订单数", f"{filtered['order_id'].nunique():,.0f}")
col4.metric("📦 平均客单价", f"${filtered['revenue'].mean():,.2f}")
col5.metric("⭐ 平均评分", f"{filtered['rating'].mean():.2f}")

st.markdown("---")

# ========== 1. 月度营收趋势 ==========
st.subheader("📈 月度营收与利润趋势")
monthly = filtered.groupby("Month").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
).reset_index()
fig_trend = px.line(monthly, x="Month", y=["revenue", "profit"], markers=True,
                    labels={"value": "金额 ($)", "variable": "指标"},
                    color_discrete_map={"revenue": "#4F46E5", "profit": "#10B981"})
st.plotly_chart(fig_trend, use_container_width=True)

best_month = monthly.loc[monthly["revenue"].idxmax()]
worst_month = monthly.loc[monthly["revenue"].idxmin()]
st.info(f"💡 **洞察**：营收最高月份为 {best_month['Month']}（${best_month['revenue']:,.0f}），"
        f"最低为 {worst_month['Month']}（${worst_month['revenue']:,.0f}）。"
        f"建议在低谷期加大营销投放，平抑季节性波动。")

st.markdown("---")

# ========== 2. 品类分析 ==========
st.subheader("🥧 品类营收与利润分析")
col_left, col_right = st.columns(2)

cat_sales = filtered.groupby("product_category").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count"),
    avg_margin=("profit_margin", "mean")
).reset_index()

with col_left:
    fig_pie = px.pie(cat_sales, values="revenue", names="product_category", hole=0.4,
                     title="营收占比")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    fig_cat_margin = px.bar(cat_sales, x="product_category", y="avg_margin",
                            color="product_category", title="平均利润率 (%)")
    fig_cat_margin.update_layout(xaxis_title="品类", yaxis_title="利润率 (%)")
    st.plotly_chart(fig_cat_margin, use_container_width=True)

top_cat = cat_sales.loc[cat_sales["revenue"].idxmax()]
top_margin_cat = cat_sales.loc[cat_sales["avg_margin"].idxmax()]
low_margin_cat = cat_sales.loc[cat_sales["avg_margin"].idxmin()]
st.info(f"💡 **洞察**：{top_cat['product_category']} 营收最高（${top_cat['revenue']:,.0f}），"
        f"但利润率最高的是 {top_margin_cat['product_category']}（{top_margin_cat['avg_margin']:.1f}%），"
        f"最低的是 {low_margin_cat['product_category']}（{low_margin_cat['avg_margin']:.1f}%）。"
        f"营收≠利润，高营收品类需关注成本控制。")

st.markdown("---")

# ========== 3. 区域分析 ==========
st.subheader("🗺️ 区域销售对比")
country_sales = filtered.groupby("customer_country").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count"),
    avg_margin=("profit_margin", "mean")
).reset_index()

fig_bar = px.bar(country_sales, x="customer_country", y="revenue", color="customer_country",
                 title="各国营收")
fig_bar.update_layout(xaxis_title="国家", yaxis_title="营收 ($)")
st.plotly_chart(fig_bar, use_container_width=True)

top_country = country_sales.loc[country_sales["revenue"].idxmax()]
low_country = country_sales.loc[country_sales["avg_margin"].idxmin()]
st.info(f"💡 **洞察**：{top_country['customer_country']} 营收领先（${top_country['revenue']:,.0f}），"
        f"但利润率最低的是 {low_country['customer_country']}（{low_country['avg_margin']:.1f}%），"
        f"可能存在运费或折扣过高问题，建议优化定价策略。")

st.markdown("---")

# ========== 4. 流量来源 ==========
st.subheader("🔗 流量来源转化分析")
col_left2, col_right2 = st.columns(2)

source_data = filtered.groupby("traffic_source").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    avg_revenue=("revenue", "mean")
).reset_index()

with col_left2:
    fig_source = px.bar(source_data, x="traffic_source", y="orders", color="traffic_source",
                        title="各来源订单量")
    st.plotly_chart(fig_source, use_container_width=True)

with col_right2:
    fig_source_rev = px.bar(source_data, x="traffic_source", y="avg_revenue", color="traffic_source",
                            title="各来源平均客单价")
    st.plotly_chart(fig_source_rev, use_container_width=True)

best_source = source_data.loc[source_data["orders"].idxmax()]
high_aov_source = source_data.loc[source_data["avg_revenue"].idxmax()]
st.info(f"💡 **洞察**：{best_source['traffic_source']} 带来最多订单（{best_source['orders']:,}），"
        f"但 {high_aov_source['traffic_source']} 客单价最高（${high_aov_source['avg_revenue']:,.0f}）。"
        f"高客单价渠道值得加大投入。")

st.markdown("---")

# ========== 5. 折扣影响分析 ==========
st.subheader("💵 折扣率对利润率的影响")

fig_scatter = px.scatter(filtered, x="discount_percent", y="profit_margin",
                         color="product_category", opacity=0.3, trendline="ols",
                         labels={"discount_percent": "折扣率 (%)", "profit_margin": "利润率 (%)"})
st.plotly_chart(fig_scatter, use_container_width=True)

filtered["discount_level"] = pd.cut(filtered["discount_percent"],
                                     bins=[0, 10, 20, 30, 50, 100],
                                     labels=["0-10%", "10-20%", "20-30%", "30-50%", "50%+"])
discount_impact = filtered.groupby("discount_level", observed=True).agg(
    avg_margin=("profit_margin", "mean"),
    return_rate=("is_returned", "mean"),
    orders=("order_id", "count")
).reset_index()

st.dataframe(discount_impact.style.format({"avg_margin": "{:.1f}%", "return_rate": "{:.2%}", "orders": "{:,}"}),
             use_container_width=True)

high_discount = discount_impact.loc[discount_impact["avg_margin"].idxmin()]
st.info(f"💡 **洞察**：折扣率 {high_discount['discount_level']} 区间利润率最低（{high_discount['avg_margin']:.1f}%），"
        f"且退货率随折扣升高而上升。建议将折扣控制在 20% 以内，避免利润侵蚀。")

st.markdown("---")

# ========== 6. 支付与退货 ==========
st.subheader("💳 支付方式与退货分析")
col_left3, col_right3 = st.columns(2)

payment = filtered.groupby("payment_method").agg(
    orders=("order_id", "count"),
    return_rate=("is_returned", "mean")
).reset_index()

with col_left3:
    fig_pay = px.pie(payment, values="orders", names="payment_method", hole=0.4,
                     title="支付方式分布")
    st.plotly_chart(fig_pay, use_container_width=True)

with col_right3:
    fig_return = px.bar(payment, x="payment_method", y="return_rate", color="payment_method",
                        title="各支付方式退货率")
    fig_return.update_layout(yaxis_tickformat=".1%", yaxis_title="退货率")
    st.plotly_chart(fig_return, use_container_width=True)

high_return_pay = payment.loc[payment["return_rate"].idxmax()]
st.info(f"💡 **洞察**：{high_return_pay['payment_method']} 退货率最高（{high_return_pay['return_rate']:.1%}），"
        f"可能存在支付便捷导致的冲动消费问题，可考虑针对性售后策略。")

st.markdown("---")

# ========== 7. 评分分布 ==========
st.subheader("⭐ 评分分布与影响")
col_left4, col_right4 = st.columns(2)

with col_left4:
    fig_rating = px.histogram(filtered, x="rating", nbins=20, title="评分分布")
    fig_rating.update_layout(xaxis_title="评分", yaxis_title="订单数")
    st.plotly_chart(fig_rating, use_container_width=True)

with col_right4:
    rating_impact = filtered.groupby(pd.cut(filtered["rating"], bins=[0, 2, 3, 4, 5]))["revenue"].mean().reset_index()
    rating_impact.columns = ["rating_range", "avg_revenue"]
    rating_impact["rating_range"] = rating_impact["rating_range"].astype(str)
    fig_rating_rev = px.bar(rating_impact, x="rating_range", y="avg_revenue",
                            title="不同评分区间的平均营收")
    st.plotly_chart(fig_rating_rev, use_container_width=True)

st.info("💡 **洞察**：评分分布可反映产品质量和客户满意度，低评分订单的退货率是否更高值得关注。")

st.markdown("---")

# ========== 数据表 ==========
with st.expander("📋 查看明细数据（前500条）"):
    st.dataframe(filtered.head(500), use_container_width=True)

# ========== 页脚 ==========
st.markdown("---")
st.caption("📌 数据来源：Shopify Sales EDA | 技术栈：Python + Pandas + Streamlit + Plotly | 作者：老K")
