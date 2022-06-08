from functools import partial
import signal
import sys
from requests import request
import websockets
import asyncio
import json
import os
from quart import Quart
from jsonschema import validate

connected = []


def getenv(key, default):
    env = os.environ.get(key)
    return env if env is not None else default


async def watch(websocket):
    try:
        await websocket.wait_closed()
    finally:
        print(f'remove websocket id = {websocket.id}')
        connected.remove(websocket)

def validateJson(message):
    schema = {
        "properties": {
            "type": { "type": "string" },
        }
    }
    validate(instance=message, schema=schema)


async def handler(websocket):
    async for message in websocket:
        try:
            print(message)
            validate(message)
            event = json.loads(message)
            action = event['type']
            print(f'action {action} for websocket {websocket.id}')
            if action == 'init':
                connected.append(websocket)
            elif action == 'watch':
                await watch(websocket)
            elif action == 'exit':
                connected.remove(websocket)
        except Exception as e:
            print(f'handler websocket failed with {e}')
            connected.remove(websocket)


def boradcast(message):
    print(f'broadacst message {message}')
    websockets.broadcast(connected, message)


async def serveWebsocket():
    try:
        print('Serve websockets...')
        wss = getenv('WSS', 8765)
        async with websockets.serve(handler, 'localhost', wss):
            await asyncio.Future()
    except SystemExit:
        print('System-Exit')
    except KeyboardInterrupt:
        print('Serve websocket canncelted')


# Flask App
app = Quart(__name__)


@app.route('/ping')
async def ping():
    return { "message": "pong" }


@app.after_serving
async def shutdown():
    sys.exit('app aborted by user')


async def run_app():
    try:
        print('Run app...')
        port = getenv('PORT', 5000)
        await app.run_task(port=port)
    except SystemExit:
        print('Aborted')
        return 


def ask_exit2(signame, loop):
    try:
        print("got signal %s: exit" % signame)
        print('Exit')
        quit()
    except Exception as e:
        print(e)


async def main():
    try:
        tasks = [
            run_app(),
            serveWebsocket()
            ]

        loop = asyncio.get_running_loop()
        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                partial(ask_exit2, signame, loop))    

        print('Starting tasks')
        await asyncio.gather(*tasks)
        # await asyncio.wait(tasks)
    except SystemExit:
        print('System-Exit')
        pass
    except KeyboardInterrupt:
        print('ctrl-c')
        pass


if __name__ == "__main__":
    asyncio.run(main())