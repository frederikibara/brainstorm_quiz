import asyncio
import logging
import websockets
import aiohttp
import json
import datetime
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiofile import AIOFile
from aiopath import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = f"User{len(self.clients)+1}"
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')


    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')


    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]


    async def fetch_exchange_rates(self, currencies, date=None):
        api_url = 'https://api.privatbank.ua/p24api/exchange_rates?json'
        if date:
            api_url += f'&date={date}'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {currency: {"sale": 0, "purchase": 0} for currency in currencies}
                    for rate in data.get('exchangeRate', []):
                        if rate['currency'] in rates:
                            rates[rate['currency']]['sale'] = rate['saleRate']
                            rates[rate['currency']]['purchase'] = rate['purchaseRate']
                    return rates
                else:
                    return None


    async def handle_exchange_command(self, ws: WebSocketServerProtocol, params):
        if len(params) > 1:
            try:
                days = int(params[1])
                if days < 1 or days > 10:
                    await ws.send("Введіть число від 1 до 10 для кількості днів.")
                    return
                date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%d.%m.%Y')
            except ValueError:
                await ws.send("Невірний формат кількості днів.")
                return
        else:
            date = None
        
        currencies = params[2:] if len(params) > 2 else ['USD', 'EUR']

        rates = await self.fetch_exchange_rates(currencies, date)
        if not rates:
            await ws.send("Не вдалося отримати курси валют.")
            return

        message = json.dumps(rates, indent=2)
        await ws.send(message)

        async with AIOFile('exchange_commands.log', 'a') as log_file:
            await log_file.write(f"{datetime.datetime.now()} - {ws.name} - Command: {' '.join(params)}\n")


    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            async for message in ws:
                if message.startswith('exchange'):
                    params = message.split()
                    await self.handle_exchange_command(ws, params)
                else:
                    await self.send_to_clients(f"{ws.name}: {message}")
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
