# International Finance Analysis: South Korea ↔ Switzerland
**Currency Pair Analysis: KRW/CHF**

A Python-based analytical toolkit for analyzing the economic and currency relationship between **South Korea (KRW)** and **Switzerland (CHF)**. This project focuses on data collection, processing, visualization, and report generation using APIs and Python libraries.

---

## Project Overview

This toolkit performs comprehensive currency analysis including:

### Part A: Country Selection Justification
- Trade relationship analysis (bilateral trade: $5.2B annually)
- Economic profile comparison (Korea: high-tech exporter, Swiss: safe haven)
- Strategic importance for semiconductor supply chains

### Part B: Exchange Rate Analysis
- Historical vs current KRW/CHF rates
- Percentage change calculation
- Impact on exporters (Samsung, Hyundai) and importers (pharmaceutical distributors)

### Part C: Parity Conditions
- **Interest Rate Parity (IRP)**: Forward rate calculation with Korea (3.25%) vs Swiss (1.25%) rates
- **Purchasing Power Parity (PPP)**: Expected rate based on inflation differentials

### Part D: Policy Analysis
- Safe haven squeeze risks for KRW
- Imported inflation challenges
- Policy recommendation: SME Forex Liquidity Facility

### Part E: Stakeholder Implications
- Korean chaebols (conglomerates)
- Small and medium enterprises (SMEs)
- Central bank (Bank of Korea)
- Forex traders

---

## Quick Start

### 1. Clone/Download Project

```bash
cd /Users/amaanrahman/Finance
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv ifm_env

# Activate virtual environment
source ifm_env/bin/activate  # On Mac/Linux
# OR
ifm_env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Complete Analysis

```bash
# Run the full analysis (generates PDF, PowerPoint, charts)
python complete_analysis.py
```

**Expected Output:**
- PDF Report: `outputs/reports/Korea_Switzerland_IFM_Analysis.pdf`
- PowerPoint: `outputs/presentations/Korea_Switzerland_Analysis.pptx`
- Excel Data: `outputs/excel/analysis_results.xlsx`
- Charts: `outputs/charts/` (PNG files)

### 4. Explore with Jupyter Notebooks (Optional)

```bash
# Start Jupyter
jupyter notebook

# Open any notebook in notebooks/ folder
```

---

## 📁 Project Structure

```
Finance/
├── complete_analysis.py          # Main analysis script (run this!)
├── config.py                      # Configuration (API keys, dates, rates)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── src/                           # Core modules
│   ├── __init__.py
│   ├── data_fetchers.py          # Fetch KRW/CHF rates, interest rates, inflation
│   ├── calculators.py            # IRP, PPP, exchange rate calculations
│   ├── visualizers.py            # Charts (matplotlib, plotly)
│   └── report_generator.py       # PDF and PowerPoint generation
│
├── notebooks/                     # Jupyter notebooks (step-by-step analysis)
│   ├── 01_data_collection.ipynb
│   ├── 02_part_a_country_analysis.ipynb
│   ├── 03_part_b_exchange_rate.ipynb
│   ├── 04_part_c_parity_conditions.ipynb
│   ├── 05_part_d_policy_analysis.ipynb
│   └── 06_part_e_final_report.ipynb
│
├── data/                          # Data storage
│   ├── raw/                       # Raw API responses
│   ├── processed/                 # Cleaned data
│   └── cache/                     # Cached API calls
│
└── outputs/                       # Generated reports and charts
    ├── charts/                    # PNG/HTML charts
    ├── reports/                   # PDF reports
    ├── presentations/             # PowerPoint files
    └── excel/                     # Excel workbooks
```

---

## Configuration

### API Keys (Optional - Works Without Them!)

The project uses **FREE** data sources by default:

1. **yfinance** (NO API KEY REQUIRED)  - For KRW/CHF exchange rates
2. **Manual rates** - For interest rates and inflation

**Optional upgrades** (if you want better data quality):

Edit `config.py`:

```python
# Alpha Vantage (better forex data)
ALPHAVANTAGE_API_KEY = "your_key_here"  # Get from: alphavantage.co

