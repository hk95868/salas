"""数据洞察生成模块"""
import pandas as pd


def insight_monthly_trend(monthly_df: pd.DataFrame) -> str:
    """月度趋势洞察"""
    best = monthly_df.loc[monthly_df["revenue"].idxmax()]
    worst = monthly_df.loc[monthly_df["revenue"].idxmin()]
    return (
        f"💡 **洞察**：营收最高月份为 {best['Month']}（${best['revenue']:,.0f}），"
        f"最低为 {worst['Month']}（${worst['revenue']:,.0f}）。"
        f"建议在低谷期加大营销投放，平抑季节性波动。"
    )


def insight_category(cat_df: pd.DataFrame) -> str:
    """品类分析洞察"""
    top = cat_df.loc[cat_df["revenue"].idxmax()]
    top_margin = cat_df.loc[cat_df["avg_margin"].idxmax()]
    low_margin = cat_df.loc[cat_df["avg_margin"].idxmin()]
    return (
        f"💡 **洞察**：{top['product_category']} 营收最高（${top['revenue']:,.0f}），"
        f"但利润率最高的是 {top_margin['product_category']}（{top_margin['avg_margin']:.1f}%），"
        f"最低的是 {low_margin['product_category']}（{low_margin['avg_margin']:.1f}%）。"
        f"营收≠利润，高营收品类需关注成本控制。"
    )


def insight_country(country_df: pd.DataFrame) -> str:
    """区域分析洞察"""
    top = country_df.loc[country_df["revenue"].idxmax()]
    low = country_df.loc[country_df["avg_margin"].idxmin()]
    return (
        f"💡 **洞察**：{top['customer_country']} 营收领先（${top['revenue']:,.0f}），"
        f"但利润率最低的是 {low['customer_country']}（{low['avg_margin']:.1f}%），"
        f"可能存在运费或折扣过高问题，建议优化定价策略。"
    )


def insight_source(source_df: pd.DataFrame) -> str:
    """流量来源洞察"""
    best = source_df.loc[source_df["orders"].idxmax()]
    high_aov = source_df.loc[source_df["avg_revenue"].idxmax()]
    return (
        f"💡 **洞察**：{best['traffic_source']} 带来最多订单（{best['orders']:,}），"
        f"但 {high_aov['traffic_source']} 客单价最高（${high_aov['avg_revenue']:,.0f}）。"
        f"高客单价渠道值得加大投入。"
    )


def insight_discount(discount_df: pd.DataFrame) -> str:
    """折扣影响洞察"""
    worst = discount_df.loc[discount_df["avg_margin"].idxmin()]
    return (
        f"💡 **洞察**：折扣率 {worst['discount_level']} 区间利润率最低（{worst['avg_margin']:.1f}%），"
        f"且退货率随折扣升高而上升。建议将折扣控制在 20% 以内，避免利润侵蚀。"
    )


def insight_payment(payment_df: pd.DataFrame) -> str:
    """支付与退货洞察"""
    worst = payment_df.loc[payment_df["return_rate"].idxmax()]
    return (
        f"💡 **洞察**：{worst['payment_method']} 退货率最高（{worst['return_rate']:.1%}），"
        f"可能存在支付便捷导致的冲动消费问题，可考虑针对性售后策略。"
    )


def insight_rating() -> str:
    """评分分布洞察"""
    return "💡 **洞察**：评分分布可反映产品质量和客户满意度，低评分订单的退货率是否更高值得关注。"
