import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import time

def safe_get_stock_data(symbol, retries=3, delay=1):
    """Safely get stock data with retries"""
    for attempt in range(retries):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='3mo')
            if not hist.empty:
                return ticker, hist
        except Exception as e:
            if attempt < retries - 1:  # don't sleep on the last attempt
                time.sleep(delay)
    return None, pd.DataFrame()

class PortfolioManager:
    def __init__(self, initial_cash=100000, max_stock_value=20000, min_cash=2500):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.max_stock_value = max_stock_value
        self.min_cash = min_cash
        self.holdings = {}  # symbol: {quantity: int, avg_price: float}
        self.trades = []
        self.broker_fee = 10
        
    def can_buy(self, symbol, quantity, current_price):
        total_cost = (quantity * current_price) + self.broker_fee
        if total_cost > self.cash:
            return False, "Insufficient funds"
        if (quantity * current_price) > self.max_stock_value:
            return False, f"Exceeds max stock value of ${self.max_stock_value}"
        if (self.cash - total_cost) < self.min_cash:
            return False, f"Would leave less than minimum cash (${self.min_cash})"
        return True, ""
        
    def buy(self, symbol, quantity, price, date=None):
        if date is None:
            date = datetime.now()
            
        can_buy_status, message = self.can_buy(symbol, quantity, price)
        if not can_buy_status:
            raise ValueError(f"Cannot execute buy: {message}")
            
        total_cost = (quantity * price) + self.broker_fee
        self.cash -= total_cost
        
        if symbol in self.holdings:
            current_quantity = self.holdings[symbol]['quantity']
            current_avg_price = self.holdings[symbol]['avg_price']
            new_quantity = current_quantity + quantity
            new_avg_price = ((current_quantity * current_avg_price) + (quantity * price)) / new_quantity
            self.holdings[symbol] = {'quantity': new_quantity, 'avg_price': new_avg_price}
        else:
            self.holdings[symbol] = {'quantity': quantity, 'avg_price': price}
            
        self.trades.append({
            'date': date,
            'symbol': symbol,
            'action': 'BUY',
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'cash_remaining': self.cash
        })
        
    def sell(self, symbol, quantity, price, date=None):
        if date is None:
            date = datetime.now()
            
        if symbol not in self.holdings:
            raise ValueError(f"No holdings for {symbol}")
        if quantity > self.holdings[symbol]['quantity']:
            raise ValueError(f"Insufficient shares of {symbol}")
            
        proceeds = (quantity * price) - self.broker_fee
        self.cash += proceeds
        
        remaining_quantity = self.holdings[symbol]['quantity'] - quantity
        if remaining_quantity == 0:
            del self.holdings[symbol]
        else:
            self.holdings[symbol]['quantity'] = remaining_quantity
            
        self.trades.append({
            'date': date,
            'symbol': symbol,
            'action': 'SELL',
            'quantity': quantity,
            'price': price,
            'total': proceeds,
            'cash_remaining': self.cash
        })
        
    def get_portfolio_value(self, current_prices=None):
        if current_prices is None:
            current_prices = {}
            for symbol in self.holdings:
                ticker, hist = safe_get_stock_data(symbol)
                if not hist.empty:
                    current_prices[symbol] = hist['Close'].iloc[-1]
                else:
                    current_prices[symbol] = self.holdings[symbol]['avg_price']
                
        portfolio_value = self.cash
        for symbol, holding in self.holdings.items():
            if symbol in current_prices:
                portfolio_value += holding['quantity'] * current_prices[symbol]
        return portfolio_value
        
    def get_trade_history(self):
        return pd.DataFrame(self.trades)
        
    def get_performance_metrics(self, current_prices=None):
        if current_prices is None:
            current_prices = {}
            for symbol in self.holdings:
                ticker, hist = safe_get_stock_data(symbol)
                if not hist.empty:
                    current_prices[symbol] = hist['Close'].iloc[-1]
                else:
                    current_prices[symbol] = self.holdings[symbol]['avg_price']
                
        metrics = {
            'total_value': self.get_portfolio_value(current_prices),
            'cash': self.cash,
            'num_positions': len(self.holdings),
            'total_trades': len(self.trades),
            'returns': (self.get_portfolio_value(current_prices) - self.initial_cash) / self.initial_cash * 100
        }
        
        position_metrics = []
        for symbol, holding in self.holdings.items():
            current_price = current_prices.get(symbol, 0)
            position_value = holding['quantity'] * current_price
            position_return = (current_price - holding['avg_price']) / holding['avg_price'] * 100
            
            position_metrics.append({
                'symbol': symbol,
                'quantity': holding['quantity'],
                'avg_price': holding['avg_price'],
                'current_price': current_price,
                'position_value': position_value,
                'position_return': position_return
            })
            
        metrics['positions'] = pd.DataFrame(position_metrics)
        return metrics

def analyze_stock(symbol, start_date=None, end_date=None):
    if start_date is None:
        start_date = datetime.now() - timedelta(days=365)
    if end_date is None:
        end_date = datetime.now()
        
    ticker, hist = safe_get_stock_data(symbol)
    
    if hist.empty:
        print(f"Warning: Could not get data for {symbol}")
        return None
    
    # Calculate technical indicators using proper indexing
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['Daily_Return'] = hist['Close'].pct_change()
    hist['Volatility'] = hist['Daily_Return'].rolling(window=20).std() * np.sqrt(252)
    
    # Get the latest values using iloc
    latest_close = hist['Close'].iloc[-1]
    
    # Calculate price changes
    price_1m_ago = hist['Close'].iloc[-20] if len(hist) >= 20 else hist['Close'].iloc[0]
    price_3m_ago = hist['Close'].iloc[-60] if len(hist) >= 60 else hist['Close'].iloc[0]
    
    # Basic statistics
    stats = {
        'current_price': latest_close,
        'price_change_1m': (latest_close / price_1m_ago - 1) * 100,
        'price_change_3m': (latest_close / price_3m_ago - 1) * 100,
        'volatility': hist['Volatility'].iloc[-1] if not hist['Volatility'].empty else None,
        'avg_volume': hist['Volume'].mean()
    }
    
    try:
        stats['market_cap'] = ticker.info.get('marketCap', None)
    except:
        stats['market_cap'] = None
    
    return {
        'history': hist,
        'stats': stats,
        'info': ticker.info if ticker else {}
    }

if __name__ == "__main__":
    # Create portfolio manager instances for both portfolios
    active_portfolio = PortfolioManager()
    passive_portfolio = PortfolioManager()
    
    # Example analysis of a stock
    print("Analyzing AAPL...")
    analysis = analyze_stock('AAPL')
    if analysis:
        print(f"Apple Stats:\n{pd.Series(analysis['stats'])}")
        
        # Example trade
        shares_to_buy = 10
        price = analysis['stats']['current_price']
        active_portfolio.buy('AAPL', shares_to_buy, price)
        print(f"\nPortfolio after buying AAPL:\n{active_portfolio.get_performance_metrics()}")
    else:
        print("Could not analyze AAPL")