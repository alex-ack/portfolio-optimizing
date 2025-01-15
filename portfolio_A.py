from portfolio_analyzer import PortfolioManager, analyze_stock
import pandas as pd

def analyze_sector(sector_name, symbols):
    print(f"\n=== {sector_name} Analysis ===")
    data = []
    
    for symbol in symbols:
        print(f"Analyzing {symbol}...")
        analysis = analyze_stock(symbol)
        
        if analysis and 'stats' in analysis:
            stats = analysis['stats']
            price = stats['current_price']
            max_shares = int(20000 / price)
            data.append({
                'Symbol': symbol,
                'Price': f"${price:.2f}",
                'Monthly Change': f"{stats['price_change_1m']:.1f}%",
                'Volatility': f"{stats['volatility']:.1f}%" if stats['volatility'] else "N/A",
                'Max Position': f"${(max_shares * price):.2f}",
                'Shares @ $20k': max_shares
            })
    
    if data:
        return pd.DataFrame(data).set_index('Symbol')
    return pd.DataFrame()

# Initialize Portfolio A
active_portfolio = PortfolioManager()

# Analyze different sectors
tech_stocks = ['AAPL', 'AMD', 'NVDA']  # Tech with semiconductor exposure
ai_stocks = ['MSFT', 'GOOGL', 'META']  # AI players
energy_stocks = ['XOM', 'CVX', 'FSLR']  # Mix of traditional and renewable
healthcare = ['JNJ', 'ISRG', 'LLY']    # Mix of stable and growth

# Run analysis
print("Analyzing potential stocks for Portfolio A (Active/Speculative)")
sectors = {
    'Technology & Semiconductor': tech_stocks,
    'AI & Digital': ai_stocks,
    'Energy': energy_stocks,
    'Healthcare': healthcare
}

for sector_name, symbols in sectors.items():
    analysis = analyze_sector(sector_name, symbols)
    if not analysis.empty:
        print("\n" + analysis.to_string())