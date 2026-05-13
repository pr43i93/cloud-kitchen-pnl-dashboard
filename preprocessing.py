import pandas as pd
import numpy as np


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
def load_data(file_path):

    df = pd.read_excel(file_path)

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    return df


# ---------------------------------------------------
# CREATE PERCENTAGE METRICS
# ---------------------------------------------------
def create_metrics(df):

    # Gross Margin %
    df["GM_PERCENT"] = (
        df["GROSS MARGIN"] / df["NET REVENUE"]
    ) * 100

    # EBITDA %
    df["EBITDA_PERCENT"] = (
        df["KITCHEN EBITDA"] / df["NET REVENUE"]
    ) * 100

    # Variance %
    df["VARIANCE_PERCENT"] = (
        df["VARIANCE"] / df["NET REVENUE"]
    ) * 100

    return df


# ---------------------------------------------------
# VARIANCE CATEGORY
# ---------------------------------------------------
def variance_bucket(x):

    if x < 2:
        return "Below 2%"

    elif x < 3:
        return "2% to 3%"

    elif x < 5:
        return "3% to 5%"

    else:
        return "Above 5%"


# ---------------------------------------------------
# APPLY VARIANCE CATEGORY
# ---------------------------------------------------
def apply_variance_category(df):

    df["VARIANCE_CATEGORY"] = df[
        "VARIANCE_PERCENT"
    ].apply(variance_bucket)

    return df


# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
def filter_data(
    df,
    city_filter,
    store_filter,
    month_filter,
    revenue_filter,
    ebitda_filter,
    ebitda_range
):

    filtered_df = df[
        (df["CITY"].isin(city_filter)) &
        (df["STORE"].isin(store_filter)) &
        (df["MONTH"].isin(month_filter)) &
        (df["REVENUE COHORT"].isin(revenue_filter)) &
        (df["EBITDA CATEGORY"].isin(ebitda_filter)) &
        (df["KITCHEN EBITDA"] >= ebitda_range[0]) &
        (df["KITCHEN EBITDA"] <= ebitda_range[1])
    ]

    return filtered_df


# ---------------------------------------------------
# KPI SUMMARY
# ---------------------------------------------------
def calculate_kpis(df):

    total_revenue = df["NET REVENUE"].sum()

    total_gm = df["GROSS MARGIN"].sum()

    total_ebitda = df["KITCHEN EBITDA"].sum()

    total_orders = df["ORDER COUNT"].sum()

    return {
        "revenue": total_revenue,
        "gross_margin": total_gm,
        "ebitda": total_ebitda,
        "orders": total_orders
    }


# ---------------------------------------------------
# CITY SUMMARY
# ---------------------------------------------------
def city_summary(df):

    summary = df.groupby("CITY")[
        ["NET REVENUE",
         "GROSS MARGIN",
         "KITCHEN EBITDA"]
    ].sum().reset_index()

    return summary


# ---------------------------------------------------
# STORE SUMMARY
# ---------------------------------------------------
def store_summary(df):

    summary = df.groupby("STORE")[
        ["NET REVENUE",
         "KITCHEN EBITDA",
         "ORDER COUNT"]
    ].sum().reset_index()

    return summary


# ---------------------------------------------------
# VARIANCE SUMMARY
# ---------------------------------------------------
def variance_summary(df):

    summary = df.groupby(
        "REVENUE COHORT"
    )["VARIANCE_PERCENT"].mean().reset_index()

    return summary


# ---------------------------------------------------
# PIVOT TABLE
# ---------------------------------------------------
def variance_pivot(df):

    pivot = pd.pivot_table(
        df,
        values="STORE",
        index="VARIANCE_CATEGORY",
        columns="MONTH",
        aggfunc="count",
        fill_value=0
    )

    return pivot