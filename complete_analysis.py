"""
Complete Analysis Script for International Finance Management Project
South Korea (KRW) ↔ Switzerland (CHF) Currency Analysis

This script performs a complete end-to-end analysis:
- Part A: Country selection justification
- Part B: Exchange rate analysis (KRW/CHF)
- Part C: Parity conditions (IRP, PPP)
- Part D: Policy analysis and risks
- Part E: Stakeholder implications

Outputs: PDF report, PowerPoint presentation, charts
"""

import sys
import os

# Add src to path
sys.path.append('src')

from data_fetchers import fetch_all_korea_switzerland_data, ForexDataFetcher
from calculators import ExchangeRateCalculator, ParityCalculator, StatisticalAnalyzer
from visualizers import ForexVisualizer
from report_generator import PDFReportGenerator, PPTXReportGenerator

import pandas as pd
from datetime import datetime
import config

# ==========================================
# CONFIGURATION
# ==========================================

print("=" * 80)
print("INTERNATIONAL FINANCE ANALYSIS: SOUTH KOREA ↔ SWITZERLAND")
print("Currency Pair: KRW/CHF")
print("=" * 80)
print()

# Display configuration
config.print_config_summary()

# ==========================================
# PART 0: DATA COLLECTION
# ==========================================

print("\n" + "=" * 80)
print("STEP 1: DATA COLLECTION")
print("=" * 80)

# Fetch all data
all_data = fetch_all_korea_switzerland_data(
    start_date=config.START_DATE.strftime('%Y-%m-%d'),
    end_date=config.END_DATE.strftime('%Y-%m-%d'),
    alphavantage_key=config.ALPHAVANTAGE_API_KEY,
    fred_key=config.FRED_API_KEY
)

forex_data = all_data['forex_data']
interest_rates = all_data['interest_rates']
inflation_rates = all_data['inflation_rates']

print(f"\nData collection complete!")
print(f"   • Forex data points: {len(forex_data)}")
print(f"   • Date range: {forex_data.index[0].strftime('%Y-%m-%d')} to {forex_data.index[-1].strftime('%Y-%m-%d')}")

# ==========================================
# PART B: EXCHANGE RATE ANALYSIS
# ==========================================

print("\n" + "=" * 80)
print("PART B: KRW/CHF EXCHANGE RATE ANALYSIS")
print("=" * 80)

# Calculate exchange rate metrics
calculator = ExchangeRateCalculator()
old_rate = forex_data['cross_rate'].iloc[0]
new_rate = forex_data['cross_rate'].iloc[-1]

change_metrics = calculator.calculate_percentage_change(old_rate, new_rate)

print(f"\nExchange Rate Change Analysis:")
print(f"   Historical Rate ({forex_data.index[0].strftime('%B %d, %Y')}): 1 KRW = {old_rate:.6f} CHF")
print(f"   Current Rate ({forex_data.index[-1].strftime('%B %d, %Y')}):    1 KRW = {new_rate:.6f} CHF")
print(f"   Absolute Change:               {change_metrics['absolute_change']:.6f} CHF")
print(f"   Percentage Change:             {change_metrics['percentage_change']:.2f}%")
print(f"   Direction:                     {change_metrics['direction'].upper()}")

# Context interpretation
if change_metrics['percentage_change'] < 0:
    print(f"\nInterpretation:")
    print(f"   The Korean Won has DEPRECIATED against the Swiss Franc by {abs(change_metrics['percentage_change']):.2f}%")
    print(f"   • Swiss products (watches, pharmaceuticals) are MORE expensive for Koreans")
    print(f"   • Korean exports (electronics, semiconductors) are CHEAPER for Swiss buyers")
else:
    print(f"\nInterpretation:")
    print(f"   The Korean Won has APPRECIATED against the Swiss Franc by {change_metrics['percentage_change']:.2f}%")
    print(f"   • Swiss products are CHEAPER for Korean importers")
    print(f"   • Korean exports are MORE expensive for foreign buyers")

# Impact analysis
print(f"\nImpact on Stakeholders:")
impact = calculator.analyze_impact(change_metrics['percentage_change'], 
                                   config.BASE_CURRENCY, config.TARGET_CURRENCY)

