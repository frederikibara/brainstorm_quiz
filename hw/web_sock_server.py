import asyncio
import websockets
import json
from datetime import datetime, timedelta
import aiofile
import aiopath

API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
MAX_DAYS = 10
LOG_FILE = "exchange_log.txt"

async def fetch_currency_rates(date):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL + date) as response:
                response.raise_for_status()
                data = await response.json()
                rates = {'EUR': {}, 'USD': {}}
                for currency in data['exchangeRate']:
                    if currency['currency'] in rates:
                        rates[currency['currency']]['sale'] = currency['saleRate']
                        rates[currency['currency']]['purchase'] = currency['purchaseRate']
                return rates
        except aiohttp.ClientError as e:
            print(f"Error fetching data for {date}: {e}")
            return None

async def exchange_command(websocket, path):
    if path.startswith("/exchange"):
        query = path[len("/exchange"):]
        try:
            days = int(query)
            if days > MAX_DAYS:
                await websocket.send(json.dumps({"error": f"Cannot fetch more than {MAX_DAYS} days of data."}))
                return
            
            dates = [(datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]
            results = []
            for date in dates:
                rates = await fetch_currency_rates(date)
                if rates:
                    results.append({date: rates})
            result_str = json.dumps(results, indent=2)
            
            async with aiofile.AIOFile(LOG_FILE, 'a') as log_file:
                await log_file.write(f"{datetime.now()} - exchange {days}\n")
            
            await websocket.send(result_str)
        except ValueError:
            await websocket.send(json.dumps({"error": "Invalid number of days."}))

async def main():
    async with websockets.serve(exchange_command, "localhost", 8765):
        await asyncio.Future()  

if __name__ == "__main__":
    asyncio.run(main()) 
  
    

# Встановлення залежностей
# Щоб встановити всі необхідні бібліотеки, запустіть:

# bash
# pip install aiohttp websockets aiofile aiopath
# Запуск
# Для запуску консольної утиліти використовуйте команду:
# bash
# python main.py 2
# Для запуску веб-сокет сервера використовуйте команду:
# bash
# python websocket_server.py