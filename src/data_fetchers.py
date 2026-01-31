"""
Data fetching module for International Finance Analysis Project
Handles all API calls and data retrieval for South Korea (KRW) and Switzerland (CHF)
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import os
import sys

class ForexDataFetcher:
    """Fetch foreign exchange data for KRW/CHF currency pair"""
    
    def __init__(self, cache_dir='data/cache'):
        """
        Initialize ForexDataFetcher
        
        Args:
            cache_dir: Directory to store cached API responses
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_exchange_rate_yfinance(self, from_currency, to_currency, 
                                     start_date, end_date):
        """
        Fetch exchange rate using yfinance (FREE, no API key required)
        
        This is the RECOMMENDED method for KRW/CHF analysis as it requires no setup.
        
        Args:
            from_currency: Base currency code (e.g., 'KRW')
            to_currency: Target currency code (e.g., 'CHF')
            start_date: Start date (YYYY-MM-DD string or datetime)
            end_date: End date (YYYY-MM-DD string or datetime)
        
        Returns:
            pandas.DataFrame with columns:
                - from_usd_rate: Base currency per USD
                - to_usd_rate: Target currency per USD
                - cross_rate: Base currency per target currency (1 KRW = X CHF)
        
        Example:
            >>> fetcher = ForexDataFetcher()
            >>> data = fetcher.get_exchange_rate_yfinance('KRW', 'CHF', '2025-08-01', '2026-01-30')
            >>> print(f"1 KRW = {data['cross_rate'].iloc[-1]:.6f} CHF")
        """
        # Check cache first
        cache_file = f"{self.cache_dir}/{from_currency}_{to_currency}_{start_date}_{end_date}.csv"
        if os.path.exists(cache_file):
            print(f"Loading from cache: {cache_file}")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        
        print(f"Fetching {from_currency}/{to_currency} data from yfinance...")
        
        try:
            # Fetch USD rates for both currencies
            # Format: 'KRW=X' means KRW per USD
            from_usd = yf.download(f'{from_currency}=X', start=start_date, end=end_date, progress=False)
            to_usd = yf.download(f'{to_currency}=X', start=start_date, end=end_date, progress=False)
            
            # Calculate cross rate: 1 KRW = X CHF
            # Formula: (1 / KRW_per_USD) * CHF_per_USD
            df = pd.DataFrame()
            df['from_usd_rate'] = from_usd['Close']
            df['to_usd_rate'] = to_usd['Close']
            df['cross_rate'] = (1 / df['from_usd_rate']) * df['to_usd_rate']
            
            # Remove any NaN values
            df = df.dropna()
            
            # Save to cache
            df.to_csv(cache_file)
            print(f"Fetched {len(df)} days of data and cached")
            
            return df
        
        except Exception as e:
            print(f"ERROR: Error fetching data from yfinance: {e}")
            print(f"TIP: Check your internet connection and verify currency codes")
            raise
    
    def get_exchange_rate_alphavantage(self, from_currency, to_currency, api_key):
        """
        Fetch exchange rate using Alpha Vantage API (OPTIONAL - better data quality)
        
        Requires API key from: https://www.alphavantage.co/support/#api-key
        FREE tier: 25 requests/day
        PAID tier: $50/month for 500 requests/day
        
        Args:
            from_currency: Base currency code (e.g., 'KRW')
            to_currency: Target currency code (e.g., 'CHF')
            api_key: Alpha Vantage API key
        
        Returns:
            pandas.DataFrame with columns: Open, High, Low, Close
        
        Example:
            >>> fetcher = ForexDataFetcher()
            >>> data = fetcher.get_exchange_rate_alphavantage('KRW', 'CHF', 'YOUR_API_KEY')
        """
        if not api_key:
            raise ValueError("Alpha Vantage API key is required. Get one at https://www.alphavantage.co/support/#api-key")
        
        print(f"Fetching {from_currency}/{to_currency} data from Alpha Vantage...")
        
        url = "https://www.alphavantage.co/query"
        params = {
            'function': 'FX_DAILY',
            'from_symbol': from_currency,
            'to_symbol': to_currency,
            'apikey': api_key,
            'outputsize': 'full'  # Get full historical data (20 years)
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            # Check for errors
            if 'Error Message' in data:
                raise ValueError(f"API Error: {data['Error Message']}")
            if 'Note' in data:
                raise ValueError(f"API Rate Limit: {data['Note']}")
            if 'Time Series FX (Daily)' not in data:
                raise ValueError(f"Unexpected API response: {data}")
            
            # Convert to DataFrame
            time_series = data['Time Series FX (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.astype(float)
            df.columns = ['Open', 'High', 'Low', 'Close']
            df = df.sort_index()
            
            print(f"Fetched {len(df)} days of data from Alpha Vantage")
            
            return df
        
        except Exception as e:
            print(f"ERROR: Error fetching data from Alpha Vantage: {e}")
            raise


class InterestRateFetcher:
    """Fetch interest rate data for South Korea and Switzerland"""
    
    def __init__(self, fred_api_key=None):
        """
        Initialize InterestRateFetcher
        
        Args:
            fred_api_key: FRED API key (optional)
                Get from: https://fred.stlouisfed.org/docs/api/api_key.html
        """
        self.fred_api_key = fred_api_key
    
    def get_fred_rate(self, series_id, observation_date=None):
        """
        Fetch interest rate from FRED (Federal Reserve Economic Data)
        
        FRED Series IDs for Korea-Switzerland analysis:
        - 'INTDSRKRM193N': South Korea Policy Rate (Bank of Korea Base Rate)
        - 'IRSTCI01CHM156N': Switzerland Policy Rate (Swiss National Bank)
        - 'DFF': US Federal Funds Rate
        - 'ECBDFR': ECB Deposit Facility Rate
        
        Args:
            series_id: FRED series ID
            observation_date: Specific date (YYYY-MM-DD) or None for latest
        
        Returns:
            float: Interest rate as decimal (e.g., 0.0325 for 3.25%)
        
        Example:
            >>> fetcher = InterestRateFetcher('YOUR_FRED_API_KEY')
            >>> korea_rate = fetcher.get_fred_rate('INTDSRKRM193N')
            >>> print(f"Korea rate: {korea_rate*100:.2f}%")
        """
        if not self.fred_api_key:
            raise ValueError("FRED API key is required. Get one at https://fred.stlouisfed.org/docs/api/api_key.html")
        
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.fred_api_key,
            'file_type': 'json',
            'sort_order': 'desc',
            'limit': 10  # Get last 10 observations to find most recent non-empty value
        }
        
        if observation_date:
            params['observation_start'] = observation_date
            params['observation_end'] = observation_date
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'observations' not in data or len(data['observations']) == 0:
                raise ValueError(f"No data found for series {series_id}")
            
            # Get the most recent non-empty value
            for obs in data['observations']:
                if obs['value'] != '.':
                    rate_pct = float(obs['value'])
                    rate_decimal = rate_pct / 100  # Convert percentage to decimal
                    print(f"Fetched rate from FRED: {rate_pct}% (series: {series_id})")
                    return rate_decimal
            
            raise ValueError(f"No valid data found for series {series_id}")
        
        except Exception as e:
            print(f"ERROR: Error fetching FRED data: {e}")
            raise
    
    def get_korea_switzerland_rates(self):
        """
        Fetch interest rates specifically for South Korea and Switzerland
        
        Returns:
            dict: {'KRW': korea_rate, 'CHF': swiss_rate}
        
        Example:
            >>> fetcher = InterestRateFetcher('YOUR_FRED_API_KEY')
            >>> rates = fetcher.get_korea_switzerland_rates()
            >>> print(f"Interest rate differential: {(rates['KRW'] - rates['CHF'])*100:.2f}%")
        """
        print("Fetching Korea and Switzerland interest rates from FRED...")
        
        korea_rate = self.get_fred_rate('INTDSRKRM193N')
        swiss_rate = self.get_fred_rate('IRSTCI01CHM156N')
        
        return {
            'KRW': korea_rate,
            'CHF': swiss_rate
        }
    
    def get_manual_rates(self):
        """
        Return manually specified rates (FALLBACK method - no API needed)
        
        Use this if you don't have FRED API key or if API is unavailable.
        Rates are from January 2026 based on project document.
        
        Data sources for manual verification:
        - Bank of Korea: https://www.bok.or.kr/eng/main/main.do
        - Swiss National Bank: https://www.snb.ch/en/
        - Trading Economics: https://tradingeconomics.com/
        
        Returns:
            dict: Manual interest rates as decimals
        
        Example:
            >>> fetcher = InterestRateFetcher()
            >>> rates = fetcher.get_manual_rates()
            >>> print(f"Korea: {rates['KRW']*100}%")
        """
        print("Using manual interest rates (as of January 2026)")
        
        rates = {
            'KRW': 0.0325,  # 3.25% - Bank of Korea base rate
            'CHF': 0.0125,  # 1.25% - Swiss National Bank policy rate
            'USD': 0.0525,  # 5.25% - US Federal Reserve
            'EUR': 0.0400,  # 4.00% - European Central Bank
        }
        
        print(f"  • South Korea (KRW): {rates['KRW']*100:.2f}%")
        print(f"  • Switzerland (CHF): {rates['CHF']*100:.2f}%")
        print(f"  • Differential: {(rates['KRW'] - rates['CHF'])*100:.2f}% (Korea higher)")
        
        return rates


class InflationDataFetcher:
    """Fetch inflation data for South Korea and Switzerland (for PPP calculations)"""
    
    def get_worldbank_inflation(self, country_codes, start_year=2020):
        """
        Fetch inflation data from World Bank
        
        Country codes:
        - 'KR': South Korea (Korea, Rep.)
        - 'CH': Switzerland
        
        Args:
            country_codes: List of ISO country codes (e.g., ['KR', 'CH'])
            start_year: Starting year for data (default: 2020)
        
        Returns:
            pandas.DataFrame with inflation rates by country and year
        
        Example:
            >>> fetcher = InflationDataFetcher()
            >>> inflation = fetcher.get_worldbank_inflation(['KR', 'CH'])
            >>> print(inflation)
        """
        try:
            import wbdata
            
            print(f"Fetching inflation data from World Bank for {country_codes}...")
            
            # World Bank indicator for CPI inflation rate (annual %)
            indicators = {'FP.CPI.TOTL.ZG': 'inflation'}
            date_range = (datetime(start_year, 1, 1), datetime.now())
            
            df = wbdata.get_dataframe(indicators, country=country_codes, date=date_range)
            
            print(f"Fetched inflation data from World Bank")
            print(df)
            
            return df
        
        except ImportError:
            print("WARNING: wbdata package not installed. Install with: pip install wbdata")
            print("Falling back to manual inflation data...")
            return self.get_manual_inflation()
        
        except Exception as e:
            print(f"ERROR: Error fetching World Bank data: {e}")
            print("Falling back to manual inflation data...")
            return self.get_manual_inflation()
    
    def get_manual_inflation(self):
        """
        Return manually specified inflation rates (FALLBACK method)
        
        Use this if World Bank API is unavailable.
        Rates are latest available (2024-2025) from national statistical offices.
        
        Data sources:
        - Statistics Korea (KOSTAT): https://kostat.go.kr/portal/eng/
        - Swiss Federal Statistical Office: https://www.bfs.admin.ch/
        - OECD: https://data.oecd.org/
        
        Returns:
            dict: Manual inflation rates as decimals
        
        Example:
            >>> fetcher = InflationDataFetcher()
            >>> inflation = fetcher.get_manual_inflation()
            >>> print(f"Korea inflation: {inflation['KRW']*100:.2f}%")
        """
        print("Using manual inflation rates (latest available)")
        
        inflation = {
            'KRW': 0.023,  # 2.3% - Statistics Korea (KOSTAT)
            'CHF': 0.014,  # 1.4% - Swiss Federal Statistical Office
        }
        
        print(f"  • South Korea: {inflation['KRW']*100:.2f}%")
        print(f"  • Switzerland: {inflation['CHF']*100:.2f}%")
        print(f"  • Differential: {(inflation['KRW'] - inflation['CHF'])*100:.2f}%")
        print(f"  • PPP Implication: Higher Korean inflation suggests KRW depreciation")
        
        return inflation


# ==========================================
# CONVENIENCE FUNCTION
# ==========================================

def fetch_all_korea_switzerland_data(start_date='2025-08-01', end_date='2026-01-30',
                                      alphavantage_key=None, fred_key=None):
    """
    Convenience function to fetch ALL data needed for Korea-Switzerland analysis
    
    This is a one-stop function to get:
    - KRW/CHF exchange rates (6 months)
    - Korea and Switzerland interest rates
    - Korea and Switzerland inflation rates
    
    Args:
        start_date: Start date for forex data (YYYY-MM-DD)
        end_date: End date for forex data (YYYY-MM-DD)
        alphavantage_key: Alpha Vantage API key (optional, defaults to yfinance)
        fred_key: FRED API key (optional, defaults to manual rates)
    
    Returns:
        dict with keys:
            - 'forex_data': DataFrame with KRW/CHF exchange rates
            - 'interest_rates': dict with KRW and CHF interest rates
            - 'inflation_rates': dict with KRW and CHF inflation rates
    
    Example:
        >>> data = fetch_all_korea_switzerland_data()
        >>> print(f"Fetched {len(data['forex_data'])} days of forex data")
        >>> print(f"Korea rate: {data['interest_rates']['KRW']*100}%")
    """
    print("=" * 60)
    print("FETCHING ALL KOREA-SWITZERLAND DATA")
    print("=" * 60)
    
    # 1. Fetch Forex Data (KRW/CHF)
    forex_fetcher = ForexDataFetcher()
    forex_data = forex_fetcher.get_exchange_rate_yfinance('KRW', 'CHF', start_date, end_date)
    
    # 2. Fetch Interest Rates
    interest_fetcher = InterestRateFetcher(fred_key)
    if fred_key:
        try:
            interest_rates = interest_fetcher.get_korea_switzerland_rates()
        except:
            print("WARNING: FRED API failed, using manual rates...")
            interest_rates = interest_fetcher.get_manual_rates()
    else:
        interest_rates = interest_fetcher.get_manual_rates()
    
    # 3. Fetch Inflation Rates
    inflation_fetcher = InflationDataFetcher()
    inflation_rates = inflation_fetcher.get_manual_inflation()
    
    print("\n" + "=" * 60)
    print("DATA FETCH COMPLETE")
    print("=" * 60)
    print(f"Forex data: {len(forex_data)} days")
    print(f"Interest rates: KRW {interest_rates['KRW']*100}%, CHF {interest_rates['CHF']*100}%")
    print(f"Inflation rates: KRW {inflation_rates['KRW']*100}%, CHF {inflation_rates['CHF']*100}%")
    
    return {
        'forex_data': forex_data,
        'interest_rates': interest_rates,
        'inflation_rates': inflation_rates
    }


if __name__ == "__main__":
    # Test the module
    print("Testing data_fetchers.py module...")
    
    # Test forex fetching
    fetcher = ForexDataFetcher()
    data = fetcher.get_exchange_rate_yfinance('KRW', 'CHF', '2025-08-01', '2026-01-30')
    print(f"\nForex test: Fetched {len(data)} days of KRW/CHF data")
    print(f"Latest rate: 1 KRW = {data['cross_rate'].iloc[-1]:.6f} CHF")
    
    # Test interest rate fetching (manual)
    interest_fetcher = InterestRateFetcher()
    rates = interest_fetcher.get_manual_rates()
    print(f"\nInterest rate test: Korea {rates['KRW']*100}%, Swiss {rates['CHF']*100}%")
    
    # Test inflation fetching (manual)
    inflation_fetcher = InflationDataFetcher()
    inflation = inflation_fetcher.get_manual_inflation()
    print(f"\nInflation test: Korea {inflation['KRW']*100}%, Swiss {inflation['CHF']*100}%")