print(f"\n   KOREAN EXPORTERS (Samsung, Hyundai, LG):")
print(f"   Status: {impact['exporters']['impact']}")
print(f"   → {impact['exporters']['reason']}")
if 'examples' in impact['exporters']:
    print(f"   → {impact['exporters']['examples']['korea']}")

print(f"\n   KOREAN IMPORTERS (Pharmaceutical distributors, Machinery buyers):")
print(f"   Status: {impact['importers']['impact']}")
print(f"   → {impact['importers']['reason']}")
if 'examples' in impact['importers']:
    print(f"   → {impact['importers']['examples']['korea']}")

# ==========================================
# PART C: PARITY CONDITIONS
# ==========================================

print("\n" + "=" * 80)
print("PART C: INTEREST RATE PARITY & PURCHASING POWER PARITY")
print("=" * 80)

# Interest Rate Parity (IRP)
print(f"\n🔵 Interest Rate Parity (IRP) Analysis:")
parity_calc = ParityCalculator()
irp_result = parity_calc.interest_rate_parity(
    spot_rate=new_rate,
    domestic_rate=interest_rates['KRW'],
    foreign_rate=interest_rates['CHF']
)

print(f"\n   Formula: {irp_result['formula']}")
print(f"\n   Given:")
print(f"   • Spot Rate (S₀):           {new_rate:.6f} CHF per KRW")
print(f"   • Korea Interest Rate:      {interest_rates['KRW']*100:.2f}%")
print(f"   • Switzerland Interest Rate: {interest_rates['CHF']*100:.2f}%")
print(f"   • Rate Differential:        {irp_result['rate_differential_pct']:.2f}% (Korea higher)")

print(f"\n   Calculation Steps:")
for i, step in enumerate(irp_result['substitution_steps'], 1):
    print(f"   {i}. {step}")

print(f"\n   Results:")
print(f"   • Forward Rate (F):         {irp_result['forward_rate']:.6f} CHF per KRW")
print(f"   • Implied Change:           {irp_result['implied_change_pct']:.2f}%")
print(f"   • Direction:                {irp_result['direction'].title()} of KRW")

print(f"\n   Economic Interpretation:")
print(f"   {irp_result['interpretation'][:300]}...")

# Purchasing Power Parity (PPP)
print(f"\n🔴 Purchasing Power Parity (PPP) Analysis:")
ppp_result = parity_calc.purchasing_power_parity(
    spot_rate=new_rate,
    inflation_domestic=inflation_rates['KRW'],
    inflation_foreign=inflation_rates['CHF']
)

print(f"\n   Formula: {ppp_result['formula']}")
print(f"\n   Given:")
print(f"   • Spot Rate (S₀):           {new_rate:.6f} CHF per KRW")
print(f"   • Korea Inflation:          {inflation_rates['KRW']*100:.2f}%")
print(f"   • Switzerland Inflation:    {inflation_rates['CHF']*100:.2f}%")
print(f"   • Inflation Differential:   {ppp_result['inflation_differential_pct']:.2f}%")

print(f"\n   Results:")
print(f"   • Expected Rate (E[S₁]):    {ppp_result['expected_rate']:.6f} CHF per KRW")
print(f"   • Implied Change:           {ppp_result['implied_change_pct']:.2f}%")
print(f"   • Direction:                {ppp_result['direction'].title()} of KRW")

# ==========================================
# PART D: VISUALIZATIONS
# ==========================================

print("\n" + "=" * 80)
print("STEP 2: GENERATING VISUALIZATIONS")
print("=" * 80)

visualizer = ForexVisualizer()

# 1. Time series chart
print("\nCreating exchange rate time series chart...")
visualizer.plot_exchange_rate_time_series(
    forex_data, 
    config.BASE_CURRENCY, 
    config.TARGET_CURRENCY,
    save_path=f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_exchange_rate']}"
)

# 2. Volatility analysis
print("\nCreating volatility analysis chart...")
visualizer.plot_volatility_analysis(
    forex_data,
    config.BASE_CURRENCY,
    config.TARGET_CURRENCY,
    save_path=f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_volatility']}"
)

