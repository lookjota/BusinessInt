


"""Interactive Business Intelligence dashboard using prepared analytical data."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "outputs" / "sales_clean.csv"

st.set_page_config(
    page_title="Sales BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Sales Business Intelligence Dashboard")
st.caption("Portfolio demonstration · Synthetic data · 2025 · Currency: BRL")

if not SOURCE.exists():
    st.error("Missing processed data. Run `python scripts/generate_data.py` and `python scripts/analyze.py` from the project root.")
    st.stop()

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(SOURCE, parse_dates=["order_date"])

df = load_data()
regions = sorted(df["region"].unique())
categories = sorted(df["category"].unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
filtered = df[df["region"].isin(selected_regions) & df["category"].isin(selected_categories)].copy()

total_revenue = filtered["revenue"].sum()

revenue_display = (
    f"R$ {total_revenue / 1_000_000:,.2f} mi"
    if total_revenue >= 1_000_000
    else f"R$ {total_revenue:,.2f}"
)

orders = filtered["order_id"].nunique()

units = filtered["quantity"].sum()
clients = filtered["customer_id"].nunique()
c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue (BRL)", revenue_display)
c2.metric("Orders", f"{orders:,}")
c3.metric(
    "Average order value",
    f"R$ {total_revenue / orders:,.2f}" if orders else "R$ 0.00"
)
c4.metric("Customers", f"{clients:,}")

if filtered.empty:
    st.info("No sales match the selected filters.")
    st.stop()

filtered["month"] = filtered["order_date"].dt.strftime("%Y-%m")
monthly = filtered.groupby("month", as_index=False)["revenue"].sum().sort_values("month")
by_category = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
by_region = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)

left, right = st.columns(2)
with left:
    st.plotly_chart(px.line(monthly, x="month", y="revenue", markers=True, title="Monthly revenue"), width="stretch")
    st.plotly_chart(px.bar(by_region, x="region", y="revenue", title="Revenue by region"), width="stretch")
with right:
    st.plotly_chart(px.bar(by_category, x="category", y="revenue", title="Revenue by category"), width="stretch")
    st.plotly_chart(px.bar(filtered.groupby("product_name", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False), x="product_name", y="revenue", title="Revenue by product"), width="stretch")

# Dynamic Business Insights
st.subheader("Business Insights")

if not filtered.empty:
    total_revenue = filtered["revenue"].sum()

    revenue_by_region = (
        filtered.groupby("region")["revenue"].sum()
    )

    revenue_by_product = (
        filtered.groupby("product_name")["revenue"].sum()
    )

    top_region = revenue_by_region.idxmax()
    top_product = revenue_by_product.idxmax()

    region_share = (
        revenue_by_region.max() / total_revenue * 100
        if total_revenue > 0 else 0
    )

    product_share = (
        revenue_by_product.max() / total_revenue * 100
        if total_revenue > 0 else 0
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Top-performing region",
            top_region,
            f"{region_share:.1f}% of total revenue",
            delta_color="off",
        )

    with col2:
        st.metric(
            "Highest-revenue product",
            top_product,
            f"{product_share:.1f}% of total revenue",
            delta_color="off",
        )
else:
    st.warning("No sales data available for the selected filters.")



st.subheader("Sales records")

display_df = filtered[
    [
        "order_id",
        "order_date",
        "region",
        "category",
        "product_name",
        "quantity",
        "revenue",
    ]
].copy()

display_df["order_date"] = (
    pd.to_datetime(display_df["order_date"])
    .dt.strftime("%d/%m/%Y")
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True,
    column_config={
        "order_id": "Order ID",
        "order_date": "Date",
        "region": "Region",
        "category": "Category",
        "product_name": "Product",
        "quantity": "Quantity",
        "revenue": st.column_config.NumberColumn(
            "Revenue (BRL)",
            format="R$ %.2f",
        ),
    },
)

# Monthly Revenue Growth Analysis
st.subheader("Monthly Revenue Growth")

if not filtered.empty:
    monthly_growth = (
        filtered.assign(
            month=pd.to_datetime(
                filtered["order_date"]
            ).dt.to_period("M")
        )
        .groupby("month")["revenue"]
        .sum()
        .sort_index()
    )

    monthly_growth_pct = (
        monthly_growth.pct_change() * 100
    )

    latest_month = monthly_growth.index[-1]
    latest_revenue = monthly_growth.iloc[-1]
    latest_growth = monthly_growth_pct.iloc[-1]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Latest month revenue",
            f"R$ {latest_revenue:,.2f}"
        )

    with col2:
        st.metric(
            "Month-over-Month Growth",
            f"{latest_growth:+.2f}%"
            if pd.notna(latest_growth)
            else "N/A"
        )
else:
    st.info("No monthly sales data available.")


st.download_button("Export filtered sales (.csv)", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales.csv", "text/csv")
