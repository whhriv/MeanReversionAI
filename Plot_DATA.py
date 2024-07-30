import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import csv

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Example Stock Data & Relevant Dates for input
ticker = 'AMD'
start_date = '2024-06-02'
end_date = '2024-07-26'
data = get_stock_data(ticker, start_date, end_date)
print(data)
data.to_csv('JNJ_stock_data.csv')

# Calculate mean reversion in the asset prices
def calculate_mean_reversion(data):
    print(data['Close'].rolling(window=20).mean())
    data['Mean'] = data['Close'].rolling(window=10).mean()
    data['StdDev'] = data['Close'].rolling(window=10).std()
    data['Upper'] = data['Mean'] + (data['StdDev'] * 2)
    data['Lower'] = data['Mean'] - (data['StdDev'] * 2)
    
    data['Position'] = np.where(data['Close'] > data['Upper'], -1, np.nan)
    data['Position'] = np.where(data['Close'] < data['Lower'], 1, data['Position'])
    data['Position'] = data['Position'].ffill().fillna(0)
    

    return data


data = calculate_mean_reversion(data)
print(data)


# ChatGPT API Key 


# Plot the data using Matplotlib
plt.style.use('dark_background')
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', color='blue')
plt.plot(data['Mean'], label='Mean', color='orange')
plt.plot(data['Upper'], label='Upper Bound', color='red')
plt.plot(data['Lower'], label='Lower Bound', color='green')

# Highlight buying and selling positions
buy_signals = data[data['Position'] == 1]
sell_signals = data[data['Position'] == -1]

plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)

plt.title(f'Mean Reversion Strategy for {ticker}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()