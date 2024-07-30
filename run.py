from langchain import chains

def ai_investing_workflow(ticker, start_date, end_date):
    data = get_stock_data(ticker, start_date, end_date)
    analyzed_data = calculate_mean_reversion(data)
    advice = get_investment_advice(analyzed_data, ticker)
    return advice

# Example usage
chain = chains([ai_investing_workflow])
result = chain.run(ticker='AAPL', start_date='2020-01-01', end_date='2023-01-01')
print(result)
