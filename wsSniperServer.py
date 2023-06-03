import asyncio
import json
import websockets
import requests

ip = "localhost"
port = 8080
game_id = None
asset_id = None
version = "1.0"

versionreq = requests.get("https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/SERVERVERSION.md")
print("Version: " + version)
print("Latest version: " + versionreq.text)
if version != versionreq.text:
    print("Please update to the latest version.")

async def send_game_and_asset_ids(websocket, path):
    global game_id
    global asset_id
    while game_id is None or asset_id is None:
        await asyncio.sleep(1)
    # Send game and asset ids to the LuaU script
    data = {"gameId": game_id, "assetId": asset_id}
    await websocket.send(json.dumps(data))

# Start the server
start_server = websockets.serve(send_game_and_asset_ids, ip, port)
print("Server started on ws://" + ip + ":" + str(port) + "/")

asyncio.get_event_loop().run_until_complete(start_server)

async def get_user_input():
    global game_id
    global asset_id
    while game_id is None or asset_id is None:
        game_id = await asyncio.to_thread(input, "Enter the game id: ")
        asset_id = await asyncio.to_thread(input, "Enter the asset id: ")

asyncio.get_event_loop().run_until_complete(get_user_input())
asyncio.get_event_loop().run_forever()