import os
from alpaca_trade_api import REST
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Alpaca API credentials
BASE_URL = "https://paper-api.alpaca.markets/"


ALPACA_API_KEY  = os.environ.get('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')

# Instantiate REST API Connection
api = REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, 
           base_url=BASE_URL, api_version='v2')

# Fetch Account
account = api.get_account()
# Print Account Details
print(account.id, account.equity, account.status)
def calculate_mean_reversion(data):
    # Make sure column names match those in bars_df
    data['Mean'] = data['close'].rolling(window=3).mean()
    data['StdDev'] = data['close'].rolling(window=3).std()
    data['Upper'] = data['Mean'] + (data['StdDev'] * 2)
    data['Lower'] = data['Mean'] - (data['StdDev'] * 2)

    data['Position'] = np.where(data['close'] > data['Upper'], -1, np.nan)
    data['Position'] = np.where(data['close'] < data['Lower'], 1, data['Position'])
    data['Position'] = data['Position'].ffill().fillna(0)

    print(data)
    return data

# Fetch AMD data from the last 100 days using a valid timeframe
try:
    barset = api.get_bars(
        'AMD', 
        timeframe='50Min',  
        limit=100
    )
    
 
    bars_df = barset.df
    data = bars_df
    mean_r = calculate_mean_reversion(data)
    print(mean_r)
    data.to_csv('AMD_mean_reversion_data.csv', index=True)

    
    # Preview Data
    print(bars_df.head())

    # Optional: Plot the data
    plt.style.use('dark_background')

    plt.figure(figsize=(12, 6))
    plt.plot(bars_df.index, bars_df['close'], label='Close Price')
    plt.title('AMD 15-Minute Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")

# Call the function with the DataFrame
# data_mr = calculate_mean_reversion(data)





# from alpaca.trading.client import TradingClient
# import alpaca_trade_api as tradeapi


# trading_client = TradingClient('PK1N3MB68S3ALQMIUCV8', 'Gc6GPDNhaAJ5YYbxQayetshmyDGtFcf9jgo32iTr')

# # Get our position in AAPL.
# OII_position = trading_client.get_open_position('OII')

# # Get a list of all of our positions.
# portfolio = trading_client.get_all_positions()

# # Print the quantity of shares for each position.
# for position in portfolio:
#     print("{} shares of {}".format(position.qty, position.symbol))


# import alpaca_trade_api as tradeapi
# # from alpaca_trade_api import 
# import matplotlib.pyplot as plt

# # # API Info for fetching data, portfolio, etc. from Alpaca
# BASE_URL = "https://paper-api.alpaca.markets/"
# ALPACA_API_KEY = "PK1N3MB68S3ALQMIUCV8"
# ALPACA_SECRET_KEY = "Gc6GPDNhaAJ5YYbxQayetshmyDGtFcf9jgo32iTr"

# # # Instantiate REST API Connection
# api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, 
#                     base_url=BASE_URL, api_version='v2')

# # # Fetch Account
# account = api.get_account()
# #Print Account Details
# print(account.id, account.equity, account.status)

# # # # Fetch Apple data from last 100 days
# AMD_data = api.get_bars('AMD', 'Day', limit=100)
# # # # Preview Data
# print(AMD_data.df.head())


# from alpaca_trade_api import REST, TimeFrame
# import matplotlib.pyplot as plt

# # Alpaca API credentials
# BASE_URL = "https://paper-api.alpaca.markets/"
# ALPACA_API_KEY = "PK1N3MB68S3ALQMIUCV8"
# ALPACA_SECRET_KEY = "Gc6GPDNhaAJ5YYbxQayetshmyDGtFcf9jgo32iTr"

# # Instantiate REST API Connection
# api = REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, 
#            base_url=BASE_URL, api_version='v2')

# # Fetch Account
# account = api.get_account()
# # Print Account Details
# print(account.id, account.equity, account.status)

# # Fetch AMD data from last 100 days using correct TimeFrame
# try:
#     barset = api.get_bars(
#         'AMD', 
#         TimeFrame.Day, 
#         limit=100
#     )
    
#     # Convert to DataFrame for easier manipulation
#     bars_df = barset.df
    
#     # Preview Data
#     print(bars_df.head())

#     # Optional: Plot the data
#     plt.figure(figsize=(12, 6))
#     plt.plot(bars_df.index, bars_df['close'], label='Close Price')
#     plt.title('AMD Daily Closing Prices')
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# except Exception as e:
#     print(f"An error occurred: {e}")



# # # Fetch Apple data from last 100 days
# AMD_data = api.get_bars('AAPL', 'day', limit=100).df

# # Reformat data (drop multiindex, rename columns, reset index)
# AMD_data.columns = AMD_data.columns.to_flat_index()
# AMD_data.columns = [x[1] for x in AMD_data.columns]
# AMD_data.reset_index(inplace=True)
# print(AMD_data.head())

# # Plot stock price data
# plt.style.use('dark_background')

# plot = AMD_data.plot(x="time", y="close", legend=False)
# plot.set_xlabel("Date")
# plot.set_ylabel("Apple Close Price ($)")
# plt.show()


# api.submit_order(symbol='AAPL', qty=1, side='buy', type='market', time_in_force='day')

# #short order for tsla
# api.submit_order('TSLA', 1, 'sell', 'market', 'day')

# # Get stock position for Apple

# aapl_position = api.get_position('AAPL')

# print(aapl_position)

# # Get a list of all of our positions.
# portfolio = api.list_positions()

# # Print the quantity of shares for each position.
# for position in portfolio:
#     print("{} shares of {}".format(position.qty, position.symbol))