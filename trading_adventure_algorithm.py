import yfinance as yf
import pandas as pd

class trade():
    def __init__(self, symbol, from_date, to_date):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.data = None
        
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

# ===== Usage =====
trd = trade("AAPL", "2018-01-01", "2023-12-31")
trd.get_data()
trd.moving_average()
print(trd.data[['Close','avg_50','avg_200']].tail())