# 3. Stakeholder impact matrix
print("\nCreating stakeholder impact chart...")
visualizer.plot_stakeholder_impact(
    impact,
    save_path=f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_impact']}"
)

# 4. Rate comparison chart
print("\nCreating rate comparison chart...")
visualizer.plot_comparison_chart(
    historical_rate=old_rate,
    current_rate=new_rate,
    forward_rate=irp_result['forward_rate'],
    ppp_rate=ppp_result['expected_rate'],
    from_currency=config.BASE_CURRENCY,
    to_currency=config.TARGET_CURRENCY,
    save_path=f"{config.OUTPUT_PATHS['charts']}rate_comparison.png"
)

# 5. Interactive chart (if Plotly available)
print("\nCreating interactive chart...")
try:
    visualizer.plot_interactive_forex(
        forex_data,
        config.BASE_CURRENCY,
        config.TARGET_CURRENCY,
        save_path=f"{config.OUTPUT_PATHS['charts']}interactive_krw_chf.html"
    )
except Exception as e:
    print(f"   WARNING: Interactive chart skipped: {e}")

# ==========================================
# PART E: REPORT GENERATION
# ==========================================

print("\n" + "=" * 80)
print("STEP 3: GENERATING REPORTS")
print("=" * 80)

# PDF Report
print("\nGenerating PDF report...")
try:
    pdf = PDFReportGenerator(f"{config.OUTPUT_PATHS['reports']}{config.DEFAULT_FILENAMES['pdf_report']}")
    
    # Title page
    pdf.add_title(config.REPORT_TITLE)
    pdf.add_paragraph(config.REPORT_SUBTITLE)
    pdf.add_paragraph(f"Analysis Period: {config.START_DATE.strftime('%B %d, %Y')} to {config.END_DATE.strftime('%B %d, %Y')}")
    pdf.add_paragraph(f"Currency Pair: Korean Won (KRW) / Swiss Franc (CHF)")
    
    # Executive Summary
    pdf.add_heading("Executive Summary")
    pdf.add_paragraph(
        f"This report analyzes the currency relationship between South Korea (KRW) and Switzerland (CHF) "
        f"over a {(config.END_DATE - config.START_DATE).days}-day period. The Korean Won has "
        f"{'depreciated' if change_metrics['percentage_change'] < 0 else 'appreciated'} by "
        f"{abs(change_metrics['percentage_change']):.2f}% against the Swiss Franc, with significant "
        f"implications for Korean exporters, importers, and policymakers."
    )
    
    # Part A: Country Selection
    pdf.add_heading("Part A: Why Switzerland Matters for South Korea")
    pdf.add_paragraph(
        f"Switzerland is a critical trading partner for South Korea with bilateral trade valued at "
        f"${config.KOREA_SWITZERLAND_TRADE['total_trade_value_usd']/1e9:.1f} billion annually. "
        f"South Korea exports semiconductors, electronics, and vehicles to Switzerland while importing "
        f"precision machinery, pharmaceuticals (Roche, Novartis), and luxury goods. This relationship "
        f"is characterized by Korean high-tech manufacturing meeting Swiss precision engineering."
    )
    
    pdf.add_subheading("Trade Balance")
    pdf.add_paragraph(
        f"Korea maintains a trade deficit of ${abs(config.KOREA_SWITZERLAND_TRADE['trade_balance'])/1e9:.1f} billion "
        f"with Switzerland, importing ${config.KOREA_SWITZERLAND_TRADE['korea_imports_from_switzerland']['value_usd']/1e9:.1f}B "
        f"and exporting ${config.KOREA_SWITZERLAND_TRADE['korea_exports_to_switzerland']['value_usd']/1e9:.1f}B. "
        f"The strategic importance lies in Switzerland's provision of precision machinery essential for "
        f"Korea's semiconductor manufacturing capabilities."
    )
    
    # Part B: Exchange Rate Analysis
    pdf.add_heading("Part B: KRW/CHF Exchange Rate Analysis")
    pdf.add_paragraph(
        f"The Korean Won has {'depreciated' if change_metrics['percentage_change'] < 0 else 'appreciated'} "
        f"by {abs(change_metrics['percentage_change']):.2f}% over the analysis period. This movement has "
        f"asymmetric effects on Korean stakeholders."
    )
    
    pdf.add_image(
        f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_exchange_rate']}",
        width=6*72,  # 6 inches
        caption=f"Figure 1: KRW/CHF Exchange Rate Trend ({config.START_DATE.strftime('%b %Y')} - {config.END_DATE.strftime('%b %Y')})"
    )
    
    # Stakeholder Impact Table
    pdf.add_subheading("Stakeholder Impact Matrix")
    stakeholder_data = [
        ['Stakeholder', 'Impact', 'Key Considerations'],
        [
            'Korean Exporters\n(Samsung, Hyundai, LG)',
            impact['exporters']['impact'],
            'Semiconductors and electronics more competitive in Swiss/European markets'
        ],
        [
            'Korean Importers\n(Pharma distributors)',
            impact['importers']['impact'],
            'Swiss machinery and pharmaceuticals become costlier; margin pressure'
        ],
        [
            'Korean Chaebols',
            'MIXED',
            'Export divisions benefit while import costs rise; hedging essential'
        ],
        [
            'Korean SMEs',
            'NEGATIVE',
            'Lack hedging capabilities; vulnerable to import cost shocks'
        ],
        [
            'Bank of Korea',
            'COMPLEX',
            'Must balance export competitiveness vs. imported inflation'
        ]
    ]
    pdf.add_table(stakeholder_data)
    
    pdf.add_image(
        f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_impact']}",
        width=6*72,
        caption="Figure 2: Stakeholder Impact Visualization"
    )
    
    # Part C: Parity Conditions
    pdf.add_heading("Part C: Interest Rate Parity and Purchasing Power Parity")
    
    pdf.add_subheading("Interest Rate Parity (IRP)")
    pdf.add_paragraph(
        f"With South Korea's interest rate at {interest_rates['KRW']*100:.2f}% and Switzerland's at "
        f"{interest_rates['CHF']*100:.2f}%, the {irp_result['rate_differential_pct']:.2f}% differential "
        f"suggests the Won should trade at a forward {'discount' if irp_result['implied_change_pct'] < 0 else 'premium'}. "
        f"The calculated forward rate of {irp_result['forward_rate']:.6f} CHF per KRW implies an expected "
        f"{abs(irp_result['implied_change_pct']):.2f}% {'depreciation' if irp_result['implied_change_pct'] < 0 else 'appreciation'}."
    )
    
    pdf.add_paragraph(
        f"Economic Mechanism: Higher Korean interest rates ({interest_rates['KRW']*100:.2f}%) initially attract "
        f"carry trade investors. However, IRP dictates that the expected {abs(irp_result['implied_change_pct']):.2f}% "
        f"currency movement must offset the interest advantage to prevent arbitrage."
    )
    
    pdf.add_subheading("Purchasing Power Parity (PPP)")
    pdf.add_paragraph(
        f"Korea's inflation rate ({inflation_rates['KRW']*100:.2f}%) exceeds Switzerland's ({inflation_rates['CHF']*100:.2f}%) "
        f"by {ppp_result['inflation_differential_pct']:.2f}%, suggesting PPP-driven depreciation pressure on the Won. "
        f"The expected rate under PPP is {ppp_result['expected_rate']:.6f} CHF per KRW."
    )
    
    pdf.add_image(
        f"{config.OUTPUT_PATHS['charts']}rate_comparison.png",
        width=5*72,
        caption="Figure 3: Rate Comparison - Historical, Current, IRP Forward, and PPP Expected"
    )
    
    # Part D: Policy Analysis
    pdf.add_heading("Part D: Policy Implications and Risks for South Korea")
    
    pdf.add_subheading("Key Risks")
    pdf.add_paragraph(
        "1. Safe Haven Squeeze: During global market stress, investors flee Korean Won (risky emerging market currency) "
        "and buy Swiss Francs (safe haven), causing non-fundamental depreciation.\n\n"
        "2. Imported Inflation: Won depreciation makes Swiss machinery and pharmaceuticals costlier, potentially "
        "feeding into domestic inflation.\n\n"
        "3. Impossible Trinity: South Korea cannot simultaneously maintain exchange rate stability, free capital flows, "
        "and independent monetary policy."
    )
    
    pdf.add_subheading("Policy Recommendation: SME Forex Liquidity Facility")
    pdf.add_paragraph(
        "The Bank of Korea should establish an 'SME Forex Liquidity Facility' to protect small Korean businesses from "
        "sudden import cost shocks. This facility would provide:\n\n"
        "• Hedging instruments at subsidized rates for SMEs importing Swiss machinery\n"
        "• Forward contract access without requiring large collateral\n"
        "• Currency risk education programs\n\n"
        "Benefits: Stabilizes supply chains during J-Curve adjustment periods while maintaining export competitiveness."
    )
    
    pdf.add_image(
        f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_volatility']}",
        width=6.5*72,
        caption="Figure 4: KRW/CHF Volatility and Return Distribution Analysis"
    )
    
    #Part E: Conclusions
    pdf.add_heading("Part E: Conclusions and Outlook")
    pdf.add_paragraph(
        f"The {abs(change_metrics['percentage_change']):.2f}% {'depreciation' if change_metrics['percentage_change'] < 0 else 'appreciation'} "
        f"of the Korean Won against the Swiss Franc reflects broader macroeconomic fundamentals:\n\n"
        f"• Interest rate differential ({irp_result['rate_differential_pct']:.2f}%): Korea's higher rates attract capital but IRP predicts offsetting depreciation\n"
        f"• Inflation differential ({ppp_result['inflation_differential_pct']:.2f}%): Higher Korean inflation erodes purchasing power\n"
        f"• Trade dynamics: Korea's export competitiveness improves, but import costs rise\n\n"
        f"Korean policymakers face the classic trilemma: balancing export-led growth (benefits from weak Won) against "
        f"imported inflation risks (from expensive Swiss machinery and pharmaceuticals)."
    )
    
    pdf.add_paragraph(
        "The SME Forex Liquidity Facility represents a pragmatic middle path - allowing market forces to support exporters "
        "while protecting vulnerable small businesses from currency volatility."
    )
    
    pdf.build()
    
