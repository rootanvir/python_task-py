import yfinance as yf
import pandas as pd

class trade():
    def __init__(self, symbol, from_date, to_date):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.data =None
    def get_data(self):
        data = yf.download(self.symbol ,start=self.from_date,end=self.to_date)
        data.to_csv("historical_market_data.csv")




