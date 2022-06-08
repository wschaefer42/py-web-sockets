import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send('Hello websocket world')
        message = await websocket.recv()
        print(f'received {message}')

asyncio.run(hello())