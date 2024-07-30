from openai import OpenAI

client = OpenAI(api_key='')
import pandas as pd
import yahoo_finance as yf
import numpy as np
# from openai import ChatCompletion

# Initialize OpenAI client

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Example usage
ticker = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'
data = get_stock_data(ticker, start_date, end_date)

def calculate_mean_reversion(data):
    data['Mean'] = data['Close'].rolling(window=20).mean()
    data['StdDev'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['Mean'] + (data['StdDev'] * 2)
    data['Lower'] = data['Mean'] - (data['StdDev'] * 2)

    data['Position'] = np.where(data['Close'] > data['Upper'], -1, np.nan)
    data['Position'] = np.where(data['Close'] < data['Lower'], 1, data['Position'])
    data['Position'] = data['Position'].ffill().fillna(0)

    return data

data = calculate_mean_reversion(data)

# def get_investment_advice(data, ticker):
#     latest_data = data.iloc[-1]
#     prompt = f"Analyze the following stock data for {ticker} and suggest whether to buy or sell:\n" \
#              f"Current Price: {latest_data['Close']}\n" \
#              f"Mean: {latest_data['Mean']}\n" \
#              f"Upper Bound: {latest_data['Upper']}\n" \
#              f"Lower Bound: {latest_data['Lower']}\n" \
#              f"Position: {latest_data['Position']}\n" \
#              "Based on mean reversion strategy, should we buy or sell this stock?"

#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",  
#         prompt=prompt,
#         max_tokens=150
#     )

#     return response.choices[0].text.strip()



def get_investment_advice(data, ticker):
    latest_data = data.iloc[-1]
    prompt = f"Analyze the following stock data for {ticker} and suggest whether to buy or sell:\n" \
             f"Current Price: {latest_data['Close']}\n" \
             f"Mean: {latest_data['Mean']}\n" \
             f"Upper Bound: {latest_data['Upper']}\n" \
             f"Lower Bound: {latest_data['Lower']}\n" \
             f"Position: {latest_data['Position']}\n" \
             "Based on mean reversion strategy, should we buy or sell this stock?"

    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Ensure you use the correct model name
    messages=[
        {"role": "system", "content": "You are a financial advisor."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=150)

    return response.choices[0].message.content.strip()




# Example usage
advice = get_investment_advice(data, ticker)
print(advice)

def ai_investing_workflow(ticker, start_date, end_date):
    data = get_stock_data(ticker, start_date, end_date)
    analyzed_data = calculate_mean_reversion(data)
    advice = get_investment_advice(analyzed_data, ticker)
    return advice

# Example usage
result = ai_investing_workflow(ticker='AAPL', start_date='2020-01-01', end_date='2023-01-01')
print(result)