# FRED (for interest rate data from Federal Reserve)
FRED_API_KEY = "your_key_here"          # Get from: fred.stlouisfed.org
```

### Date Range & Currency Pair

Edit `config.py`:

```python
# Analysis period
START_DATE = datetime(2025, 8, 1)
END_DATE = datetime(2026, 1, 30)

# Currency pair
BASE_CURRENCY = 'KRW'      # South Korean Won
TARGET_CURRENCY = 'CHF'    # Swiss Franc
```

### Interest & Inflation Rates

Edit `config.py`:

```python
INTEREST_RATES = {
    'KRW': 0.0325,  # 3.25% - Bank of Korea
    'CHF': 0.0125,  # 1.25% - Swiss National Bank
}

INFLATION_RATES = {
    'KRW': 0.023,   # 2.3% - Korea
    'CHF': 0.014,   # 1.4% - Switzerland
}
```

---

##  Key Outputs

### 1. PDF Report
**File:** `outputs/reports/Korea_Switzerland_IFM_Analysis.pdf`

Professional report with:
- Executive summary
- Part A: Why Switzerland matters for Korea
- Part B: Exchange rate analysis with charts
- Part C: IRP and PPP calculations with formulas
- Part D: Policy recommendations
- Part E: Stakeholder impact tables

### 2. PowerPoint Presentation
**File:** `outputs/presentations/Korea_Switzerland_Analysis.pptx`

10-slide presentation including:
- Title slide
- Country selection justification
- Exchange rate trend charts
- Stakeholder impact analysis (winners/losers)
- IRP and PPP results
- Policy recommendations
- Conclusions

### 3. Excel Workbook
**File:** `outputs/excel/analysis_results.xlsx`

Two sheets:
- **Summary**: All calculated metrics (rates, changes, IRP, PPP)
- **Exchange Rates**: Full 6-month KRW/CHF time series data

### 4. Charts
**Location:** `outputs/charts/`

- `exchange_rate_analysis.png` - Time series with moving average
- `volatility_analysis.png` - Rolling volatility and return distribution
- `stakeholder_impact.png` - Bar chart showing impact on different groups
- `rate_comparison.png` - Historical, current, IRP, PPP rates
- `interactive_krw_chf.html` - Interactive Plotly chart (hover for details)

---

## Module Usage Examples

### Example 1: Fetch Data Only

```python
from src.data_fetchers import fetch_all_korea_switzerland_data

# Get all data with one function call
data = fetch_all_korea_switzerland_data(
    start_date='2025-08-01',
    end_date='2026-01-30'
)

print(f"Fetched {len(data['forex_data'])} days of KRW/CHF data")
print(f"Korea interest rate: {data['interest_rates']['KRW']*100}%")
```

### Example 2: Calculate IRP

```python
from src.calculators import ParityCalculator

calc = ParityCalculator()
result = calc.interest_rate_parity(
    spot_rate=0.00062,        # Current rate
    domestic_rate=0.0325,     # Korea 3.25%
    foreign_rate=0.0125       # Swiss 1.25%
)

print(f"Forward rate: {result['forward_rate']:.6f}")
print(f"Expected change: {result['implied_change_pct']:.2f}%")
print(result['interpretation'])
```

### Example 3: Create Visualizations

```python
from src.visualizers import ForexVisualizer
import pandas as pd

visualizer = ForexVisualizer()

# Assuming you have forex_data DataFrame
visualizer.plot_exchange_rate_time_series(
    forex_data, 'KRW', 'CHF',
    save_path='my_chart.png'
)
```

### Example 4: Generate PDF Report

```python
from src.report_generator import PDFReportGenerator

pdf = PDFReportGenerator('my_report.pdf')
pdf.add_title("Custom Korea-Switzerland Analysis")
pdf.add_heading("Introduction")
pdf.add_paragraph("Your analysis text here...")
pdf.add_image('chart.png', width=5*72)
pdf.build()
```

---

## Testing Modules

Test each module independently:

```bash
# Test data fetching
python -c "from src.data_fetchers import ForexDataFetcher; \
f = ForexDataFetcher(); \
data = f.get_exchange_rate_yfinance('KRW', 'CHF', '2025-08-01', '2026-01-30'); \
print(f'Fetched {len(data)} days')"

