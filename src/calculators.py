"""
Financial calculators for International Finance Analysis Project
IRP, PPP, exchange rate changes, volatility analysis
Specifically for South Korea (KRW) and Switzerland (CHF)
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

class ExchangeRateCalculator:
    """Calculate exchange rate metrics and impacts"""
    
    @staticmethod
    def calculate_percentage_change(old_rate: float, new_rate: float) -> Dict:
        """
        Calculate percentage change in exchange rate
        
        Formula: % Change = ((New - Old) / Old) × 100
        
        Args:
            old_rate: Historical exchange rate (e.g., 0.00067 CHF per KRW on Aug 1, 2025)
            new_rate: Current exchange rate (e.g., 0.00062 CHF per KRW on Jan 30, 2026)
        
        Returns:
            dict with:
                - old_rate: Original rate
                - new_rate: New rate
                - absolute_change: Absolute difference
                - percentage_change: Percentage change
                - direction: 'depreciation' or 'appreciation'
        
        Example:
            >>> calc = ExchangeRateCalculator()
            >>> result = calc.calculate_percentage_change(0.00067, 0.00062)
            >>> print(f"KRW {result['direction']}: {result['percentage_change']:.2f}%")
        """
        absolute_change = new_rate - old_rate
        pct_change = (absolute_change / old_rate) * 100
        
        # Determine direction
        # Negative change means base currency (KRW) depreciated
        # Positive change means base currency (KRW) appreciated
        direction = "depreciation" if pct_change < 0 else "appreciation"
        
        return {
            'old_rate': old_rate,
            'new_rate': new_rate,
            'absolute_change': absolute_change,
            'percentage_change': pct_change,
            'direction': direction
        }
    
    @staticmethod
    def analyze_impact(pct_change: float, from_currency: str = 'KRW', 
                      to_currency: str = 'CHF') -> Dict:
        """
        Analyze impact on exporters and importers
        
        Key economic principles:
        - DEPRECIATION (negative % change):
          * Exporters benefit: Goods become cheaper for foreign buyers
          * Importers lose: Foreign goods become more expensive
        
        - APPRECIATION (positive % change):
          * Exporters lose: Goods become more expensive abroad
          * Importers benefit: Foreign goods become cheaper
        
        Args:
            pct_change: Percentage change in exchange rate
            from_currency: Base currency (default: 'KRW')
            to_currency: Target currency (default: 'CHF')
        
        Returns:
            dict with impact analysis for exporters and importers
        
        Example (KRW depreciation by 7.46%):
            >>> calc = ExchangeRateCalculator()
            >>> impact = calc.analyze_impact(-7.46, 'KRW', 'CHF')
            >>> print(impact['exporters']['impact'])  # 'BENEFIT'
        """
        if pct_change < 0:
            # DEPRECIATION of base currency (KRW weakened vs CHF)
            return {
                'exporters': {
                    'impact': 'BENEFIT',
                    'magnitude': abs(pct_change),
                    'reason': f'{from_currency} goods become ~{abs(pct_change):.2f}% cheaper for {to_currency} buyers',
                    'condition': 'Assuming Marshall-Lerner condition met (demand is price-elastic)',
                    'examples': {
                        'korea': 'Samsung semiconductors, Hyundai cars more competitive in Switzerland/Europe',
                        'mechanism': f'A Swiss buyer with 1000 {to_currency} can now buy ~{abs(pct_change):.2f}% more Korean goods'
                    },
                    'caveats': [
                        'J-Curve effect: Short-term worsening before improvement',
                        'Benefit only if foreign demand is elastic',
                        'Requires export contracts not locked in {to_currency} prices'
                    ]
                },
                'importers': {
                    'impact': 'LOSS',
                    'magnitude': abs(pct_change),
                    'reason': f'{to_currency} goods become ~{abs(pct_change):.2f}% costlier for {from_currency} buyers',
                    'consequence': 'Margin squeeze on import-dependent firms',
                    'examples': {
                        'korea': 'Korean pharmaceutical distributors (Roche/Novartis drugs), machinery importers face higher costs',
                        'mechanism': f'Korean manufacturers need ~{abs(pct_change):.2f}% more {from_currency} to buy same Swiss precision equipment'
                    },
                    'risks': [
                        'Imported inflation if cost increases passed to consumers',
                        'Cash flow pressure for firms with {to_currency}-denominated payables',
                        'Competitive disadvantage vs. domestic producers'
                    ]
                },
                'overall_trade_balance': {
                    'expectation': 'Improvement (if Marshall-Lerner holds)',
                    'timeframe': '12-18 months (after J-Curve)',
                    'for_korea': 'Export-led economic support, but inflation risk from costlier imports'
                }
            }
        else:
            # APPRECIATION of base currency (KRW strengthened vs CHF)
            return {
                'exporters': {
                    'impact': 'LOSS',
                    'magnitude': pct_change,
                    'reason': f'{from_currency} goods become ~{pct_change:.2f}% more expensive for {to_currency} buyers',
                    'consequence': 'Reduced export competitiveness',
                    'examples': {
                        'korea': 'Samsung, Hyundai products less price-competitive in Switzerland',
                        'mechanism': 'Swiss buyers need more CHF to purchase same Korean goods'
                    },
                    'risks': [
                        'Loss of market share to competitors',
                        'Pressure to cut prices (margin squeeze)',
                        'Reduced export volumes'
                    ]
                },
                'importers': {
                    'impact': 'BENEFIT',
                    'magnitude': pct_change,
                    'reason': f'{to_currency} goods become ~{pct_change:.2f}% cheaper for {from_currency} buyers',
                    'opportunity': 'Lower input costs, improved margins',
                    'examples': {
                        'korea': 'Korean importers of Swiss machinery, pharmaceuticals save costs',
                        'mechanism': 'Need less KRW to buy same Swiss products'
                    },
                    'benefits': [
                        'Reduced production costs for manufacturers',
                        'Lower consumer prices (disinflationary)',
                        'Easier for Korean firms to acquire Swiss technology'
                    ]
                },
                'overall_trade_balance': {
                    'expectation': 'Deterioration',
                    'timeframe': 'Immediate',
                    'for_korea': 'Imports rise, exports fall; trade deficit widens'
                }
            }
    
    @staticmethod
    def calculate_competitiveness_index(exchange_rate_change: float, 
                                        inflation_differential: float) -> Dict:
        """
        Calculate Real Effective Exchange Rate (REER) change
        
        REER adjustment: Nominal rate change + Inflation differential
        
        Args:
            exchange_rate_change: Nominal exchange rate change (%)
            inflation_differential: (Domestic inflation - Foreign inflation) in %
        
        Returns:
            dict with real exchange rate change and interpretation
        
        Example:
            >>> calc = ExchangeRateCalculator()
            >>> # KRW nominal depreciation: -7.46%
            >>> # Korea inflation 2.3% - Swiss 1.4% = 0.9% differential
            >>> result = calc.calculate_competitiveness_index(-7.46, 0.9)
            >>> print(f"Real depreciation: {result['real_change']:.2f}%")
        """
        # Real exchange rate change = Nominal change + Inflation differential
        # Positive inflation differential reduces real depreciation
        real_change = exchange_rate_change + inflation_differential
        
        interpretation = ""
        if real_change < 0:
            interpretation = (
                f"Real depreciation of {abs(real_change):.2f}%. "
                f"The currency has genuinely weakened in competitiveness terms. "
                f"Exporters gain real advantage."
            )
        elif real_change > 0:
            interpretation = (
                f"Real appreciation of {real_change:.2f}%. "
                f"The currency has genuinely strengthened. "
                f"Exporters lose competitiveness."
            )
        else:
            interpretation = (
                "No change in real exchange rate. "
                "Nominal depreciation exactly offset by inflation differential."
            )
        
        return {
            'nominal_change': exchange_rate_change,
            'inflation_differential': inflation_differential,
            'real_change': real_change,
            'interpretation': interpretation
        }


class ParityCalculator:
    """Calculate Interest Rate Parity (IRP) and Purchasing Power Parity (PPP)"""
    
    @staticmethod
    def interest_rate_parity(spot_rate: float, 
                            domestic_rate: float, 
                            foreign_rate: float,
                            time_period: float = 1.0) -> Dict:
        """
        Calculate Interest Rate Parity (IRP)
        
        **Covered Interest Rate Parity Formula:**
        F = S₀ × [(1 + i_foreign × t) / (1 + i_domestic × t)]
        
        Where:
        - F = Forward exchange rate
        - S₀ = Spot exchange rate (domestic currency per foreign currency)
        - i_domestic = Domestic interest rate (annual, as decimal)
        - i_foreign = Foreign interest rate (annual, as decimal)
        - t = Time period in years (default: 1 year)
        
        **Economic Intuition:**
        If domestic rates > foreign rates:
        → Domestic currency trades at FORWARD DISCOUNT (expected to depreciate)
        → High domestic rates attract capital, but IRP requires depreciation to prevent arbitrage
        
        Args:
            spot_rate: Current exchange rate (e.g., 0.00062 CHF per KRW)
            domestic_rate: Domestic interest rate (e.g., 0.0325 for Korea's 3.25%)
            foreign_rate: Foreign interest rate (e.g., 0.0125 for Swiss 1.25%)
            time_period: Time horizon in years (default: 1 year)
        
        Returns:
            dict with:
                - formula: The IRP formula used
                - spot_rate, domestic_rate, foreign_rate: Input values
                - forward_rate: Calculated forward rate
                - implied_change_pct: Expected currency change (%)
                - interpretation: Economic meaning
                - substitution_steps: Step-by-step calculation
                - arbitrage_check: Whether arbitrage opportunities exist
        
        Example (Korea-Switzerland):
            >>> calc = ParityCalculator()
            >>> result = calc.interest_rate_parity(
            ...     spot_rate=0.00062,  # 1 KRW = 0.00062 CHF
            ...     domestic_rate=0.0325,  # Korea 3.25%
            ...     foreign_rate=0.0125    # Swiss 1.25%
            ... )
            >>> print(f"Forward rate: {result['forward_rate']:.6f}")
            >>> print(f"KRW expected to depreciate by {abs(result['implied_change_pct']):.2f}%")
        """
        # Calculate forward rate using IRP formula
        forward_rate = spot_rate * ((1 + foreign_rate * time_period) / 
                                   (1 + domestic_rate * time_period))
        
        # Calculate implied change
        implied_change = ((forward_rate - spot_rate) / spot_rate) * 100
        
        # Determine interpretation
        rate_differential = (domestic_rate - foreign_rate) * 100
        
        if domestic_rate > foreign_rate:
            interpretation = (
                f"DOMESTIC CURRENCY EXPECTED TO DEPRECIATE by {abs(implied_change):.2f}% "
                f"(trades at forward discount).\n\n"
                f"**Economic Mechanism:**\n"
                f"1. Domestic interest rates ({domestic_rate*100:.2f}%) > Foreign rates ({foreign_rate*100:.2f}%)\n"
                f"2. Interest differential: +{rate_differential:.2f}% in favor of domestic currency\n"
                f"3. This attracts capital inflows → upward pressure on domestic currency\n"
                f"4. BUT: To prevent arbitrage, forward market must price in depreciation\n"
                f"5. Forward discount of {abs(implied_change):.2f}% offsets the {rate_differential:.2f}% interest advantage\n"
                f"6. Result: No risk-free arbitrage profit available\n\n"
                f"**For Korean Won (KRW):**\n"
                f"• Higher Korean rates (vs Switzerland) initially attract carry trade investors\n"
                f"• However, expected {abs(implied_change):.2f}% depreciation eliminates the arbitrage gain\n"
                f"• Korean exporters benefit from expected Won weakness\n"
                f"• Swiss investors face currency risk when investing in Korean bonds"
            )
        else:
            interpretation = (
                f"DOMESTIC CURRENCY EXPECTED TO APPRECIATE by {implied_change:.2f}% "
                f"(trades at forward premium).\n\n"
                f"**Economic Mechanism:**\n"
                f"1. Foreign interest rates ({foreign_rate*100:.2f}%) > Domestic rates ({domestic_rate*100:.2f}%)\n"
                f"2. Lower domestic rates reduce capital inflow\n"
                f"3. Forward premium of {implied_change:.2f}% compensates for lower interest returns\n"
                f"4. IRP maintains no-arbitrage equilibrium"
            )
        
        # Check for arbitrage opportunities
        # In real markets, if |implied_change| significantly differs from actual forward premium,
        # arbitrage exists
        arbitrage_check = {
            'covered_interest_arbitrage': f"IRP suggests no arbitrage if forward rate = {forward_rate:.6f}",
            'note': "If actual forward rate differs significantly, arbitrage opportunity may exist"
        }
        
        return {
            'formula': 'F = S₀ × [(1 + i_foreign × t) / (1 + i_domestic × t)]',
            'spot_rate': spot_rate,
            'domestic_rate': domestic_rate,
            'foreign_rate': foreign_rate,
            'time_period': time_period,
            'rate_differential_pct': rate_differential,
            'forward_rate': forward_rate,
            'implied_change_pct': implied_change,
            'direction': 'depreciation' if implied_change < 0 else 'appreciation',
            'interpretation': interpretation,
            'substitution_steps': [
                f"F = {spot_rate:.6f} × [(1 + {foreign_rate:.4f} × {time_period}) / (1 + {domestic_rate:.4f} × {time_period})]",
                f"F = {spot_rate:.6f} × [{1 + foreign_rate * time_period:.6f} / {1 + domestic_rate * time_period:.6f}]",
                f"F = {spot_rate:.6f} × {(1 + foreign_rate * time_period)/(1 + domestic_rate * time_period):.6f}",
               f"F = {forward_rate:.6f} CHF per KRW"
            ],
            'arbitrage_check': arbitrage_check
        }
    
    @staticmethod
    def purchasing_power_parity(spot_rate: float,
                                inflation_domestic: float,
                                inflation_foreign: float,
                                time_period: float = 1.0) -> Dict:
        """
        Calculate Purchasing Power Parity (PPP)
        
        **Relative PPP Formula:**
        E[S₁] = S₀ × [(1 + π_foreign × t) / (1 + π_domestic × t)]
        
        Where:
        - E[S₁] = Expected future spot rate
        - S₀ = Current spot rate
        - π_domestic = Domestic inflation rate (annual, as decimal)
        - π_foreign = Foreign inflation rate (annual, as decimal)
        - t = Time period in years
        
        **Economic Intuition:**
        If domestic inflation > foreign inflation:
        → Domestic currency expected to DEPRECIATE
        → Erosion of purchasing power leads to currency weakness
        
        Args:
            spot_rate: Current exchange rate (e.g., 0.00062 CHF per KRW)
            inflation_domestic: Domestic inflation rate (e.g., 0.023 for Korea's 2.3%)
            inflation_foreign: Foreign inflation rate (e.g., 0.014 for Swiss 1.4%)
            time_period: Time horizon in years (default: 1)
        
        Returns:
            dict with expected rate, change, and interpretation
        
        Example:
            >>> calc = ParityCalculator()
            >>> result = calc.purchasing_power_parity(
            ...     spot_rate=0.00062,
            ...     inflation_domestic=0.023,  # Korea 2.3%
            ...     inflation_foreign=0.014    # Swiss 1.4%
            ... )
            >>> print(f"Expected rate: {result['expected_rate']:.6f}")
        """
        # Calculate expected future rate using PPP formula
        expected_rate = spot_rate * ((1 + inflation_foreign * time_period) / 
                                    (1 + inflation_domestic * time_period))
        
        # Calculate implied change
        implied_change = ((expected_rate - spot_rate) / spot_rate) * 100
        
        # Inflation differential
        inflation_diff = (inflation_domestic - inflation_foreign) * 100
        
        # Interpretation
        if inflation_domestic > inflation_foreign:
            interpretation = (
                f"DOMESTIC CURRENCY EXPECTED TO DEPRECIATE by {abs(implied_change):.2f}% "
                f"due to higher domestic inflation.\n\n"
                f"**Economic Mechanism:**\n"
                f"1. Domestic inflation ({inflation_domestic*100:.2f}%) > Foreign inflation ({inflation_foreign*100:.2f}%)\n"
                f"2. Inflation differential: +{inflation_diff:.2f}%\n"
                f"3. Higher domestic inflation erodes purchasing power\n"
                f"4. Domestic goods become relatively more expensive\n"
                f"5. Currency depreciates to restore purchasing power parity\n\n"
                f"**For Korean Won (KRW):**\n"
                f"• Korean prices rising faster than Swiss prices\n"
                f"• Korean goods lose competitiveness unless KRW weakens\n"
                f"• PPP predicts ~{abs(implied_change):.2f}% KRW depreciation to compensate"
            )
        else:
            interpretation = (
                f"DOMESTIC CURRENCY EXPECTED TO APPRECIATE by {implied_change:.2f}% "
                f"due to lower domestic inflation.\n\n"
                f"**Economic Mechanism:**\n"
                f"1. Foreign inflation ({inflation_foreign*100:.2f}%) > Domestic inflation ({inflation_domestic*100:.2f}%)\n"
                f"2. Stronger domestic purchasing power supports currency\n"
                f"3. Domestic goods become relatively cheaper\n"
                f"4. Currency appreciates per PPP theory"
            )
        
        return {
            'formula': 'E[S₁] = S₀ × [(1 + π_foreign × t) / (1 + π_domestic × t)]',
            'spot_rate': spot_rate,
            'inflation_domestic': inflation_domestic,
            'inflation_foreign': inflation_foreign,
            'time_period': time_period,
            'inflation_differential_pct': inflation_diff,
            'expected_rate': expected_rate,
            'implied_change_pct': implied_change,
            'direction': 'depreciation' if implied_change < 0 else 'appreciation',
            'interpretation': interpretation,
            'substitution_steps': [
                f"E[S₁] = {spot_rate:.6f} × [(1 + {inflation_foreign:.4f} × {time_period}) / (1 + {inflation_domestic:.4f} × {time_period})]",
                f"E[S₁] = {spot_rate:.6f} × [{1 + inflation_foreign * time_period:.6f} / {1 + inflation_domestic * time_period:.6f}]",
                f"E[S₁] = {spot_rate:.6f} × {(1 + inflation_foreign * time_period)/(1 + inflation_domestic * time_period):.6f}",
                f"E[S₁] = {expected_rate:.6f} CHF per KRW"
            ]
        }


class StatisticalAnalyzer:
    """Advanced statistical analysis for forex data"""
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, annualize: bool = True) -> float:
        """
        Calculate volatility (standard deviation of returns)
        
        Args:
            returns: Series of daily returns
            annualize: If True, annualize the volatility (multiply by sqrt(252))
        
        Returns:
            float: Volatility
        
        Example:
            >>> returns = forex_data['cross_rate'].pct_change().dropna()
            >>> analyzer = StatisticalAnalyzer()
            >>> vol = analyzer.calculate_volatility(returns)
            >>> print(f"Annualized volatility: {vol*100:.2f}%")
        """
        volatility = returns.std()
        if annualize:
            volatility = volatility * np.sqrt(252)  # 252 trading days per year
        return volatility
    
    @staticmethod
    def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR)
        
        VaR represents the maximum expected loss over a given time period
        at a specified confidence level.
        
        Args:
            returns: Series of daily returns
            confidence: Confidence level (default: 0.95 for 95%)
        
        Returns:
            float: VaR value (negative number representing potential loss)
        
        Example:
            >>> var_95 = analyzer.calculate_var(returns, 0.95)
            >>> print(f"95% VaR: {var_95*100:.2f}% (max loss on worst 5% of days)")
        """
        return np.percentile(returns, (1 - confidence) * 100)
    
    @staticmethod
    def moving_average(data: pd.Series, window: int) -> pd.Series:
        """
        Calculate moving average
        
        Args:
            data: Time series data
            window: Window size in days
        
        Returns:
            pd.Series: Moving average
        
        Example:
            >>> ma_20 = analyzer.moving_average(forex_data['cross_rate'], 20)
        """
        return data.rolling(window=window).mean()
    
    @staticmethod
    def correlation_with_returns(rate_series: pd.Series, 
                                 market_index: pd.Series) -> Dict:
        """
        Calculate correlation between currency returns and market returns
        
        Useful for understanding if KRW moves with global risk sentiment.
        
        Args:
            rate_series: Currency rate series
            market_index: Market index series (e.g., S&P 500, KOSPI)
        
        Returns:
            dict with correlation coefficient and interpretation
        """
        # Calculate returns
        currency_returns = rate_series.pct_change().dropna()
        market_returns = market_index.pct_change().dropna()
        
        # Align dates
        aligned_data = pd.DataFrame({
            'currency': currency_returns,
            'market': market_returns
        }).dropna()
        
        correlation = aligned_data['currency'].corr(aligned_data['market'])
        
        if correlation > 0.5:
            interpretation = "High positive correlation: Currency moves with market (pro-cyclical)"
        elif correlation < -0.5:
            interpretation = "High negative correlation: Currency moves opposite to market (counter-cyclical/safe haven)"
        else:
            interpretation = "Low correlation: Currency relatively independent of market movements"
        
        return {
            'correlation': correlation,
            'interpretation': interpretation,
            'n_observations': len(aligned_data)
        }


if __name__ == "__main__":
    # Test the module
    print("Testing calculators.py module...\n")
    
    # Test 1: Exchange rate change
    print("=" * 60)
    print("TEST 1: Exchange Rate Change (KRW/CHF)")
    print("=" * 60)
    calc = ExchangeRateCalculator()
    result = calc.calculate_percentage_change(0.00067, 0.00062)
    print(f"Old rate: {result['old_rate']:.6f} CHF per KRW")
    print(f"New rate: {result['new_rate']:.6f} CHF per KRW")
    print(f"Change: {result['percentage_change']:.2f}%")
    print(f"Direction: {result['direction']}")
    
    # Test 2: Impact analysis
    print("\n" + "=" * 60)
    print("TEST 2: Impact Analysis")
    print("=" * 60)
    impact = calc.analyze_impact(result['percentage_change'])
    print(f"Exporters: {impact['exporters']['impact']}")
    print(f"  → {impact['exporters']['reason']}")
    print(f"Importers: {impact['importers']['impact']}")
    print(f"  → {impact['importers']['reason']}")
    
    # Test 3: Interest Rate Parity
    print("\n" + "=" * 60)
    print("TEST 3: Interest Rate Parity (Korea vs Switzerland)")
    print("=" * 60)
    parity_calc = ParityCalculator()
    irp = parity_calc.interest_rate_parity(
        spot_rate=0.00062,
        domestic_rate=0.0325,  # Korea 3.25%
        foreign_rate=0.0125    # Swiss 1.25%
    )
    print(f"Spot rate: {irp['spot_rate']:.6f} CHF per KRW")
    print(f"Forward rate: {irp['forward_rate']:.6f} CHF per KRW")
    print(f"Expected change: {irp['implied_change_pct']:.2f}%")
    print(f"Direction: {irp['direction']}")
    
    print("\nAll calculator tests passed!")
