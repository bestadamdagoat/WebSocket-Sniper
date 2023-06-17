import asyncio
import json
import websockets
import requests

ip = "localhost"
port = 8080
game_id = None
asset_id = None
roblosecurity = "PLACE ROBLOSECURITY HERE"
version = "1.5"

versionreq = requests.get("https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/SERVERVERSION.md")
print("Version: " + version)
print("Latest version: " + versionreq.text)
if version != versionreq.text:
    print("Please update to the latest version.")

async def send_game_and_asset_ids(websocket, path):
    while game_id is None or asset_id is None:
        await asyncio.sleep(1)
    # Send game and asset ids to the LuaU script
    data = {"gameId": game_id, "assetId": asset_id}
    await websocket.send(json.dumps(data))

# Start the server
start_server = websockets.serve(send_game_and_asset_ids, ip, port) # type: ignore
print("Server started on ws://" + ip + ":" + str(port) + "/")

asyncio.get_event_loop().run_until_complete(start_server)

async def get_user_input():
    global game_id
    global asset_id
    while asset_id is None:
        asset_id = await asyncio.to_thread(input, "Enter the asset id: ")
    economyreq = requests.get(f"https://economy.roblox.com/v2/assets/{asset_id}/details", cookies={".ROBLOSECURITY": roblosecurity})
    if economyreq.status_code != 200:
        print("Roblox didn't properly respond.")
    else:
        if (economyreq.json())["SaleLocation"] is None or len((economyreq.json())["SaleLocation"].get("UniverseIds", [])) == 0:
            print("No game associated with this asset.")
        else:
            universe_ids = (economyreq.json())['SaleLocation'].get('UniverseIds', [])
            gamereq = requests.get(f"https://games.roblox.com/v1/games?universeIds={','.join(str(id) for id in universe_ids)}", cookies={".ROBLOSECURITY": roblosecurity})
            if gamereq.status_code != 200:
                print("Roblox didn't properly respond.")
            else:
                game_id = str(gamereq.json()["data"][0]['rootPlaceId'])

asyncio.get_event_loop().run_until_complete(get_user_input())
asyncio.get_event_loop().run_forever()