import asyncio
from quart import Quart, websocket, render_template


app = Quart(__name__)


@app.route('/ping')
async def ping():
    return {"message": "pong"}

@app.route('/hello')
async def hello():
    return await render_template('hello.html')

@app.route('/')
async def index():
    return await render_template('index.html', title='Websocket with Quart')

@app.websocket('/ws')
async def ws():
    await websocket.accept()
    while True:
        data = await websocket.receive()
        print(f'received {data}')
        await websocket.send(data)

'''Broadcast Version -----------------------'''

connected = set()

async def broadcast(message):
    for queue in connected:
        await queue.put(message)

@app.websocket('/api/v2/ws')
async def ws_v2():
    print(f'websocket broadcast request')
    queue = asyncio.Queue()
    connected.add(queue)
    try:
        while True:
            data = await queue.get()
            await websocket.send(data)
    except:
        connected.remove(queue)

@app.route('/send/<message>')
async def send(message):
    print(f'broadcast message {message}')
    await broadcast(message)
    return {'status': 'sent'}


'''Main Loop -----------------------------'''

if __name__ == '__main__':
    app.run(port=5005)