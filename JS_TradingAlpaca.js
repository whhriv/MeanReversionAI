const axios = require('axios');
const Papa = require('papaparse');
const fs = require('fs');

// Alpaca API credentials
const BASE_URL = "https://paper-api.alpaca.markets/v2";
const ALPACA_API_KEY = "";
const ALPACA_SECRET_KEY = ""

// Function to fetch account information
async function getAccount() {
  try {
    const response = await axios.get(`${BASE_URL}/account`, {
      headers: {
        'APCA_API_KEY_ID': ALPACA_API_KEY,
        'APCA_API_SECRET_KEY': ALPACA_SECRET_KEY
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error("Error fetching account information:", error);
  }
}

// Function to fetch bar data
async function getBarData(symbol, timeframe, limit) {
  try {
    const response = await axios.get(`${BASE_URL}/bars/${timeframe}`, {
      headers: {
        'APCA_API_KEY_ID': ALPACA_API_KEY,
        'APCA_API_SECRET_KEY': ALPACA_SECRET_KEY
      },
      params: {
        symbols: symbol,
        limit: limit
      }
    });
    
    const bars = response.data.bars[symbol];
    // Convert to CSV format
    const csv = Papa.unparse(bars);

    // Save CSV to file
    fs.writeFileSync('AMD_mean_reversion_data.csv', csv);
    console.log("Data saved to AMD_mean_reversion_data.csv");

  } catch (error) {
    console.error("Error fetching bar data:", error);
  }
}

// Fetch account details
getAccount();

// Fetch AMD data and save to CSV
getBarData('AMD', '15Min', 100);
