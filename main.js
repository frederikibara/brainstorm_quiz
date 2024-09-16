document.getElementById('fetchRates').addEventListener('click', () => {
    
    const apiUrl = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=01.01.2024';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayRates(data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});

function displayRates(data) {
    const ratesDiv = document.getElementById('rates');
    ratesDiv.innerHTML = ''; 

    const rates = data.exchangeRate;

    if (!rates || rates.length === 0) {
        ratesDiv.textContent = 'denied request';
        return;
    }

    rates.forEach(rate => {
        const rateElement = document.createElement('div');
        rateElement.textContent = `${rate.currency}: ${rate.saleRate} / ${rate.purchaseRate}`;
        ratesDiv.appendChild(rateElement);
    });
}
