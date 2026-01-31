"""
Configuration file for International Finance Analysis Project
South Korea (KRW) ↔ Switzerland (CHF) Analysis
"""

from datetime import datetime, timedelta

# ==========================================
# API KEYS (Optional - can work without them)
# ==========================================

# Alpha Vantage API Key (Optional - for better forex data quality)
# Get free key at: https://www.alphavantage.co/support/#api-key
ALPHAVANTAGE_API_KEY = None  # Replace with your key or leave as None

# FRED API Key (Optional - for interest rate data)
# Get free key at: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = None  # Replace with your key or leave as None

# ==========================================
# CURRENCY PAIR CONFIGURATION
# ==========================================

# This analysis is specifically for:
# BASE COUNTRY: South Korea (Currency: Korean Won - KRW)
# TRADING PARTNER: Switzerland (Currency: Swiss Franc - CHF)

BASE_CURRENCY = 'KRW'      # South Korean Won
TARGET_CURRENCY = 'CHF'    # Swiss Franc
CURRENCY_PAIR_NAME = "South Korea (KRW) ↔ Switzerland (CHF)"

# ==========================================
# TIME PERIOD CONFIGURATION
# ==========================================

# Analysis period: August 2025 - January 2026 (6 months)
END_DATE = datetime(2026, 1, 30)    # Current analysis date
START_DATE = datetime(2025, 8, 1)    # 6 months prior

# Alternative: Use dynamic dates (last 6 months from today)
# END_DATE = datetime.now()
# START_DATE = END_DATE - timedelta(days=180)

# ==========================================
# INTEREST RATES (Manual Input)
# ==========================================

# As of January 2026
# Sources: Bank of Korea (BOK) and Swiss National Bank (SNB)

INTEREST_RATES = {
    'KRW': 0.0325,  # 3.25% - Bank of Korea base rate
    'CHF': 0.0125,  # 1.25% - Swiss National Bank policy rate
    'USD': 0.0525,  # 5.25% - US Federal Reserve (for reference)
    'EUR': 0.0400,  # 4.00% - European Central Bank (for reference)
}

# Interest rate differential (Korea - Switzerland)
RATE_DIFFERENTIAL = INTEREST_RATES['KRW'] - INTEREST_RATES['CHF']

# ==========================================
# INFLATION RATES (Manual Input)
# ==========================================

# Latest inflation rates for South Korea and Switzerland
# Sources: OECD, World Bank, National Statistical Offices

INFLATION_RATES = {
    'KRW': 0.023,  # 2.3% - Statistics Korea (KOSTAT)
    'CHF': 0.014,  # 1.4% - Swiss Federal Statistical Office
}

# Inflation differential
INFLATION_DIFFERENTIAL = INFLATION_RATES['KRW'] - INFLATION_RATES['CHF']

# ==========================================
# EXPECTED EXCHANGE RATES (From Project Document)
# ==========================================

# These are the expected values based on the project document
# Your actual API data may vary slightly

EXPECTED_RATES = {
    'historical_date': '2025-08-01',
    'historical_rate': 0.00067,  # 1 KRW = 0.00067 CHF (Aug 1, 2025)
    'current_date': '2026-01-30',
    'current_rate': 0.00062,     # 1 KRW = 0.00062 CHF (Jan 30, 2026)
    'expected_change_pct': -7.46  # Expected depreciation: -7.46%
}

# ==========================================
# TRADE DATA (Korea-Switzerland)
# ==========================================

# Bilateral trade facts for Part A analysis
KOREA_SWITZERLAND_TRADE = {
    'total_trade_value_usd': 5_200_000_000,  # ~$5.2 billion annually
    
    'korea_exports_to_switzerland': {
        'value_usd': 2_100_000_000,
        'top_products': [
            'Semiconductors and electronic integrated circuits',
            'Passenger vehicles and auto parts',
            'Smartphones and consumer electronics',
            'Display panels',
            'Petroleum products'
        ],
        'key_exporters': ['Samsung Electronics', 'SK Hynix', 'Hyundai', 'LG']
    },
    
    'korea_imports_from_switzerland': {
        'value_usd': 3_100_000_000,
        'top_products': [
            'Pharmaceutical products',
            'Precision instruments and machinery',
            'Watches and clocks',
            'Chemical products',
            'Medical equipment'
        ],
        'key_importers': ['Roche Korea', 'Novartis Korea', 'Korean manufacturers']
    },
    
    'trade_balance': -1_000_000_000,  # Korea has trade deficit with Switzerland
}