except Exception as e:
    print(f"   WARNING: PDF generation failed: {e}")
    print(f"   Make sure reportlab is installed: pip install reportlab")

# PowerPoint Presentation
print("\nGenerating PowerPoint presentation...")
try:
    pptx = PPTXReportGenerator(f"{config.OUTPUT_PATHS['presentations']}{config.DEFAULT_FILENAMES['pptx_report']}")
    
    # Slide 1: Title
    pptx.add_title_slide(
        config.REPORT_TITLE,
        config.REPORT_SUBTITLE
    )
    
    # Slide 2: Why Switzerland?
    pptx.add_content_slide(
        "Part A: Why Switzerland?",
        [
            f"Critical trading partner: ${config.KOREA_SWITZERLAND_TRADE['total_trade_value_usd']/1e9:.1f}B bilateral trade",
            f"Korea exports: Semiconductors, electronics, vehicles (${config.KOREA_SWITZERLAND_TRADE['korea_exports_to_switzerland']['value_usd']/1e9:.1f}B)",
            f"Korea imports: Precision machinery, pharmaceuticals, watches (${config.KOREA_SWITZERLAND_TRADE['korea_imports_from_switzerland']['value_usd']/1e9:.1f}B)",
            f"Trade deficit: ${abs(config.KOREA_SWITZERLAND_TRADE['trade_balance'])/1e9:.1f}B (Korea imports more)",
            "Strategic: Swiss precision tools enable Korean semiconductor manufacturing"
        ]
    )
    
    # Slide 3: Exchange Rate Change
    pptx.add_content_slide(
        "Part B: KRW/CHF Exchange Rate Change",
        [
            f"Historical ({forex_data.index[0].strftime('%b %d, %Y')}): 1 KRW = {old_rate:.6f} CHF",
            f"Current ({forex_data.index[-1].strftime('%b %d, %Y')}): 1 KRW = {new_rate:.6f} CHF",
            f"Change: {change_metrics['percentage_change']:.2f}%",
            f"Direction: {change_metrics['direction'].title()}",
            f"Impact: {'Korean exporters benefit' if change_metrics['percentage_change'] < 0 else 'Korean importers benefit'}, "
            f"{'importers face cost pressure' if change_metrics['percentage_change'] < 0 else 'exporters face competitive pressure'}"
        ]
    )
    
    # Slide 4: Time Series Chart
    pptx.add_image_slide(
        "KRW/CHF Exchange Rate Trend",
        f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_exchange_rate']}",
        caption=f"6-month trend showing {abs(change_metrics['percentage_change']):.2f}% {'depreciation' if change_metrics['percentage_change'] < 0 else 'appreciation'}"
    )
    
    # Slide 5: Stakeholder Impact
    pptx.add_two_column_slide(
        "Stakeholder Impact Analysis",
        [
            "WINNERS:",
            f"• Korean exporters ({impact['exporters']['impact']})",
            "  - Samsung, Hyundai, LG benefit",
            "  - Goods cheaper for Swiss buyers",
            "• Forex traders",
            "  - Carry trade opportunities"
        ],
        [
            "LOSERS:",
            f"• Korean importers ({impact['importers']['impact']})",
            "  - Swiss machinery costlier",
            "  - Roche/Novartis drugs expensive",
            "• Korean SMEs",
            "  - Lack hedging capacity",
            "  - Vulnerable to shocks"
        ]
    )
    
    # Slide 6: Interest Rate Parity
    pptx.add_content_slide(
        "Part C: Interest Rate Parity (IRP)",
        [
            f"Korea interest rate: {interest_rates['KRW']*100:.2f}%",
            f"Switzerland interest rate: {interest_rates['CHF']*100:.2f}%",
            f"Differential: +{irp_result['rate_differential_pct']:.2f}% (Korea higher)",
            f"Forward rate (IRP): {irp_result['forward_rate']:.6f} CHF per KRW",
            f"Implied KRW movement: {irp_result['implied_change_pct']:.2f}%",
            f"Interpretation: Higher Korean rates offset by expected {abs(irp_result['implied_change_pct']):.2f}% depreciation"
        ]
    )
    
    # Slide 7: Purchasing Power Parity
    pptx.add_content_slide(
        "Part C: Purchasing Power Parity (PPP)",
        [
            f"Korea inflation: {inflation_rates['KRW']*100:.2f}%",
            f"Switzerland inflation: {inflation_rates['CHF']*100:.2f}%",
            f"Differential: +{ppp_result['inflation_differential_pct']:.2f}%",
            f"PPP expected rate: {ppp_result['expected_rate']:.6f} CHF per KRW",
            f"Implication: Higher Korean inflation → KRW depreciation pressure",
            "Both IRP and PPP predict Won weakness"
        ]
    )
    
    # Slide 8: Policy Recommendations
    pptx.add_content_slide(
        "Part D: Policy Recommendations for South Korea",
        [
            "CHALLENGE: 'Impossible Trinity'",
            "  - Can't control exchange rate, capital flows, AND monetary policy simultaneously",
            "RISK: Safe haven squeeze during global stress (KRW → CHF flight)",
            "RISK: Imported inflation from Won depreciation",
            "",
            "RECOMMENDATION: 'SME Forex Liquidity Facility'",
            "  - Provide hedging instruments to small Korean businesses",
            "  - Protect against import cost shocks",
            "  - Stabilize supply chains while maintaining export competitiveness"
        ]
    )
    
    # Slide 9: Volatility Chart
    pptx.add_image_slide(
        "Volatility Analysis",
        f"{config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_volatility']}",
        caption="Rolling volatility and return distribution"
    )
    
    # Slide 10: Conclusions
    pptx.add_content_slide(
        "Part E: Key Takeaways",
        [
            f"✓ KRW {change_metrics['direction']}d {abs(change_metrics['percentage_change']):.2f}% vs CHF over 6 months",
            "✓ IRP and PPP both predict Won depreciation (fundamentals-driven)",
            "✓ Korean exporters (Samsung, Hyundai) gain competitiveness",
            "✓ Korean importers face margin pressure from expensive Swiss goods",
            "✓ Policy challenge: Balance export growth vs. imported inflation",
            "✓ Solution: SME Forex Facility to protect vulnerable businesses"
        ]
    )
    
    pptx.save()
    
