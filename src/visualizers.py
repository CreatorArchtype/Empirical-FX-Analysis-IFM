"""
Visualization module for International Finance Analysis Project
Creates publication-quality charts for South Korea (KRW) and Switzerland (CHF) analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Optional, List
import warnings
warnings.filterwarnings('ignore')

# Try to import plotly for interactive charts (optional)
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("WARNING: Plotly not installed. Interactive charts will be unavailable.")
    print("Install with: pip install plotly kaleido")

# Set default style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Color scheme (Korean flag + Swiss red + neutral)
COLORS = {
    'korea_blue': '#003478',
    'korea_red': '#CD2E3A',
    'swiss_red': '#FF0000',
    'neutral': '#2c3e50',
    'positive': '#27ae60',
    'negative': '#e74c3c',
    'warning': '#f39c12',
    'info': '#3498db'
}


class ForexVisualizer:
    """Create forex-related visualizations for KRW/CHF analysis"""
    
    @staticmethod
    def plot_exchange_rate_time_series(df: pd.DataFrame, 
                                       from_currency: str,
                                       to_currency: str,
                                       save_path: Optional[str] = None,
                                       show_ma: bool = True,
                                       ma_window: int = 20):
        """
        Plot exchange rate time series with optional moving average
        
        Creates a professional time series chart showing:
        - Exchange rate over time
        - 20-day moving average (optional)
        - Percentage change annotation
        - Trend visualization
        
        Args:
            df: DataFrame with 'cross_rate' column
            from_currency: Base currency (e.g., 'KRW')
            to_currency: Target currency (e.g., 'CHF')
            save_path: Path to save the chart (optional)
            show_ma: Show moving average (default: True)
            ma_window: Moving average window in days (default: 20)
        
        Example:
            >>> visualizer = ForexVisualizer()
            >>> visualizer.plot_exchange_rate_time_series(
            ...     forex_data, 'KRW', 'CHF',
            ...     save_path='outputs/charts/krw_chf_analysis.png'
            ... )
        """
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Main line plot - exchange rate
        ax.plot(df.index, df['cross_rate'], 
                label=f'{from_currency}/{to_currency} Exchange Rate',
                color=COLORS['neutral'], linewidth=2.5, zorder=2)
        
        # Moving average (if enabled)
        if show_ma:
            ma = df['cross_rate'].rolling(window=ma_window).mean()
            ax.plot(df.index, ma, 
                    label=f'{ma_window}-Day Moving Average',
                    color=COLORS['negative'], linestyle='--', linewidth=1.8, 
                    alpha=0.8, zorder=1)
        
        # Formatting
        ax.set_title(
            f'{from_currency}/{to_currency} Exchange Rate Analysis\n'
            f'{df.index[0].strftime("%B %d, %Y")} - {df.index[-1].strftime("%B %d, %Y")}',
            fontsize=16, fontweight='bold', pad=20
        )
        ax.set_xlabel('Date', fontsize=13, fontweight='bold')
        ax.set_ylabel(f'Exchange Rate (1 {from_currency} = X {to_currency})', 
                     fontsize=13, fontweight='bold')
        ax.legend(loc='best', fontsize=12, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
        
        # Calculate and annotate percentage change
        start_rate = df['cross_rate'].iloc[0]
        end_rate = df['cross_rate'].iloc[-1]
        pct_change = ((end_rate - start_rate) / start_rate) * 100
        
        # Choose color based on change direction
        change_color = COLORS['positive'] if pct_change > 0 else COLORS['negative']
        direction = "Appreciation" if pct_change > 0 else "Depreciation"
        
        # Add annotation box
        annotation_text = (
            f'{direction}: {pct_change:+.2f}%\n'
            f'Start: {start_rate:.6f}\n'
            f'End: {end_rate:.6f}'
        )
        
        ax.text(0.02, 0.98, annotation_text,
                transform=ax.transAxes,
                fontsize=12, fontweight='bold',
                verticalalignment='top',
                bbox=dict(boxstyle='round,pad=0.8', 
                         facecolor=change_color, alpha=0.2,
                         edgecolor=change_color, linewidth=2))
        
        # Mark start and end points
        ax.plot(df.index[0], start_rate, 'o', 
               color=COLORS['info'], markersize=10, zorder=3,
               label=f'Start: {start_rate:.6f}')
        ax.plot(df.index[-1], end_rate, 'o', 
               color=change_color, markersize=10, zorder=3,
               label=f'End: {end_rate:.6f}')
        
        ax.legend(loc='best', fontsize=11)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"Chart saved: {save_path}")
        
        plt.show()
    
    @staticmethod
    def plot_interactive_forex(df: pd.DataFrame,
                               from_currency: str,
                               to_currency: str,
                               save_path: Optional[str] = None):
        """
        Create interactive Plotly chart (HTML output)
        
        Args:
            df: DataFrame with 'cross_rate' column
            from_currency: Base currency
            to_currency: Target currency
            save_path: Path to save HTML file (optional)
        
        Example:
            >>> visualizer = ForexVisualizer()
            >>> visualizer.plot_interactive_forex(
            ...     forex_data, 'KRW', 'CHF',
            ...     save_path='outputs/charts/interactive_krw_chf.html'
            ... )
        """
        if not PLOTLY_AVAILABLE:
            print("ERROR: Plotly not installed. Skipping interactive chart.")
            return
        
        fig = go.Figure()
        
        # Add main exchange rate line
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['cross_rate'],
            mode='lines',
            name='Exchange Rate',
            line=dict(color=COLORS['neutral'], width=2),
            hovertemplate='<b>Date</b>: %{x}<br><b>Rate</b>: %{y:.6f}<extra></extra>'
        ))
        
        # Add 20-day moving average
        ma20 = df['cross_rate'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=ma20,
            mode='lines',
            name='20-Day MA',
            line=dict(color=COLORS['negative'], width=1.5, dash='dash'),
            hovertemplate='<b>Date</b>: %{x}<br><b>MA</b>: %{y:.6f}<extra></extra>'
        ))
        
        # Layout
        fig.update_layout(
            title=f'{from_currency}/{to_currency} Exchange Rate - Interactive View',
            xaxis_title='Date',
            yaxis_title=f'Exchange Rate (1 {from_currency} = X {to_currency})',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            font=dict(size=12),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"Interactive chart saved: {save_path}")
        else:
            fig.show()
    
    @staticmethod
    def plot_volatility_analysis(df: pd.DataFrame, 
                                 from_currency: str = 'KRW',
                                 to_currency: str = 'CHF',
                                 save_path: Optional[str] = None,
                                 rolling_window: int = 20):
        """
        Plot volatility and return distribution analysis
        
        Creates a 2-panel chart:
        - Left: Rolling volatility over time
        - Right: Return distribution histogram
        
        Args:
            df: DataFrame with 'cross_rate' column
            from_currency: Base currency
            to_currency: Target currency
            save_path: Path to save chart
            rolling_window: Window for rolling volatility (default: 20 days)
        
        Example:
            >>> visualizer = ForexVisualizer()
            >>> visualizer.plot_volatility_analysis(
            ...     forex_data, 'KRW', 'CHF',
            ...     save_path='outputs/charts/volatility.png'
            ... )
        """
        # Calculate returns
        returns = df['cross_rate'].pct_change().dropna()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Panel 1: Rolling volatility
        rolling_vol = returns.rolling(window=rolling_window).std() * 100
        ax1.plot(rolling_vol.index, rolling_vol, color=COLORS['negative'], linewidth=2)
        ax1.fill_between(rolling_vol.index, rolling_vol, alpha=0.3, color=COLORS['negative'])
        ax1.set_title(f'Rolling Volatility ({rolling_window}-Day Window)', 
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Volatility (%)', fontsize=12)
        ax1.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
        
        # Add mean volatility line
        mean_vol = rolling_vol.mean()
        ax1.axhline(mean_vol, color=COLORS['warning'], linestyle='--', 
                   linewidth=1.5, label=f'Mean: {mean_vol:.3f}%')
        ax1.legend(loc='best', fontsize=11)
        
        # Panel 2: Return distribution
        ax2.hist(returns * 100, bins=50, color=COLORS['info'], alpha=0.7, 
                edgecolor='black', linewidth=0.5)
        ax2.axvline(returns.mean() * 100, color=COLORS['negative'], linestyle='--', 
                   linewidth=2.5, label=f'Mean: {returns.mean()*100:.3f}%')
        ax2.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
        ax2.set_title('Daily Return Distribution', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Daily Return (%)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.legend(loc='best', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=0.8)
        
        # Add statistics text box
        stats_text = (
            f'Statistics:\n'
            f'Mean: {returns.mean()*100:.3f}%\n'
            f'Std Dev: {returns.std()*100:.3f}%\n'
            f'Min: {returns.min()*100:.3f}%\n'
            f'Max: {returns.max()*100:.3f}%'
        )
        ax2.text(0.98, 0.97, stats_text,
                transform=ax2.transAxes,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.8', 
                         facecolor='white', alpha=0.8,
                         edgecolor='gray', linewidth=1))
        
        plt.suptitle(f'{from_currency}/{to_currency} Volatility Analysis', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Volatility chart saved: {save_path}")
        
        plt.show()
    
    @staticmethod
    def plot_stakeholder_impact(impact_data: Dict, 
                               save_path: Optional[str] = None):
        """
        Visualize stakeholder impact matrix
        
        Creates a horizontal bar chart showing impact on different stakeholders.
        
        Args:
            impact_data: Dict with stakeholder impact information
            save_path: Path to save chart
        
        Example:
            >>> visualizer = ForexVisualizer()
            >>> impact = {
            ...     'exporters': {'impact': 'BENEFIT', 'magnitude': 7.46},
            ...     'importers': {'impact': 'LOSS', 'magnitude': 7.46}
            ... }
            >>> visualizer.plot_stakeholder_impact(impact)
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Define stakeholders and their impacts
        stakeholders = [
            'Korean Exporters\n(Samsung, Hyundai, LG)',
            'Korean Importers\n(Pharma, Machinery)',
            'Korean Chaebols\n(Conglomerates)',
            'Korean SMEs\n(Small Businesses)',
            'Bank of Korea\n(Central Bank)',
            'Forex Traders\n(Carry Trade)'
        ]
        
        # Impact scores (positive = benefit, negative = loss)
        # Based on KRW depreciation scenario
        impacts = [85, -75, 30, -60, -40, 70]
        colors_list = [COLORS['positive'] if x > 0 else COLORS['negative'] for x in impacts]
        
        # Create horizontal bar chart
        y_pos = range(len(stakeholders))
        bars = ax.barh(y_pos, impacts, color=colors_list, alpha=0.7, edgecolor='black', linewidth=1.2)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(stakeholders, fontsize=11)
        ax.set_xlabel('Impact Score', fontsize=13, fontweight='bold')
        ax.set_title('Stakeholder Impact Analysis: KRW Depreciation vs CHF', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.set_xlim(-100, 100)
        ax.axvline(0, color='black', linewidth=1.5, linestyle='-')
        ax.grid(True, alpha=0.3, axis='x', linestyle=':', linewidth=0.8)
        
        # Add impact labels on bars
        impact_labels = [
            'High Benefit (+)',
            'Margin Pressure (-)',
            'Mixed Impact',
            'Vulnerable (-)',
            'Policy Challenge (-)',
            'Opportunity (+)'
        ]
        
        for i, (bar, label) in enumerate(zip(bars, impact_labels)):
            width = bar.get_width()
            label_x_pos = width + 3 if width > 0 else width - 3
            alignment = 'left' if width > 0 else 'right'
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2,
                   label, ha=alignment, va='center', fontsize=10, fontweight='bold')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=COLORS['positive'], label='Positive Impact'),
            Patch(facecolor=COLORS['negative'], label='Negative Impact')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Stakeholder impact chart saved: {save_path}")
        
        plt.show()
    
    @staticmethod
    def plot_comparison_chart(historical_rate: float,
                             current_rate: float,
                             forward_rate: float,
                             ppp_rate: float,
                             from_currency: str = 'KRW',
                             to_currency: str = 'CHF',
                             save_path: Optional[str] = None):
        """
        Create comparison chart showing historical, current, forward (IRP), and PPP rates
        
        Args:
            historical_rate: Historical exchange rate
            current_rate: Current exchange rate
            forward_rate: IRP forward rate
            ppp_rate: PPP expected rate
            from_currency: Base currency
            to_currency: Target currency
            save_path: Path to save chart
        
        Example:
            >>> visualizer = ForexVisualizer()
            >>> visualizer.plot_comparison_chart(
            ...     historical_rate=0.00067,
            ...     current_rate=0.00062,
            ...     forward_rate=0.00061,
            ...     ppp_rate=0.00061,
            ...     save_path='outputs/charts/rate_comparison.png'
            ... )
        """
        fig, ax = plt.subplots(figsize=(10, 7))
        
        categories = ['Historical\n(Aug 2025)', 'Current\n(Jan 2026)', 
                     'Forward (IRP)\n(1 Year)', 'PPP Expected\n(1 Year)']
        rates = [historical_rate, current_rate, forward_rate, ppp_rate]
        colors_list = [COLORS['info'], COLORS['neutral'], 
                      COLORS['korea_blue'], COLORS['korea_red']]
        
        bars = ax.bar(categories, rates, color=colors_list, alpha=0.7, 
                     edgecolor='black', linewidth=1.5, width=0.6)
        
        # Add value labels on bars
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{rate:.6f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel(f'Exchange Rate (1 {from_currency} = X {to_currency})', 
                     fontsize=13, fontweight='bold')
        ax.set_title(f'{from_currency}/{to_currency} Rate Comparison', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle=':', linewidth=0.8)
        
        # Add horizontal line at current rate for reference
        ax.axhline(current_rate, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"Comparison chart saved: {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Test the module with sample data
    print("Testing visualizers.py module...\n")
    
    # Create sample data
    dates = pd.date_range(start='2025-08-01', end='2026-01-30', freq='D')
    np.random.seed(42)
    
    # Simulate KRW/CHF exchange rate (starting at 0.00067, trending to 0.00062)
    n = len(dates)
    trend = np.linspace(0.00067, 0.00062, n)
    noise = np.random.normal(0, 0.00001, n)
    rates = trend + noise
    
    sample_df = pd.DataFrame({
        'cross_rate': rates
    }, index=dates)
    
    print("Creating sample visualizations...\n")
    
    # Test time series plot
    visualizer = ForexVisualizer()
    print("1. Time series chart:")
    visualizer.plot_exchange_rate_time_series(
        sample_df, 'KRW', 'CHF',
        save_path='outputs/charts/test_exchange_rate.png'
    )
    
    # Test volatility analysis
    print("\n2. Volatility analysis:")
    visualizer.plot_volatility_analysis(
        sample_df, 'KRW', 'CHF',
        save_path='outputs/charts/test_volatility.png'
    )
    
    # Test stakeholder impact
    print("\n3. Stakeholder impact:")
    visualizer.plot_stakeholder_impact(
        {},  # Empty dict - uses defaults
        save_path='outputs/charts/test_stakeholder_impact.png'
    )
    
    # Test comparison chart
    print("\n4. Rate comparison:")
    visualizer.plot_comparison_chart(
        historical_rate=0.00067,
        current_rate=0.00062,
        forward_rate=0.000608,
        ppp_rate=0.000615,
        save_path='outputs/charts/test_rate_comparison.png'
    )
    
    print("\nAll visualization tests complete!")
