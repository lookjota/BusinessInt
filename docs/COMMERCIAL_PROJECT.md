# Commercial Performance Dashboard — Project 02

**Live source**: [Interactive static dashboard](index.html) · **Power BI**: [Setup and DAX](POWER_BI_SETUP.md) · **Data**: [Synthetic cleaned sales](../outputs/sales_clean.csv)

## Scope
A separate commercial indicators project built on the same dataset as Sales Data Analysis. The Excel workbook is available as an accompanying downloadable portfolio artifact; the GitHub-hosted static dashboard is written in vanilla JS + SVG and requires no backend.

### KPIs
| Metric | Value |
|---|---:|
| Revenue | R$ 2,288,963.75 |
| Completed sales | 1,086 |
| Average order | R$ 2,107.70 |
| Customers | 150 |
| Best region | Sul — 22.6% |
| Top revenue product | Notebook — 65.5% |
| December MoM growth | +11.27% |

### Features
- Filter by region, product category, or month
- Track revenue, orders, average ticket, customer counts
- Explore monthly trend, category, region, and product breakdowns
- Export filtered records to CSV
- Run without server or credentials

### Limitations
- Synthetic training data; no real organization performance
- No native PBIX file is included; the DAX guide helps reproduce the model in Power BI
- Data is shipped embedded in the static HTML; edit the source and republish to refresh