except Exception as e:
    print(f"   WARNING: PowerPoint generation failed: {e}")
    print(f"   Make sure python-pptx is installed: pip install python-pptx")

# Excel Export
print("\nExporting data to Excel...")
try:
    from report_generator import export_to_excel
    
    # Create summary DataFrame
    summary_df = pd.DataFrame({
        'Metric': [
            'Historical Rate',
            'Current Rate',
            'Absolute Change',
            'Percentage Change (%)',
            'Direction',
            'Korea Interest Rate (%)',
            'Swiss Interest Rate (%)',
            'Interest Differential (%)',
            'IRP Forward Rate',
            'IRP Implied Change (%)',
            'Korea Inflation (%)',
            'Swiss Inflation (%)',
            'PPP Expected Rate',
            'PPP Implied Change (%)'
        ],
        'Value': [
            f"{old_rate:.6f}",
            f"{new_rate:.6f}",
            f"{change_metrics['absolute_change']:.6f}",
            f"{change_metrics['percentage_change']:.2f}",
            change_metrics['direction'],
            f"{interest_rates['KRW']*100:.2f}",
            f"{interest_rates['CHF']*100:.2f}",
            f"{irp_result['rate_differential_pct']:.2f}",
            f"{irp_result['forward_rate']:.6f}",
            f"{irp_result['implied_change_pct']:.2f}",
            f"{inflation_rates['KRW']*100:.2f}",
            f"{inflation_rates['CHF']*100:.2f}",
            f"{ppp_result['expected_rate']:.6f}",
            f"{ppp_result['implied_change_pct']:.2f}"
        ]
    })
    
    export_to_excel(
        {
            'Summary': summary_df,
            'Exchange Rates': forex_data
        },
        f"{config.OUTPUT_PATHS['excel']}{config.DEFAULT_FILENAMES['excel_results']}"
    )
    