# ==========================================
# OUTPUT SETTINGS
# ==========================================

# Chart styling
CHART_STYLE = 'seaborn-v0_8-whitegrid'
CHART_DPI = 300
CHART_FIGSIZE = (12, 6)

# Colors (Korean flag inspired + Swiss red)
COLORS = {
    'korea_blue': '#003478',
    'korea_red': '#CD2E3A',
    'swiss_red': '#FF0000',
    'neutral_gray': '#2c3e50',
    'positive_green': '#27ae60',
    'negative_red': '#e74c3c',
    'warning_orange': '#f39c12'
}

# Report titles
REPORT_TITLE = "South Korea - Switzerland Currency Analysis"
REPORT_SUBTITLE = f"KRW/CHF Exchange Rate & Economic Impact • {END_DATE.strftime('%B %Y')}"

# ==========================================
# FILE PATHS
# ==========================================

OUTPUT_PATHS = {
    'charts': 'outputs/charts/',
    'reports': 'outputs/reports/',
    'presentations': 'outputs/presentations/',
    'excel': 'outputs/excel/',
    'cache': 'data/cache/'
}

# Default output filenames
DEFAULT_FILENAMES = {
    'pdf_report': 'Korea_Switzerland_IFM_Analysis.pdf',
    'pptx_report': 'Korea_Switzerland_Analysis.pptx',
    'excel_results': 'analysis_results.xlsx',
    'chart_exchange_rate': 'exchange_rate_analysis.png',
    'chart_volatility': 'volatility_analysis.png',
    'chart_impact': 'stakeholder_impact.png'
}

# ==========================================
# DISPLAY SETTINGS
# ==========================================

def print_config_summary():
    """Print configuration summary"""
    print("=" * 60)
    print("KOREA-SWITZERLAND FINANCE ANALYSIS - CONFIGURATION")
    print("=" * 60)
    print(f"\nCurrency Pair: {BASE_CURRENCY}/{TARGET_CURRENCY}")
    print(f"Analysis Period: {START_DATE.strftime('%B %d, %Y')} to {END_DATE.strftime('%B %d, %Y')}")
    print(f"Duration: {(END_DATE - START_DATE).days} days")
    
    print(f"\nInterest Rates:")
    print(f"  • South Korea (KRW): {INTEREST_RATES['KRW']*100:.2f}%")
    print(f"  • Switzerland (CHF): {INTEREST_RATES['CHF']*100:.2f}%")
    print(f"  • Differential: {RATE_DIFFERENTIAL*100:.2f}% (Korea higher)")
    
    print(f"\nInflation Rates:")
    print(f"  • South Korea: {INFLATION_RATES['KRW']*100:.2f}%")
    print(f"  • Switzerland: {INFLATION_RATES['CHF']*100:.2f}%")
    print(f"  • Differential: {INFLATION_DIFFERENTIAL*100:.2f}%")
    
    print(f"\nExpected Exchange Rate Change:")
    print(f"  • Historical ({EXPECTED_RATES['historical_date']}): 1 KRW = {EXPECTED_RATES['historical_rate']:.6f} CHF")
    print(f"  • Current ({EXPECTED_RATES['current_date']}): 1 KRW = {EXPECTED_RATES['current_rate']:.6f} CHF")
    print(f"  • Expected Change: {EXPECTED_RATES['expected_change_pct']:.2f}%")
    
    print(f"\nAPI Configuration:")
    print(f"  • Alpha Vantage: {'Configured' if ALPHAVANTAGE_API_KEY else 'Not configured (using yfinance)'}")
    print(f"  • FRED API: {'Configured' if FRED_API_KEY else 'Not configured (using manual rates)'}")
    print("=" * 60)

if __name__ == "__main__":
    print_config_summary()
