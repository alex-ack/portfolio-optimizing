from portfolio_analyzer import analyze_stock
import pandas as pd
import numpy as np

def analyze_tech_stocks():
    # Stocks to analyze
    tech_stocks = ['AMD', 'MRVL', 'PLTR']
    
    # Store analysis results
    results = []
    
    print("Analyzing tech stocks...\n")
    
    for symbol in tech_stocks:
        print(f"Getting data for {symbol}...")
        analysis = analyze_stock(symbol)
        
        if analysis and 'stats' in analysis:
            stats = analysis['stats']
            price = stats['current_price']
            max_shares = int(20000 / price)  # Max shares within project limits
            
            results.append({
                'Symbol': symbol,
                'Current Price': f"${price:.2f}",
                'Monthly Change': f"{stats['price_change_1m']:.1f}%",
                'Volatility': f"{stats['volatility']:.1f}%" if stats['volatility'] else "N/A",
                'Max Position': f"${(max_shares * price):.2f}",
                'Shares @ $20k': max_shares,
                'Volume': format(int(stats['avg_volume']), ',')
            })
    
    if results:
        # Convert to DataFrame and sort by monthly change
        df = pd.DataFrame(results).set_index('Symbol')
        print("\n=== Tech Stock Analysis ===")
        print(df.to_string())
        
        # Print some trading insights
        print("\n=== Trading Insights ===")
        for stock in results:
            symbol = stock['Symbol']
            max_pos = stock['Max Position']
            shares = stock['Shares @ $20k']
            print(f"\n{symbol}:")
            print(f"- Could buy {shares} shares (about {max_pos})")
            print(f"- Volume: {stock['Volume']} (daily avg)")
            print(f"- Monthly Move: {stock['Monthly Change']}")

if __name__ == "__main__":
    analyze_tech_stocks()