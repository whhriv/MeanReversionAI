const url = 'http://localhost:5000/meanreversion';

const params = new URLSearchParams({
    ticker: 'OII',
    start_date: '2022-06-02',
    end_date: '2024-07-23'
});

fetch(`${url}?${params}`)
    .then(response => {
        console.log('Response Status:', response.status);
        console.log('Response Headers:', response.headers);
        return response.text(); // Read the response as text
    })
    .then(text => {
        console.log('Response Text:', text);
        try {
            const data = JSON.parse(text); // Attempt to parse as JSON
            console.log('Parsed Data:', data);
            return data;
        } catch (e) {
            console.error('JSON Parsing Error:', e);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
