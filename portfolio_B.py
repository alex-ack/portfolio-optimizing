from portfolio_analyzer import PortfolioManager, analyze_stock
import pandas as pd

def plan_long_term_portfolio():
    # Create suggested allocations
    portfolio_plan = {
        'Index Funds (40%)': [
            ('VOO', 'S&P 500 ETF', 0.25),  # 25% to S&P 500
            ('QQQ', 'Nasdaq 100 ETF', 0.15)  # 15% to tech-heavy Nasdaq
        ],
        'Blue Chips (35%)': [
            ('BRK-B', 'Berkshire Hathaway', 0.15),  # 15% to Berkshire
            ('PG', 'Procter & Gamble', 0.10),  # 10% to P&G
            ('KO', 'Coca-Cola', 0.10)  # 10% to Coca-Cola
        ],
        'Dividend Stocks (25%)': [
            ('PEP', 'PepsiCo', 0.10),  # 10% to PepsiCo
            ('ABT', 'Abbott Labs', 0.15)  # 15% to Abbott
        ]
    }
    
    print("=== Long-term Portfolio Analysis ===")
    results = []
    
    total_cash = 100000
    for category, stocks in portfolio_plan.items():
        print(f"\n{category}")
        for symbol, name, allocation in stocks:
            target_amount = total_cash * allocation
            analysis = analyze_stock(symbol)
            
            if analysis and 'stats' in analysis:
                price = analysis['stats']['current_price']
                shares = int(min(target_amount, 20000) / price)
                actual_amount = shares * price
                
                results.append({
                    'Symbol': symbol,
                    'Name': name,
                    'Target %': f"{allocation*100:.1f}%",
                    'Shares': shares,
                    'Price': f"${price:.2f}",
                    'Investment': f"${actual_amount:.2f}",
                    'Monthly Change': f"{analysis['stats']['price_change_1m']:.1f}%"
                })
    
    return pd.DataFrame(results)

# Generate and display the portfolio plan
portfolio_plan = plan_long_term_portfolio()
print("\nDetailed Portfolio Allocation:")
print(portfolio_plan.to_string(index=False))