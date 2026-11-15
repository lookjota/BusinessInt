import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "sales.sqlite"
)


def test_sql_matches_pandas():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM sales_clean",
            conn,
        )

        sql_result = conn.execute("""
            SELECT
                SUM(revenue),
                COUNT(DISTINCT order_id)
            FROM sales_clean
        """).fetchone()

    sql_revenue, sql_orders = sql_result

    pandas_revenue = df["revenue"].sum()
    pandas_orders = df["order_id"].nunique()

    assert abs(sql_revenue - pandas_revenue) < 0.01
    assert sql_orders == pandas_orders


def test_sales_data_quality():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT * FROM sales_clean",
            conn,
        )

    assert not df.empty
    assert df["order_id"].notna().all()
    assert df["revenue"].notna().all()
    assert (df["revenue"] >= 0).all()
    assert not df["order_id"].duplicated().any()
