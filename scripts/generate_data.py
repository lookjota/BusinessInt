"""Create reproducible, clearly synthetic sales data for a portfolio exercise."""
from pathlib import Path
import csv
from datetime import date, timedelta
import random

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main() -> None:
    DATA.mkdir(exist_ok=True)
    rng = random.Random(42)
    regions = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    products = [
        (101, "Notebook", "Eletronicos", 3200.00),
        (102, "Mouse", "Acessorios", 85.00),
        (103, "Teclado", "Acessorios", 175.00),
        (104, "Monitor", "Eletronicos", 950.00),
        (105, "Headset", "Acessorios", 245.00),
        (106, "Webcam", "Eletronicos", 310.00),
    ]
    customers = [(i, f"Cliente {i:03d}", rng.choice(regions)) for i in range(1, 151)]
    with (DATA / "customers.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["customer_id", "customer_name", "region"])
        writer.writerows(customers)
    with (DATA / "products.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["product_id", "product_name", "category", "list_price"])
        writer.writerows(products)

    start = date(2025, 1, 1)
    with (DATA / "orders.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price", "discount_pct", "status"])
        for order_id in range(1, 1201):
            customer = rng.choice(customers)
            product = rng.choice(products)
            day = start + timedelta(days=rng.randrange(365))
            quantity = rng.randint(1, 4)
            discount = rng.choice([0, 0, 0, 0.05, 0.10, 0.15])
            status = rng.choices(["completed", "cancelled", "returned"], weights=[90, 6, 4])[0]
            writer.writerow([order_id, day.isoformat(), customer[0], product[0], quantity, f"{product[3]:.2f}", f"{discount:.2f}", status])
    print("Created 3 synthetic datasets in data/ (2025, 1200 orders)")


if __name__ == "__main__":
    main()
