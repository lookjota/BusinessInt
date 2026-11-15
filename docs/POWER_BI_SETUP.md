# Commercial KPI Dashboard — Power BI setup

The interactive dashboard is published at `docs/index.html`. The source dataset lives at `outputs/sales_clean.csv` in this repository. This file is a Power BI implementation guide, **not a claim that a native PBIX file is included**.

## Import
1. Download `outputs/sales_clean.csv` locally.
2. Power BI Desktop: Home > Get Data > Text/CSV.
3. Name imported table `Sales`.
4. Convert `order_date` to Date, `revenue` to Decimal Number, `quantity` to Whole Number and `customer_id` to Whole Number.

## Measures

```dax
Total Revenue = SUM(Sales[revenue])
Completed Orders = DISTINCTCOUNT(Sales[order_id])
Average Ticket = DIVIDE([Total Revenue], [Completed Orders])
Customers = DISTINCTCOUNT(Sales[customer_id])
Units Sold = SUM(Sales[quantity])
```

Create a calendar table:

```dax
Calendar = CALENDAR(MIN(Sales[order_date]), MAX(Sales[order_date]))
YearMonthSort = YEAR('Calendar'[Date]) * 100 + MONTH('Calendar'[Date])
MonthYear = FORMAT('Calendar'[Date], "MMM yyyy")
Previous Month Revenue = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
MoM Growth % = DIVIDE([Total Revenue] - [Previous Month Revenue], [Previous Month Revenue])
```

Sort the MonthYear label using YearMonthSort. Relate Calendar[Date] to Sales[order_date] and mark the Calendar table as a date table. Add cards, a monthly line chart, regional bars, product ranking, category breakdown, and date / region / category slicers.

The dataset is synthetic and intended only for portfolio demonstration.
