import os
import openai
import requests
import yfinance as yf
import numpy as np
import pandas as pd


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def calculate_mean_reversion(data):
    data['Mean'] = data['Close'].rolling(window=20).mean()
    data['StdDev'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['Mean'] + (data['StdDev'] * 2)
    data['Lower'] = data['Mean'] - (data['StdDev'] * 2)

    data['Position'] = np.where(data['Close'] > data['Upper'], -1, np.nan)
    data['Position'] = np.where(data['Close'] < data['Lower'], 1, data['Position'])
    data['Position'] = data['Position'].ffill().fillna(0)

    return data

def get_investment_advice(data, ticker):
    latest_data = data.iloc[-1]
    messages = [
        {"role": "system", "content": "You are an investment advisor."},
        {"role": "user", "content": f"Here is the latest data snapshot for {ticker}:\n"
                                    f"Current Price: {latest_data['Close']}\n"
                                    f"Mean: {latest_data['Mean']}\n"
                                    f"Upper Bound: {latest_data['Upper']}\n"
                                    f"Lower Bound: {latest_data['Lower']}\n"
                                    f"Position: {latest_data['Position']}\n\n"
                                    "Based on this data, and considering a mean reversion strategy, what would you advise for this stock? Should we buy or sell?"}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",  # Replace with the correct model name if different
        messages=messages,
        max_tokens=150
    )
    #WRAP RESPONSE IN DIR EX: res = dir(response)
    resdir = dir(response)
    # print(resdir)
    return response
import requests

def get_stock_news(ticker):
    api_key = '603b27d13ee5411aa732c00ada877a3d'  # Replace with your NewsAPI key
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': ticker,  # The stock ticker symbol or company name
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt',  # Sort by latest news
        'pageSize': 5  # Limit to 5 news articles
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        # Extract headline and description for sentiment analysis
        headlines = [
            article['title'] for article in articles
        ]
        
        return headlines
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

def analyze_sentiment(headlines):
    sentiment_messages = []
    
    for headline in headlines:
        messages = [
            {"role": "system", "content": "You are a sentiment analysis expert."},
            {"role": "user", "content": f"Analyze the sentiment of the following news headline:\n{headline}"}
        ]
        
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=60
        )
        
        sentiment = response.choices[0].message['content'].strip()
        sentiment_messages.append({
            'headline': headline,
            'sentiment': sentiment
        })
    
    return sentiment_messages



def ai_investing_workflow(ticker, start_date, end_date):
    data = get_stock_data(ticker, start_date, end_date)
    analyzed_data = calculate_mean_reversion(data)
    advice = get_investment_advice(analyzed_data, ticker)
    print(advice.choices[0].message.content)
    # print(advice['content'])
    latest_data = analyzed_data.iloc[-1]
    # pd.set_option('display.max_colwidth', None)
    result_df = pd.DataFrame({
        'Metric': ['Current Price', 'Mean', 'Upper Bound', 'Lower Bound', 'Position', 'Advice'],
        'Value': [latest_data['Close'], latest_data['Mean'], latest_data['Upper'], latest_data['Lower'], latest_data['Position'], advice.choices[0].message.content]
    })
    with open('advice.txt', 'w') as file:
        file.write(advice.choices[0].message.content)
    return result_df

result_df = ai_investing_workflow(ticker='JNJ', start_date='2024-01-01', end_date='2024-07-24')
# print(result_df.to_string(index=False))
print(result_df)
