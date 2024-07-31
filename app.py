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


# OpenAI API Key
openai.api_key = OPENAI_API_KEY 

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
                                    "Based on this data, and considering a mean reversion strategy, what would you advise for this stock? Should we buy, sell or hold? "}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",  
        messages=messages,
        max_tokens=150
    )
    if response.choices:
        advice_content = response.choices[0].message.content
        # advice.choices[0].message.content
        print(advice_content)
        return advice_content
    else:
        print("No choices available in the response.")
        return "No advice available"

#TEST STOCK NEWS
def get_stock_news(ticker):
    api_key = NewsAPI_API_KEY
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
#TEST ANALYZE SENTIMENT
def analyze_sentiment(headlines):
    sentiment_messages = []
    #DOING INDIVIDUAL HEADLINES FOR SENTIMENT
    # for headline in headlines:
    messages = [
        {"role": "system", "content": "You are a sentiment analysis expert."},
        {"role": "user", "content": f"Analyze the sentiment of the following news headlines:\n{headlines}\n\n to generate a consensus and provide an estimated percentage of success, limit response to >5 bulletpoints"}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=150
    )
    
    sentiment_init = response.choices[0].message.content.strip()
    sentiment = sentiment_init.replace('\n', '<br>')

    sentiment_json = jsonify(sentiment)
    print(sentiment_json)
    # sentiment = response.choices[0].message.content.sentiment.
    sentiment_messages.append({
        # 'headline': headlines,
        'sentiment': sentiment.strip(),
        
    })
    #end forloop
    print('SENTIMENT MESSAGES: ', sentiment_messages)
    return sentiment_messages


    # FLASK ROUTING
#HOME
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# [testing] ONLY MEAN REVISION DATA ENDPOINT FOR GRAPHING FE [testing]
@app.route('/meanRevision', methods=['GET'])
def mean_revision():
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not ticker or not start_date or not end_date:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        data = get_stock_data(ticker, start_date, end_date)
        analyzed_data = calculate_mean_reversion(data)
        
        # Convert the relevant columns to a dictionary format
        result = analyzed_data[['Close', 'Mean', 'Upper', 'Lower', 'Position']].tail().to_dict(orient='records')
        print("Returning JSON response:", result)

        return jsonify(result)

    except Exception as e:
        print("Error:", str(e))

        return jsonify({'error': str(e)}), 500
# [testing] ONLY MEAN REVISION DATA ENDPOINT FOR GRAPHING FE [testing]


#[testing] plot route - plot data hardcoded. 
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

    # Render template with image URL
    return render_template('plot.html', img_url=img_url)

# ROUTE TO ANALYZE STOCK - USED IN /TEMPLATES/INDEX.HTML 
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
        # advice_json = jsonify(advice)
                # Fetch news headlines and perform sentiment analysis
        headlines = get_stock_news(ticker)  
        sentiment_analysis = analyze_sentiment(headlines)  

# [testing] PLOTTING TEST FOR OUTPUT [testing]

         # Generate plot
        # plt.use("macOSX")
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

        # Save plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
        img_url = f'data:image/png;base64,{img_base64}'
        # print(img_url)

        plt.close()

# [testing] PLOTTING TEST FOR OUTPUT [testing]

        
        latest_data = analyzed_data.iloc[-1]
        result_df = pd.DataFrame({
            'Metric': ['Current Price', 'Mean', 'Upper Bound', 'Lower Bound', 'Position', 'Advice'],
            'Value': [latest_data['Close'], latest_data['Mean'], latest_data['Upper'], latest_data['Lower'], latest_data['Position'], advice]
        })
        
        # Convert DataFrame to JSON serializable format
        result_json = result_df.to_dict(orient='records')

        # return result_json CORRECT-UNCOMMENT IF BELOW IS WRONG
        # return render_template('index.html', result=result_json, sentiment=sentiment_analysis, img_url=img_url) 
        return render_template('index.html', result=result_json, sentiment=sentiment_analysis, advice=advice, img_url=img_url)

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



if __name__ == '__main__':
    app.run(debug=True)


