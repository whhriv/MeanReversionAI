import requests

# Define the API endpoint
url = 'http://localhost:5000/analyze'

# Define the parameters
params = {
    'ticker': 'OII',
    'start_date': '2022-06-02',
    'end_date': '2024-07-23'
}

# Make the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
