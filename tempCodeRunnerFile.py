import yfinance as yf
import pandas as pd

class trade():
    def __init__(self, symbol, from_date, to_date):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.data = None
        self.cash = 5000
        self.position = 0
        self.buy_price = 0
        self.total_profit = 0
        
    def get_data(self):
        self.data = yf.download(self.symbol, start=self.from_date, end=self.to_date)
        self.clean_data()
        self.data.to_csv("historical_market_data.csv")
        print(f"Data saved to csv [cleaned]")
        
    def clean_data(self):
        if self.data is not None:
            self.data = self.data.drop_duplicates()
            self.data = self.data.ffill()
        else:
            print("Nothing to clean")
            
    def moving_average(self):
        if self.data is not None:
            self.data['avg_50'] = self.data['Close'].rolling(window=50).mean()
            self.data['avg_200'] = self.data['Close'].rolling(window=200).mean()
        else:
            print("No data to calculate averages")
    
    def investment_strategy(self):
        if self.data is not None:
            latest_price = float(self.data['Close'].iloc[-1])  # ✅ convert to float
            budget = 5000
            max_shares = int(budget // latest_price)
            print(f"With a ${budget} budget, you can buy {max_shares} shares of {self.symbol} at ${latest_price:.2f} each.")
        else:
            print("No data available to calculate investment strategy.")

    
    def trade_signals(self):
        if self.data is None:
            print("No data to trade on")
            return
        
        for i in range(1, len(self.data)):
            prev_short = float(self.data['avg_50'].iloc[i-1])
            prev_long = float(self.data['avg_200'].iloc[i-1])
            short = float(self.data['avg_50'].iloc[i])
            long = float(self.data['avg_200'].iloc[i])
            price = float(self.data['Close'].iloc[i])  # ✅ ensures it's a scalar float
            
            # Golden Cross → Buy
            if prev_short < prev_long and short > long and self.position == 0:
                self.position = int(self.cash // price)
                self.cash -= self.position * price
                self.buy_price = price
                print(f"BUY {self.position} shares at ${price:.2f} on {self.data.index[i].date()}")
            
            # Death Cross → Sell
            elif prev_short > prev_long and short < long and self.position > 0:
                self.cash += self.position * price
                profit = (price - self.buy_price) * self.position
                self.total_profit += profit
                print(f"SELL {self.position} shares at ${price:.2f} on {self.data.index[i].date()} | Profit: ${profit:.2f}")
                self.position = 0
        
        # Final forced sell if still holding
        if self.position > 0:
            price = float(self.data['Close'].iloc[-1])
            self.cash += self.position * price
            profit = (price - self.buy_price) * self.position
            self.total_profit += profit
            print(f"FORCED SELL {self.position} shares at ${price:.2f} on last day | Profit: ${profit:.2f}")
            self.position = 0
        
        print(f"\nFinal Portfolio Value: ${self.cash:.2f}")
        print(f"Total Profit: ${self.total_profit:.2f}")

# ===== Usage =====
trd = trade("AAPL", "2018-01-01", "2023-12-31")
trd.get_data()
trd.moving_average()
trd.investment_strategy()                           
trd.trade_signals()         

