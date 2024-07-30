import numpy as np

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
