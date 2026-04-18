# MoPhones Credit Intelligence Dashboard

A production-grade Streamlit dashboard analysing MoPhones' 2025 credit portfolio.
Built as part of the **Data Analyst – Product & Credit** case study.

---

## What It Does

Five interactive pages address every core business question:

| Page | Question Answered |
|------|-------------------|
| **Overview** | How is the portfolio performing right now? |
| **Portfolio Health** | How are the 5 key credit KPIs trending over time? |
| **Segment Analysis** | Which customer segments carry the most risk? |
| **Customer Experience** | What does NPS data reveal about credit-CX tension? |
| **Data Quality** | What limitations exist and what must be fixed? |
| **Recommendations** | What should MoPhones do, in what order? |

---

## Key Findings

- **PAR 30 grew from 22.9% → 32.8%** (+10pp) over 2025
- **Avg Days Past Due rose 66%** to 283 days - chronic delinquency is ageing, not resolving
- **13.6% of customers** report phone locked despite on-time payment
- **Return account NPS = -46.8** - the single largest customer experience failure
- **18–25 cohort** has the highest PAR 30 (21.3%) and FPD (7.0%)

---
## Project Structure

```
mophones-credit-dashboard/
├── app.py                  ← Main
├── requirements.txt        ← Python dependencies
├── .streamlit/
│   └── config.toml        ← Theme configuration
├── Credit Data/            ← Credit snapshot CSVs 
│   ├── Credit Data - 01-01-2025.csv
│   ├── Credit Data - 30-03-2025.csv
│   ├── Credit Data - 30-06-2025.csv
│   ├── Credit Data - 30-09-2025.csv
│   └── Credit Data - 30-12-2025.csv
├── Sales and Customer Data.xlsx   ← Demographics 
└── NPS Data.xlsx                  ← NPS survey 
```

## Tech Stack

- **Streamlit** - dashboard framework
- **Plotly** - interactive charts
- **Pandas / NumPy** - data processing

---

## Data Sources

| Dataset | Records | Description |
|---------|---------|-------------|
| Credit Data | 5 snapshots, 8,935–20,742 rows | Quarterly portfolio positions |
| Sales & Customer Data | 20,747 sales, ~50K demographic | Customer demographics & income |
| NPS Survey | 4,129 responses | Customer satisfaction data |

---

*MoPhones  · 2025*
