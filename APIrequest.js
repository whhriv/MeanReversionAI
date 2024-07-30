const url = 'http://localhost:5000/analyze';

const params = new URLSearchParams({
    ticker: 'OII',
    start_date: '2022-06-02',
    end_date: '2024-07-23'
});

fetch(`${url}?${params}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        // Process the data 
    })
    .catch(error => {
        console.error('Error:', error);
    });
