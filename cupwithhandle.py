import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 過去1年間の日付を設定

days=int(input('何日さかのぼる?'))
drop=int(input('下落率は？'))
jump=int(input('上昇率は?'))

        

end_date = datetime.now()
#start_date = end_date - timedelta(days=365)
start_date = end_date - timedelta(days)
#さかのぼる日付を指定する

# S&P 500株のリストを取得（Wikipediaから）
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(sp500_url)
sp500_tickers = sp500_table[0]['Symbol'].tolist()

# 株価の分析を行う関数
def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(start=start_date, end=end_date)

        if stock_data.empty:
            return None

        high_price = stock_data['High'].max()
        low_price = stock_data['Low'].min()
        current_price = stock_data['Close'].iloc[-1]

        # 最高値から最低値への下落率
        drop_percentage = ((high_price - low_price) / high_price) * 100

        # 最低値から現在価格までの回復率
        recovery_percentage = ((current_price - low_price) / low_price) * 100
#どれだけ上げて下げたかを指定する

        if drop_percentage >= drop and recovery_percentage >= jump:
       
            return ticker
        else:
            return None
    except Exception as e:
        return None

# 条件に合致する株を探す
matching_stocks = []
for ticker in sp500_tickers:
    result = analyze_stock(ticker)
    if result is not None:
        matching_stocks.append(result)

print(matching_stocks)
