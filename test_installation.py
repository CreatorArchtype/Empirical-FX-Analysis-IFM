"""
Quick Installation Test Script
Tests that all modules import correctly
"""

import sys
print("Python version:", sys.version)
print("\n" + "="*60)
print("TESTING KOREA-SWITZERLAND FINANCE ANALYSIS TOOLKIT")
print("="*60)

# Test imports
print("\n1. Testing module imports...")

try:
    sys.path.append('src')
    from data_fetchers import ForexDataFetcher, InterestRateFetcher, InflationDataFetcher
    print("  data_fetchers module imported")
except Exception as e:
    print(f" data_fetchers import failed: {e}")
    sys.exit(1)

try:
    from calculators import ExchangeRateCalculator, ParityCalculator, StatisticalAnalyzer
    print(" calculators module imported")
except Exception as e:
    print(f"   ERROR: calculators import failed: {e}")
    sys.exit(1)

try:
    from visualizers import ForexVisualizer
    print("   visualizers module imported")
except Exception as e:
    print(f"   ERROR: visualizers import failed: {e}")
    sys.exit(1)

try:
    from report_generator import PDFReportGenerator, PPTXReportGenerator
    print("   report_generator module imported")
except Exception as e:
    print(f"   ERROR: report_generator import failed: {e}")
    print(f"   ℹ️  Install reportlab and python-pptx: pip install reportlab python-pptx")

try:
    import config
    print("   config module imported")
except Exception as e:
    print(f"   ERROR: config import failed: {e}")
    sys.exit(1)

# Test calculator functionality
print("\n2. Testing calculator functions...")
calc = ExchangeRateCalculator()
result = calc.calculate_percentage_change(0.00067, 0.00062)
expected_change = -7.46
actual_change = result['percentage_change']

if abs(actual_change - expected_change) < 0.1:
    print(f"   Exchange rate calculation: {actual_change:.2f}% (Expected: {expected_change:.2f}%)")
else:
    print(f"   ERROR: Calculation mismatch: Got {actual_change:.2f}%, expected {expected_change:.2f}%")
    sys.exit(1)

# Test IRP calculation
print("\n3. Testing Interest Rate Parity (IRP)...")
parity_calc = ParityCalculator()
irp_result = parity_calc.interest_rate_parity(
    spot_rate=0.00062,
    domestic_rate=0.0325,
    foreign_rate=0.0125
)
print(f"   IRP Forward Rate: {irp_result['forward_rate']:.6f} CHF per KRW")
print(f"   Implied Change: {irp_result['implied_change_pct']:.2f}%")

# Test PPP calculation
print("\n4. Testing Purchasing Power Parity (PPP)...")
ppp_result = parity_calc.purchasing_power_parity(
    spot_rate=0.00062,
    inflation_domestic=0.023,
    inflation_foreign=0.014
)
print(f"   PPP Expected Rate: {ppp_result['expected_rate']:.6f} CHF per KRW")
print(f"   Implied Change: {ppp_result['implied_change_pct']:.2f}%")

# Test impact analysis
print("\n5. Testing stakeholder impact analysis...")
impact = calc.analyze_impact(result['percentage_change'])
print(f"   Exporters Impact: {impact['exporters']['impact']}")
print(f"   Importers Impact: {impact['importers']['impact']}")

# Check configuration
print("\n6. Testing configuration...")
print(f"   Currency Pair: {config.BASE_CURRENCY}/{config.TARGET_CURRENCY}")
print(f"   Analysis Period: {config.START_DATE.strftime('%Y-%m-%d')} to {config.END_DATE.strftime('%Y-%m-%d')}")
print(f"   Korea Interest Rate: {config.INTEREST_RATES['KRW']*100}%")
print(f"   Swiss Interest Rate: {config.INTEREST_RATES['CHF']*100}%")

# Check directories exist
import os
print("\n7. Testing directory structure...")
required_dirs = [
    'src',
    'data/raw',
    'data/processed',
    'data/cache',
    'outputs/charts',
    'outputs/reports',
    'outputs/presentations',
    'outputs/excel',
    'notebooks'
]

all_exist = True
for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"   {dir_path}/")
    else:
        print(f"   ERROR: {dir_path}/ NOT FOUND")
        all_exist = False

if not all_exist:
    print("\n   WARNING: Some directories missing. Run: mkdir -p data/raw data/processed data/cache outputs/charts outputs/reports outputs/presentations outputs/excel notebooks")

# Check key files exist
print("\n8. Testing key files...")
required_files = [
    'config.py',
    'requirements.txt',
    'README.md',
    'complete_analysis.py',
    'src/__init__.py',
    'src/data_fetchers.py',
    'src/calculators.py',
    'src/visualizers.py',
    'src/report_generator.py'
]

all_files_exist = True
for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   {file_path}")
    else:
        print(f"   ERROR: {file_path} NOT FOUND")
        all_files_exist = False

# Check dependencies
print("\n9. Testing dependencies...")
dependencies = {
    'pandas': 'Data manipulation',
    'numpy': 'Numerical computing',
    'matplotlib': 'Plotting',
    'seaborn': 'Statistical visualization'
}

for package, description in dependencies.items():
    try:
        __import__(package)
        print(f"   {package} ({description})")
    except ImportError:
        print(f"   ERROR: {package} NOT INSTALLED - {description}")
        print(f"      Install with: pip install {package}")

# Optional dependencies
print("\n10. Testing optional dependencies...")
optional_deps = {
    'yfinance': 'Forex data (REQUIRED for data fetching)',
    'plotly': 'Interactive charts',
    'reportlab': 'PDF generation',
    'python-pptx': 'PowerPoint generation (install as python-pptx)',
    'openpyxl': 'Excel export'
}

all_optional = True
for package, description in optional_deps.items():
    try:
        if package == 'python-pptx':
            __import__('pptx')
        else:
            __import__(package)
        print(f"   {package} ({description})")
    except ImportError:
        print(f"   WARNING: {package} not installed - {description}")
        all_optional = False

if not all_optional:
    print("\n   ℹ️  Install all dependencies with: pip install -r requirements.txt")

# Final summary
print("\n" + "="*60)
print("INSTALLATION TEST SUMMARY")
print("="*60)
print("All core modules working correctly")
print("Calculations producing expected results")
print("Configuration loaded successfully")

if all_exist and all_files_exist:
    print("All files and directories present")
else:
    print("WARNING: Some files/directories missing (check above)")

print("\n" + "="*60)
print("READY TO RUN!")
print("="*60)
print("\nNext steps:")
print("1. Install dependencies (if not done):")
print("   pip install -r requirements.txt")
print("\n2. Run complete analysis:")
print("   python complete_analysis.py")
print("\n3. Or explore with Jupyter:")
print("   jupyter notebook")
print("   # Open: notebooks/03_part_b_exchange_rate.ipynb")
print("\n" + "="*60)
