import aiohttp
import asyncio
from .utils import get_last_n_days_dates

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

class ExchangeRateService:
    async def fetch_exchange_rates(self, session, date):
        url = f"{API_URL}{date}"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            logging.error(f"HTTP error: {e}")
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Connection error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        return None

    async def get_rates_for_dates(self, days, currencies):
        dates = get_last_n_days_dates(days)
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_exchange_rates(session, date) for date in dates]
            responses = await asyncio.gather(*tasks)
        
        results = []
        for date, response in zip(dates, responses):
            if response:
                rates = self.extract_rates(response, currencies)
                if rates:
                    results.append({date: rates})
        
        return results

    def extract_rates(self, data, currencies):
        if data is None:
            return None
        
        rates = {}
        for item in data.get('exchangeRate', []):
            if item['currency'] in currencies:
                rates[item['currency']] = {
                    'sale': item['saleRateNB'],
                    'purchase': item['purchaseRateNB']
                }
        return rates
