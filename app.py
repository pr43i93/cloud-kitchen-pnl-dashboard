import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Cloud Kitchen Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    color: #ff4b4b;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    # READ EXCEL FILE WITH CORRECT HEADER
    df = pd.read_excel(
       "Kittchen PNL Data.xlsx",
        header=1
    )

    # CLEAN COLUMN NAMES
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
    )

    return df


df = load_data()

# ---------------------------------------------------
# CREATE METRICS
# ---------------------------------------------------

# Gross Margin %
df["GM_PERCENT"] = (
    df["GROSS_MARGIN"] / df["NET_REVENUE"]
) * 100

# EBITDA %
df["EBITDA_PERCENT"] = (
    df["KITCHEN_EBITDA"] / df["NET_REVENUE"]
) * 100

# Variance %
df["VARIANCE_PERCENT"] = (
    df["VARIANCE"] / df["NET_REVENUE"]
) * 100

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


df["VARIANCE_CATEGORY"] = df[
    "VARIANCE_PERCENT"
].apply(variance_bucket)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.title("Dashboard Filters")

# City Filter
city_filter = st.sidebar.multiselect(
    "Select City",
    options=df["CITY"].unique(),
    default=df["CITY"].unique()
)

# Store Filter
store_filter = st.sidebar.multiselect(
    "Select Store",
    options=df["STORE"].unique(),
    default=df["STORE"].unique()
)

# Month Filter
month_filter = st.sidebar.multiselect(
    "Select Month",
    options=df["MONTH"].unique(),
    default=df["MONTH"].unique()
)

# Revenue Cohort Filter
revenue_filter = st.sidebar.multiselect(
    "Revenue Cohort",
    options=df["REVENUE_COHORT"].unique(),
    default=df["REVENUE_COHORT"].unique()
)

# EBITDA Category Filter
ebitda_filter = st.sidebar.multiselect(
    "EBITDA Category",
    options=df["EBITDA_CATEGORY"].unique(),
    default=df["EBITDA_CATEGORY"].unique()
)

# EBITDA Range Slider
min_ebitda = int(df["KITCHEN_EBITDA"].min())
max_ebitda = int(df["KITCHEN_EBITDA"].max())

ebitda_range = st.sidebar.slider(
    "EBITDA Range",
    min_ebitda,
    max_ebitda,
    (min_ebitda, max_ebitda)
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df[
    (df["CITY"].isin(city_filter)) &
    (df["STORE"].isin(store_filter)) &
    (df["MONTH"].isin(month_filter)) &
    (df["REVENUE_COHORT"].isin(revenue_filter)) &
    (df["EBITDA_CATEGORY"].isin(ebitda_filter)) &
    (df["KITCHEN_EBITDA"] >= ebitda_range[0]) &
    (df["KITCHEN_EBITDA"] <= ebitda_range[1])
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("Cloud Kitchen PNL Dashboard")

st.markdown("""
Interactive Dashboard for:
- Kitchen Level PNL
- Variance Analysis
- Revenue Insights
- EBITDA Performance
""")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Revenue
col1.metric(
    "Total Revenue",
    f"₹ {filtered_df['NET_REVENUE'].sum():,.0f}"
)

# Gross Margin
col2.metric(
    "Gross Margin",
    f"₹ {filtered_df['GROSS_MARGIN'].sum():,.0f}"
)

# EBITDA
col3.metric(
    "Total EBITDA",
    f"₹ {filtered_df['KITCHEN_EBITDA'].sum():,.0f}"
)

# Orders
col4.metric(
    "Order Count",
    f"{filtered_df['ORDER_COUNT'].sum():,.0f}"
)

# ---------------------------------------------------
# TOP STORE
# ---------------------------------------------------
top_store = filtered_df.groupby(
    "STORE"
)["NET_REVENUE"].sum().idxmax()

st.success(f"Top Revenue Store: {top_store}")

# ---------------------------------------------------
# REVENUE TREND
# ---------------------------------------------------
st.subheader("Monthly Revenue Trend")

revenue_chart = px.line(
    filtered_df,
    x="MONTH",
    y="NET_REVENUE",
    color="CITY",
    markers=True,
    title="Revenue Trend by City"
)

st.plotly_chart(
    revenue_chart,
    use_container_width=True
)

# ---------------------------------------------------
# EBITDA BY STORE
# ---------------------------------------------------
st.subheader("EBITDA by Store")

ebitda_chart = px.bar(
    filtered_df,
    x="STORE",
    y="KITCHEN_EBITDA",
    color="CITY",
    title="Store-wise EBITDA"
)

st.plotly_chart(
    ebitda_chart,
    use_container_width=True
)

# ---------------------------------------------------
# GROSS MARGIN ANALYSIS
# ---------------------------------------------------
st.subheader("Gross Margin Analysis")

gm_chart = px.bar(
    filtered_df,
    x="STORE",
    y="GM_PERCENT",
    color="CITY",
    title="Gross Margin % by Store"
)

st.plotly_chart(
    gm_chart,
    use_container_width=True
)

# ---------------------------------------------------
# VARIANCE ANALYSIS
# ---------------------------------------------------
st.subheader("Variance Analysis Dashboard")

variance_summary = filtered_df.groupby(
    "REVENUE_COHORT"
)["VARIANCE_PERCENT"].mean().reset_index()

variance_chart = px.bar(
    variance_summary,
    x="REVENUE_COHORT",
    y="VARIANCE_PERCENT",
    color="REVENUE_COHORT",
    title="Average Variance % by Revenue Cohort"
)

st.plotly_chart(
    variance_chart,
    use_container_width=True
)

# ---------------------------------------------------
# STORE COUNT PIVOT
# ---------------------------------------------------
st.subheader("Store Count by Variance Category")

pivot_table = pd.pivot_table(
    filtered_df,
    values="STORE",
    index="VARIANCE_CATEGORY",
    columns="MONTH",
    aggfunc="count",
    fill_value=0
)

st.dataframe(
    pivot_table,
    use_container_width=True
)

# ---------------------------------------------------
# CITY PERFORMANCE
# ---------------------------------------------------
st.subheader("City Performance")

city_summary = filtered_df.groupby("CITY")[
    ["NET_REVENUE",
     "GROSS_MARGIN",
     "KITCHEN_EBITDA"]
].sum().reset_index()

city_chart = px.pie(
    city_summary,
    names="CITY",
    values="NET_REVENUE",
    title="Revenue Contribution by City"
)

st.plotly_chart(
    city_chart,
    use_container_width=True
)

# ---------------------------------------------------
# REVENUE VS EBITDA
# ---------------------------------------------------
st.subheader("Revenue vs EBITDA")

scatter_chart = px.scatter(
    filtered_df,
    x="NET_REVENUE",
    y="KITCHEN_EBITDA",
    color="CITY",
    size="ORDER_COUNT",
    hover_name="STORE",
    title="Revenue vs EBITDA"
)

st.plotly_chart(
    scatter_chart,
    use_container_width=True
)

# ---------------------------------------------------
# FULL DATA TABLE
# ---------------------------------------------------
st.subheader("Detailed Kitchen Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_kitchen_data.csv',
    mime='text/csv',
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown("""
### Dashboard Developed Using:
- Streamlit
- Plotly
- Pandas
- Python

### Features:
- Kitchen Level PNL
- Variance Dashboard
- Revenue Analysis
- EBITDA Tracking
- Interactive Filters
""")
