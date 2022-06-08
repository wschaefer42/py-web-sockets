from dataclasses import dataclass
from quart import Quart, jsonify, request
import json

app = Quart(__name__)

@dataclass
class Name:
    name: str
    email: str

name = Name('alice', 'alice@outlook.com')

@app.route('/name', methods=['GET', 'PUT'])
async def name_route():
    if request.method == 'GET':
        return jsonify(name)
    elif request.method == 'PUT':
        # This is special for Quart to await for the request data
        # data = await request.data
        # record = json.loads(data)
        record = await request.get_json(force=True)
        name.name = record["name"]
        name.email = record["email"]
        return jsonify(name)

app.run(port=5011)
