from portfolio_analyzer import PortfolioManager, analyze_stock
import pandas as pd
from datetime import datetime, timedelta

def display_stock_analysis(symbols):
    """Analyze a list of stocks and display results in a table"""
    data = []
    
    for symbol in symbols:
        print(f"\nAnalyzing {symbol}...")
        analysis = analyze_stock(symbol)
        
        if analysis and 'stats' in analysis:
            stats = analysis['stats']
            price = stats['current_price']
            max_shares = int(20000 / price)
            data.append({
                'Symbol': symbol,
                'Current Price': f"${price:.2f}",
                '1-Month Change': f"{stats['price_change_1m']:.1f}%",
                'Volatility': f"{stats['volatility']:.1f}%" if stats['volatility'] else "N/A",
                'Max Shares @ $20k': max_shares,
                'Cost for Max Shares': f"${(max_shares * price):.2f}"
            })
    
    if data:
        return pd.DataFrame(data).set_index('Symbol')
    return pd.DataFrame()

def make_trade(portfolio, symbol, amount_to_invest):
    """Make a trade and display the results"""
    analysis = analyze_stock(symbol)
    
    if analysis and 'stats' in analysis:
        current_price = analysis['stats']['current_price']
        shares = min(
            int(amount_to_invest / current_price),
            int(20000 / current_price)
        )
        
        if shares > 0:
            portfolio.buy(symbol, shares, current_price)
            print(f"\nBought {shares} shares of {symbol} at ${current_price:.2f} per share")
            
            metrics = portfolio.get_performance_metrics()
            print("\nUpdated Portfolio Status:")
            print(f"Cash: ${metrics['cash']:.2f}")
            print(f"Total Value: ${metrics['total_value']:.2f}")
            print("\nPositions:")
            print(metrics['positions'])

# Create portfolio instances
active_portfolio = PortfolioManager()   # Portfolio A (Actively managed)
passive_portfolio = PortfolioManager()  # Portfolio B (Passively managed)

# Example analysis of tech stocks
print("\n=== Technology Sector Analysis ===")
tech_stocks = ['AAPL', 'MSFT', 'GOOGL']
tech_analysis = display_stock_analysis(tech_stocks)
if not tech_analysis.empty:
    print(tech_analysis)

# Example of making a trade
print("\n=== Making Sample Trade ===")
make_trade(active_portfolio, 'AAPL', 15000)

# Show trade history
print("\n=== Trade History ===")
print(active_portfolio.get_trade_history())