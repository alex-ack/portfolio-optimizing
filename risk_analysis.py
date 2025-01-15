import pandas as pd
import numpy as np
from portfolio_analyzer import PortfolioManager, analyze_stock

def check_portfolio_health(portfolio, name=""):
    """
    check if our portfolio is looking healthy
    """
    metrics = portfolio.get_performance_metrics()
    
    # basic health check
    print(f"\n🏥 health check for {name}")
    print(f"💰 total value: ${metrics['total_value']:.2f}")
    print(f"💵 cash: ${metrics['cash']:.2f}")
    
    if metrics['cash'] < 2500:
        print("⚠️ watch out! cash is below $2.5k minimum!")
    
    # check position sizes
    positions = metrics['positions']
    for _, pos in positions.iterrows():
        if pos['position_value'] > 20000:
            print(f"⚠️ heads up! {pos['symbol']} position (${pos['position_value']:.2f}) is over $20k limit")
            print(f"   might wanna sell {pos['quantity'] - int(20000/pos['current_price'])} shares")
    
    # concentration check
    total_value = metrics['total_value']
    for _, pos in positions.iterrows():
        concentration = (pos['position_value'] / total_value) * 100
        if concentration > 25:
            print(f"⚠️ watch out! {pos['symbol']} is {concentration:.1f}% of portfolio (maybe diversify?)")

def analyze_risk(portfolio, name=""):
    """
    quick risk check on our positions
    """
    metrics = portfolio.get_performance_metrics()
    positions = metrics['positions']
    
    print(f"\n🎲 risk analysis for {name}")
    
    risk_scores = []
    for _, pos in positions.iterrows():
        analysis = analyze_stock(pos['symbol'])
        if analysis and 'stats' in analysis:
            volatility = analysis['stats']['volatility']
            monthly_change = analysis['stats']['price_change_1m']
            
            risk_score = {
                'symbol': pos['symbol'],
                'position_size': f"${pos['position_value']:.2f}",
                'volatility': f"{volatility:.1f}%",
                'monthly_change': f"{monthly_change:.1f}%",
                'return': f"{pos['position_return']:.1f}%"
            }
            risk_scores.append(risk_score)
    
    return pd.DataFrame(risk_scores)

def track_trades(portfolio):
    """
    check how we're doing with required trades
    """
    trades = portfolio.get_trade_history()
    total_trades = len(trades)
    trades_needed = 54  # for 2 person group
    
    print("\n📊 trade tracking")
    print(f"trades made: {total_trades}")
    print(f"trades left: {trades_needed - total_trades}")
    
    if trades_needed > total_trades:
        weeks_left = 16  # or however many weeks left
        trades_per_week = (trades_needed - total_trades) / weeks_left
        print(f"need about {trades_per_week:.1f} trades per week to hit the target")

if __name__ == "__main__":
    # check portfolio A (active/trading)
    active = PortfolioManager()
    check_portfolio_health(active, "portfolio A (trading)")
    risks_a = analyze_risk(active, "portfolio A")
    if not risks_a.empty:
        print("\nrisk breakdown:")
        print(risks_a)
    track_trades(active)
    
    # check portfolio B (long-term)
    passive = PortfolioManager()
    check_portfolio_health(passive, "portfolio B (long-term)")
    risks_b = analyze_risk(passive, "portfolio B")
    if not risks_b.empty:
        print("\nrisk breakdown:")
        print(risks_b)