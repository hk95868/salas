"""数据加载与预处理模块"""
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(filepath="sales_data.csv") -> pd.DataFrame:
    """加载CSV数据并进行预处理"""
    df = pd.read_csv(filepath)
    df = preprocess(df)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """数据预处理：类型转换、特征工程"""
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["Month"] = df["order_date"].dt.to_period("M").astype(str)
    df["Year"] = df["order_date"].dt.year
    df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(2)
    df["discount_level"] = pd.cut(
        df["discount_percent"],
        bins=[0, 10, 20, 30, 50, 100],
        labels=["0-10%", "10-20%", "20-30%", "30-50%", "50%+"],
    )
    return df


def filter_data(df: pd.DataFrame, categories, countries, sources) -> pd.DataFrame:
    """根据筛选条件过滤数据"""
    return df[
        (df["product_category"].isin(categories))
        & (df["customer_country"].isin(countries))
        & (df["traffic_source"].isin(sources))
    ]
