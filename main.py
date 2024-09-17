import argparse
import asyncio
from server.api import ExchangeRateService
from server.utils import get_last_n_days_dates

async def fetch_and_print_rates(days):
    exchange_service = ExchangeRateService()
    currencies = ['EUR', 'USD']
    rates = await exchange_service.get_rates_for_dates(days, currencies)
    for rate in rates:
        print(rate)

def main():
    parser = argparse.ArgumentParser(description='Fetch exchange rates for the last few days.')
    parser.add_argument('days', type=int, help='Number of days to fetch rates for (max 10 days).')
    args = parser.parse_args()
    
    if args.days < 1 or args.days > 10:
        print("Number of days must be between 1 and 10.")
        return
    
    asyncio.run(fetch_and_print_rates(args.days))

if __name__ == "__main__":
    main()
