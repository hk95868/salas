"""图表生成模块"""
import pandas as pd
import plotly.express as px


# ========== 配色方案 ==========
COLORS = {
    "primary": "#4F46E5",
    "profit": "#10B981",
    "category_palette": px.colors.qualitative.Set2,
}


def chart_monthly_trend(monthly_df: pd.DataFrame):
    """月度营收与利润趋势折线图"""
    fig = px.line(
        monthly_df,
        x="Month",
        y=["revenue", "profit"],
        markers=True,
        labels={"value": "金额 ($)", "variable": "指标"},
        color_discrete_map={"revenue": COLORS["primary"], "profit": COLORS["profit"]},
    )
    return fig


def chart_category_pie(cat_df: pd.DataFrame):
    """品类营收占比环形图"""
    fig = px.pie(cat_df, values="revenue", names="product_category", hole=0.4, title="营收占比")
    return fig


def chart_category_margin(cat_df: pd.DataFrame):
    """品类平均利润率柱状图"""
    fig = px.bar(
        cat_df, x="product_category", y="avg_margin",
        color="product_category", title="平均利润率 (%)",
    )
    fig.update_layout(xaxis_title="品类", yaxis_title="利润率 (%)")
    return fig


def chart_country_bar(country_df: pd.DataFrame):
    """各国营收柱状图"""
    fig = px.bar(
        country_df, x="customer_country", y="revenue",
        color="customer_country", title="各国营收",
    )
    fig.update_layout(xaxis_title="国家", yaxis_title="营收 ($)")
    return fig


def chart_source_orders(source_df: pd.DataFrame):
    """流量来源订单量柱状图"""
    fig = px.bar(
        source_df, x="traffic_source", y="orders",
        color="traffic_source", title="各来源订单量",
    )
    return fig


def chart_source_aov(source_df: pd.DataFrame):
    """流量来源平均客单价柱状图"""
    fig = px.bar(
        source_df, x="traffic_source", y="avg_revenue",
        color="traffic_source", title="各来源平均客单价",
    )
    return fig


def chart_discount_scatter(df: pd.DataFrame):
    """折扣率 vs 利润率散点图"""
    fig = px.scatter(
        df, x="discount_percent", y="profit_margin",
        color="product_category", opacity=0.3,
        labels={"discount_percent": "折扣率 (%)", "profit_margin": "利润率 (%)"},
    )
    return fig


def chart_payment_pie(payment_df: pd.DataFrame):
    """支付方式分布环形图"""
    fig = px.pie(payment_df, values="orders", names="payment_method", hole=0.4, title="支付方式分布")
    return fig


def chart_payment_return(payment_df: pd.DataFrame):
    """各支付方式退货率柱状图"""
    fig = px.bar(
        payment_df, x="payment_method", y="return_rate",
        color="payment_method", title="各支付方式退货率",
    )
    fig.update_layout(yaxis_tickformat=".1%", yaxis_title="退货率")
    return fig


def chart_rating_hist(df: pd.DataFrame):
    """评分分布直方图"""
    fig = px.histogram(df, x="rating", nbins=20, title="评分分布")
    fig.update_layout(xaxis_title="评分", yaxis_title="订单数")
    return fig


def chart_rating_revenue(rating_df: pd.DataFrame):
    """不同评分区间的平均营收柱状图"""
    fig = px.bar(rating_df, x="rating_range", y="avg_revenue", title="不同评分区间的平均营收")
    return fig
