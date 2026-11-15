"""Validate, transform, analyze and export synthetic sales records using pandas + SQLite."""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs"


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
    products = pd.read_csv(DATA / "products.csv")
    customers = pd.read_csv(DATA / "customers.csv")

    if orders["order_id"].duplicated().any():
        raise ValueError("order_id must be unique")
    if orders[["order_date", "customer_id", "product_id", "quantity", "unit_price", "discount_pct", "status"]].isna().any().any():
        raise ValueError("Unexpected null values in orders")
    if not orders["quantity"].gt(0).all() or not orders["unit_price"].ge(0).all():
        raise ValueError("Invalid quantity or price")
    if not orders["discount_pct"].between(0, 1).all():
        raise ValueError("Discount outside range 0–1")
    if not orders["status"].isin(["completed", "cancelled", "returned"]).all():
        raise ValueError("Unexpected status")
    if not orders["customer_id"].isin(customers["customer_id"]).all():
        raise ValueError("Unknown customer_id")
    if not orders["product_id"].isin(products["product_id"]).all():
        raise ValueError("Unknown product_id")

    merged = orders.merge(customers, on="customer_id", validate="many_to_one")
    merged = merged.merge(products[["product_id", "product_name", "category"]], on="product_id", validate="many_to_one")
    # Only completed orders count as revenue. Cancelled/returned orders are excluded.
    completed = merged.loc[merged["status"] == "completed"].copy()
    completed["revenue"] = (completed["quantity"] * completed["unit_price"] * (1 - completed["discount_pct"])).round(2)
    completed["month"] = completed["order_date"].dt.strftime("%Y-%m")
    completed.to_csv(OUTPUT / "sales_clean.csv", index=False)

    monthly = completed.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    monthly["revenue"] = monthly["revenue"].round(2)
    categories = completed.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), units=("quantity", "sum"))
    categories["revenue"] = categories["revenue"].round(2)
    regional = completed.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    regional["revenue"] = regional["revenue"].round(2)
    monthly.to_csv(OUTPUT / "monthly_revenue.csv", index=False)
    categories.to_csv(OUTPUT / "category_performance.csv", index=False)
    regional.to_csv(OUTPUT / "region_performance.csv", index=False)

    with sqlite3.connect(OUTPUT / "sales.sqlite") as conn:
        orders.assign(order_date=orders["order_date"].dt.strftime("%Y-%m-%d")).to_sql("orders", conn, if_exists="replace", index=False)
        customers.to_sql("customers", conn, if_exists="replace", index=False)
        products.to_sql("products", conn, if_exists="replace", index=False)
        completed.assign(order_date=completed["order_date"].dt.strftime("%Y-%m-%d")).to_sql("sales_clean", conn, if_exists="replace", index=False)

    ax = monthly.plot(x="month", y="revenue", kind="bar", legend=False, figsize=(11, 4))
    ax.set_title("Monthly Revenue — Synthetic 2025 Sales")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (BRL)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT / "monthly_revenue.png", dpi=160)
    plt.close()

    revenue = completed["revenue"].sum()
    print(f"Completed orders: {completed['order_id'].nunique()}")
    print(f"Total revenue: BRL {revenue:,.2f}")
    print(f"Average order value: BRL {revenue / completed['order_id'].nunique():,.2f}")
    print("Exports: outputs/*.csv, outputs/sales.sqlite, outputs/monthly_revenue.png")


if __name__ == "__main__":
    main()
