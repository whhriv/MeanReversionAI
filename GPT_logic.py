from openai import OpenAI

client = OpenAI(api_key='your_openai_api_key')


def get_investment_advice(data, ticker):
    latest_data = data.iloc[-1]
    prompt = f"Analyze the following stock data for {ticker} and suggest whether to buy or sell:\n" \
             f"Current Price: {latest_data['Close']}\n" \
             f"Mean: {latest_data['Mean']}\n" \
             f"Upper Bound: {latest_data['Upper']}\n" \
             f"Lower Bound: {latest_data['Lower']}\n" \
             f"Position: {latest_data['Position']}\n" \
             "Based on mean reversion strategy, should we buy or sell this stock?"

    response = client.completions.create(engine="text-davinci-003",
    prompt=prompt,
    max_tokens=150)

    return response.choices[0].text.strip()

# Example usage
advice = get_investment_advice(data, ticker)
print(advice)