except Exception as e:
    print(f"   WARNING: Excel export failed: {e}")

# ==========================================
# COMPLETION SUMMARY
# ==========================================

print("\n" + "=" * 80)
print("KOREA-SWITZERLAND ANALYSIS COMPLETE!")
print("=" * 80)

print(f"\n📂 Generated Files:")
print(f"   PDF Report:      {config.OUTPUT_PATHS['reports']}{config.DEFAULT_FILENAMES['pdf_report']}")
print(f"   PowerPoint:      {config.OUTPUT_PATHS['presentations']}{config.DEFAULT_FILENAMES['pptx_report']}")
print(f"   Excel Data:      {config.OUTPUT_PATHS['excel']}{config.DEFAULT_FILENAMES['excel_results']}")

print(f"\nCharts:")
print(f"   Exchange Rate:   {config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_exchange_rate']}")
print(f"   Volatility:      {config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_volatility']}")
print(f"   Stakeholder:     {config.OUTPUT_PATHS['charts']}{config.DEFAULT_FILENAMES['chart_impact']}")
print(f"   Comparison:      {config.OUTPUT_PATHS['charts']}rate_comparison.png")

print(f"\nKey Findings:")
print(f"   • KRW {'depreciated' if change_metrics['percentage_change'] < 0 else 'appreciated'} {abs(change_metrics['percentage_change']):.2f}% vs CHF")
print(f"   • IRP predicts {abs(irp_result['implied_change_pct']):.2f}% KRW {irp_result['direction']}")
print(f"   • PPP predicts {abs(ppp_result['implied_change_pct']):.2f}% KRW {ppp_result['direction']}")
print(f"   • Korean exporters: {impact['exporters']['impact']}")
print(f"   • Korean importers: {impact['importers']['impact']}")

print(f"\nPolicy Recommendation:")
print(f"   Establish 'SME Forex Liquidity Facility' to protect small Korean businesses")
print(f"   from currency volatility while maintaining export competitiveness")

print("\n" + "=" * 80)
