import asyncio
import logging
import websockets
from websockets.exceptions import ConnectionClosedOK
from .api import ExchangeRateService
from aiofile import AIOFile
from .utils import get_last_n_days_dates

logging.basicConfig(level=logging.INFO)

LOG_FILE = 'exchange_commands.log'

class ExchangeCommandHandler:
    def __init__(self, exchange_service):
        self.exchange_service = exchange_service

    async def handle_exchange_command(self, ws, message):
        try:
            _, *args = message.split()
            days = int(args[0]) if args else 1
            currencies = args[1:] if len(args) > 1 else ['EUR', 'USD']
            
            if not (1 <= days <= 10):
                raise ValueError("Number of days must be between 1 and 10.")
            
            results = await self.exchange_service.get_rates_for_dates(days, currencies)
            response_message = f"Exchange rates for the last {days} days: {results}"
            await ws.send(response_message)
            
            await self.log_exchange_command(f"{ws.remote_address} requested exchange rates: {message}")
        except Exception as e:
            await ws.send(f"Error: {e}")

    async def log_exchange_command(self, message):
        async with AIOFile(LOG_FILE, 'a') as afp:
            await afp.write(f"{message}\n")

class WebSocketServer:
    def __init__(self, exchange_service):
        self.exchange_command_handler = ExchangeCommandHandler(exchange_service)
        self.clients = set()

    async def register(self, ws):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message):
        if self.clients:
            await asyncio.gather(*(client.send(message) for client in self.clients))

    async def ws_handler(self, ws):
        await self.register(ws)
        try:
            async for message in ws:
                if message.startswith("exchange"):
                    await self.exchange_command_handler.handle_exchange_command(ws, message)
                else:
                    await self.send_to_clients(f"{ws.remote_address}: {message}")
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

async def main():
    exchange_service = ExchangeRateService()
    server = WebSocketServer(exchange_service)
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
