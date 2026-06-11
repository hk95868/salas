"""聚合计算模块"""
import pandas as pd


def calc_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """月度营收、利润、订单聚合"""
    return (
        df.groupby("Month")
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "count"))
        .reset_index()
    )


def calc_category(df: pd.DataFrame) -> pd.DataFrame:
    """品类营收、利润、订单、平均利润率聚合"""
    return (
        df.groupby("product_category")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "count"),
            avg_margin=("profit_margin", "mean"),
        )
        .reset_index()
    )


def calc_country(df: pd.DataFrame) -> pd.DataFrame:
    """国家营收、利润、订单、平均利润率聚合"""
    return (
        df.groupby("customer_country")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "count"),
            avg_margin=("profit_margin", "mean"),
        )
        .reset_index()
    )


def calc_source(df: pd.DataFrame) -> pd.DataFrame:
    """流量来源营收、订单、平均客单价聚合"""
    return (
        df.groupby("traffic_source")
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"), avg_revenue=("revenue", "mean"))
        .reset_index()
    )


def calc_discount_impact(df: pd.DataFrame) -> pd.DataFrame:
    """折扣分段：利润率、退货率、订单数"""
    return (
        df.groupby("discount_level", observed=True)
        .agg(avg_margin=("profit_margin", "mean"), return_rate=("is_returned", "mean"), orders=("order_id", "count"))
        .reset_index()
    )


def calc_payment(df: pd.DataFrame) -> pd.DataFrame:
    """支付方式：订单数、退货率"""
    return (
        df.groupby("payment_method")
        .agg(orders=("order_id", "count"), return_rate=("is_returned", "mean"))
        .reset_index()
    )


def calc_rating_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """评分区间平均营收"""
    result = df.groupby(pd.cut(df["rating"], bins=[0, 2, 3, 4, 5]))["revenue"].mean().reset_index()
    result.columns = ["rating_range", "avg_revenue"]
    result["rating_range"] = result["rating_range"].astype(str)
    return result
