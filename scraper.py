import requests
from bs4 import BeautifulSoup
# import get_data

# ticker = 'JNJ'

def get_google_finance_news(ticker):
    # URL for the stock ticker on Google Finance
    url = f'https://www.google.com/finance/quote/{ticker}'
    
    # Send a request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
    
        headlines = []
        for item in soup.find_all('div'):  # Adjust the class name as needed  yY3Lee
            headline = item.get_text(strip=True)
            headlines.append(headline)
        
        return headlines
    else:
        return None


ticker = 'IIC'
news = get_google_finance_news(ticker)
if news:
    for idx, headline in enumerate(news):
        print(f'{idx + 1}. {headline}')
else:
    print("Failed to retrieve news.")
