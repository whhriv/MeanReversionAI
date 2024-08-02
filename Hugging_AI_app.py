
import os
import io
import base64
from flask import Flask, request, jsonify, render_template
import requests
import openai
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
NewsAPI_API_KEY = os.environ.get('NewsAPI_API_KEY')

openai.api_key = OPENAI_API_KEY

def get_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

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
                                    "Based on this data, and considering a mean reversion strategy, what would you advise for this stock? Should we buy, sell or hold? "}
    ]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",  
        messages=messages,
        max_tokens=150
    )
    if response.choices:
        return response.choices[0].message.content.strip()
    else:
        return "No advice available"

def get_stock_news(ticker):
    api_key = NewsAPI_API_KEY
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': ticker,  
        'apiKey': api_key,
        'language': 'en',
      'sortBy': 'publishedAt',  
        'pageSize': 5  
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        headlines = [article['title'] for article in articles]
        return headlines
    else:
        return []

def analyze_sentiment(headlines):
    messages = [
        {"role": "system", "content": "You are a sentiment analysis expert."},
        {"role": "user", "content": f"Analyze the sentiment of the following news headlines:\n{headlines}\n\n to generate a consensus and provide an estimated percentage of success, limit response to >5 bulletpoints"}
    ]
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=150
    )
    sentiment = response.choices[0].message.content.strip().replace('\n', '')
    return [{"sentiment": sentiment}]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/meanreversion', methods=['GET'])
def mean_reversion():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not ticker or not start_date or not end_date:
        return jsonify({'error': 'Missing parameters'}), 400
    try:
        data = get_stock_data(ticker, start_date, end_date)
        analyzed_data = calculate_mean_reversion(data)
        advice = get_investment_advice(analyzed_data, ticker)
        result = analyzed_data[['Close', 'Mean', 'Upper', 'Lower', 'Position']].tail().to_dict(orient='records')
        result.append({'Advice': advice})
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/plot')
def plot():
    plt.figure(figsize=(14, 7))
    plt.plot([1, 2, 3], [4, 5, 6], label='Test Plot')
    plt.title('Test Plot')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.legend()
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    img_url = f'data:image/png;base64,{img_base64}'
    return render_template('plot.html', img_url=img_url)

@app.route('/analyze', methods=['GET'])
def analyze_stock():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not ticker or not start_date or not end_date:
        return jsonify({'error': 'Missing parameters'}), 400
    try:
        data = get_stock_data(ticker, start_date, end_date)
        analyzed_data = calculate_mean_reversion(data)
        advice = get_investment_advice(analyzed_data, ticker)
        headlines = get_stock_news(ticker)
        sentiment_analysis = analyze_sentiment(headlines)
        plt.style.use('dark_background')
        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label='Close Price', color='blue')
        plt.plot(data['Mean'], label='Mean', color='orange')
        plt.plot(data['Upper'], label='Upper Bound', color='red')
        plt.plot(data['Lower'], label='Lower Bound', color='green')
        buy_signals = data[data['Position'] == 1]
        sell_signals = data[data['Position'] == -1]
        plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
        plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)
        plt.title(f'Mean Reversion Strategy for {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
        img_url = f'data:image/png;base64,{img_base64}'
        plt.close()
        latest_data = analyzed_data.iloc[-1]
        result_df = pd.DataFrame({
            'Metric': ['Current Price', 'Mean', 'Upper Bound', 'Lower Bound', 'Position', 'Advice'],
            'Value': [latest_data['Close'], latest_data['Mean'], latest_data['Upper'], latest_data['Lower'], latest_data['Position'], advice]
        })
        result_json = result_df.to_dict(orient='records')
        return render_template('index.html', result=result_json, sentiment=sentiment_analysis, advice=advice, img_url=img_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)