# Test calculators
python src/calculators.py

# Test visualizers
python src/visualizers.py

# Test report generator
python src/report_generator.py
```

---

## Dependencies

### Core Libraries
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **yfinance** - FREE forex data (no API key!)
- **matplotlib** - Charts
- **seaborn** - Statistical visualizations

### Report Generation
- **reportlab** - PDF reports
- **python-pptx** - PowerPoint presentations
- **openpyxl** - Excel export

### Optional (Enhanced Features)
- **plotly** - Interactive charts
- **kaleido** - Plotly export to PNG
- **requests** - API calls (Alpha Vantage, FRED)
- **wbdata** - World Bank inflation data

**Install all:**
```bash
pip install -r requirements.txt
```

---

## Expected Results

Based on the project document (August 2025 - January 2026):

| Metric | Value |
|--------|-------|
| **Historical Rate** (Aug 1, 2025) | 1 KRW = 0.00067 CHF |
| **Current Rate** (Jan 30, 2026) | 1 KRW = 0.00062 CHF |
| **Change** | -7.46% (KRW depreciation) |
| **Korea Interest Rate** | 3.25% |
| **Swiss Interest Rate** | 1.25% |
| **Korea Inflation** | 2.3% |
| **Swiss Inflation** | 1.4% |

**Note:** Your actual results may vary slightly depending on real-time API data.

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: PDF/PowerPoint generation fails

**Check:**
```bash
pip install reportlab python-pptx
```

### Issue: No forex data returned

**Possible causes:**
1. Internet connection issue
2. Currency code typo (use 'KRW' and 'CHF')
3. yfinance API temporarily unavailable

**Solution:** The script will cache data, so subsequent runs will use cached data.

### Issue: Charts not displaying in Jupyter

**Solution:**
```python
%matplotlib inline
```

### Issue: API rate limits

**yfinance:** No limits (free)
**Alpha Vantage:** 25 requests/day (free tier)
**FRED:** 1000 requests/day (free tier)

---

## Academic Context

This toolkit is designed for **International Finance Management** coursework, specifically analyzing:

### Theory Coverage
- **Exchange Rate Determination** - Spot vs forward rates
- **Interest Rate Parity (IRP)** - Covered and uncovered parity
- **Purchasing Power Parity (PPP)** - Relative PPP
- **Marshall-Lerner Condition** - Export/import elasticity
- **J-Curve Effect** - Trade balance adjustment lags
- **Impossible Trinity** - Policy trilemma

### Real-World Application
- **Korean Chaebols** - Samsung, Hyundai currency exposure
- **Safe Haven Dynamics** - CHF as crisis hedge
- **Carry Trade** - Borrow CHF at 1.25%, invest in KRW at 3.25%
- **Central Bank Policy** - Bank of Korea interventions

---

## Contributing

To modify the analysis for a different currency pair:

1. Edit `config.py`:
   ```python
   BASE_CURRENCY = 'USD'
   TARGET_CURRENCY = 'EUR'
   ```

2. Update interest & inflation rates

3. Modify trade data in `config.py`

4. Run `python complete_analysis.py`

---

## License

This project is created for educational purposes (International Finance Management coursework).

---

## Acknowledgments

**Data Sources:**
- Exchange rates: yfinance (Yahoo Finance)
- Interest rates: FRED (Federal Reserve Economic Data), Bank of Korea, Swiss National Bank
- Inflation: World Bank, OECD
- Trade data: UN Comtrade, Korea International Trade Association (KITA)

**Economic Framework:**
- Interest Rate Parity (Keynes, 1923)
- Purchasing Power Parity (Cassel, 1918)
- Impossible Trinity (Mundell-Fleming model)

---

## Support

For questions or issues:
1. Check the code comments (heavily documented)
2. Run test scripts: `python src/calculators.py`
3. Review Jupyter notebooks for step-by-step examples

---

**Last Updated:** January 30, 2026
**Analysis Period:** August 2025 - January 2026
**Currency Pair:** KRW/CHF (Korea Won / Swiss Franc)
