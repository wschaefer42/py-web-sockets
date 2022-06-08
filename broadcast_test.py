import pytest
from broadcast import app

def hello():
    return 'hello'

def test_hello():
    assert hello() == 'hello'

@pytest.fixture(name='app')
def _app():
    return app

@pytest.mark.asyncio
async def test_websocket(app):
    test_client = app.test_client()
    data = b'Bob'
    async with test_client.websocket('/ws') as test_websocket:
        await test_websocket.send(data)
        result = await test_websocket.receive()
    assert result == data