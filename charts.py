import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------
# REVENUE TREND CHART
# ---------------------------------------------------
def revenue_trend_chart(df):

    fig = px.line(
        df,
        x="MONTH",
        y="NET REVENUE",
        color="CITY",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Net Revenue",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# EBITDA BY STORE
# ---------------------------------------------------
def ebitda_store_chart(df):

    fig = px.bar(
        df,
        x="STORE",
        y="KITCHEN EBITDA",
        color="CITY",
        title="EBITDA by Store"
    )

    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="EBITDA",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# GROSS MARGIN CHART
# ---------------------------------------------------
def gross_margin_chart(df):

    fig = px.bar(
        df,
        x="STORE",
        y="GM_PERCENT",
        color="CITY",
        title="Gross Margin % by Store"
    )

    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="GM %",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# VARIANCE ANALYSIS CHART
# ---------------------------------------------------
def variance_chart(df):

    fig = px.bar(
        df,
        x="REVENUE COHORT",
        y="VARIANCE_PERCENT",
        color="REVENUE COHORT",
        title="Average Variance % by Revenue Cohort"
    )

    fig.update_layout(
        xaxis_title="Revenue Cohort",
        yaxis_title="Variance %",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# CITY REVENUE PIE CHART
# ---------------------------------------------------
def city_pie_chart(df):

    fig = px.pie(
        df,
        names="CITY",
        values="NET REVENUE",
        title="Revenue Contribution by City"
    )

    fig.update_layout(
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# ORDER COUNT CHART
# ---------------------------------------------------
def order_count_chart(df):

    fig = px.bar(
        df,
        x="CITY",
        y="ORDER COUNT",
        color="CITY",
        title="Order Count by City"
    )

    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Orders",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# EBITDA DISTRIBUTION
# ---------------------------------------------------
def ebitda_distribution(df):

    fig = px.histogram(
        df,
        x="KITCHEN EBITDA",
        nbins=20,
        title="EBITDA Distribution"
    )

    fig.update_layout(
        xaxis_title="EBITDA",
        yaxis_title="Frequency",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# VARIANCE DISTRIBUTION
# ---------------------------------------------------
def variance_distribution(df):

    fig = px.histogram(
        df,
        x="VARIANCE_PERCENT",
        nbins=20,
        title="Variance % Distribution"
    )

    fig.update_layout(
        xaxis_title="Variance %",
        yaxis_title="Frequency",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# REVENUE VS EBITDA SCATTER
# ---------------------------------------------------
def revenue_vs_ebitda(df):

    fig = px.scatter(
        df,
        x="NET REVENUE",
        y="KITCHEN EBITDA",
        color="CITY",
        size="ORDER COUNT",
        hover_name="STORE",
        title="Revenue vs EBITDA"
    )

    fig.update_layout(
        xaxis_title="Net Revenue",
        yaxis_title="EBITDA",
        template="plotly_white"
    )

    return fig


# ---------------------------------------------------
# TOP STORES CHART
# ---------------------------------------------------
def top_stores_chart(df):

    top_df = df.groupby("STORE")[
        "NET REVENUE"
    ].sum().reset_index()

    top_df = top_df.sort_values(
        by="NET REVENUE",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_df,
        x="STORE",
        y="NET REVENUE",
        color="NET REVENUE",
        title="Top 10 Revenue Stores"
    )

    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="Revenue",
        template="plotly_white"
    )

    return fig