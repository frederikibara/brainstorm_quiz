import argparse
import asyncio
from aiohttp import ClientSession, ClientError
from datetime import datetime, timedelta

API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
MAX_DAYS = 10

async def fetch_currency_rates(session, date):
    try:
        async with session.get(API_URL + date) as response:
            response.raise_for_status()
            data = await response.json()
            rates = { 'EUR': {}, 'USD': {} }
            for currency in data['exchangeRate']:
                if currency['currency'] in rates:
                    rates[currency['currency']]['sale'] = currency['saleRate']
                    rates[currency['currency']]['purchase'] = currency['purchaseRate']
            return rates
    except ClientError as e:
        print(f"Error fetching data for {date}: {e}")
        return None

async def get_rates(days):
    if days > MAX_DAYS:
        print(f"Cannot fetch more than {MAX_DAYS} days of data.")
        return
    
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]
    async with ClientSession() as session:
        results = []
        for date in dates:
            rates = await fetch_currency_rates(session, date)
            if rates:
                results.append({date: rates})
        return results

def main():
    parser = argparse.ArgumentParser(description="Fetch currency rates from PrivatBank API.")
    parser.add_argument("days", type=int, help="Number of days of currency rates to fetch.")
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop()
    rates = loop.run_until_complete(get_rates(args.days))
    print(rates)

if __name__ == "__main__":
    main()
