import asyncio
import json
import websockets
import requests
import discord
import re
import aiohttp

game_id = None
asset_id = None
version = "2.0"
# Change these variables to your liking
ip = "localhost"
port = 8080
roblosecurity = "ROBLOSECURITY HERE"
bottoken = "BOT TOKEN HERE"
allowed_channels = [1111111111111111, 11111111111111111111]
# Don't change anything below this line unless you know what you're doing

client = discord.Client()

versionreq = requests.get("https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/SERVERVERSION.md")
print("Version: " + version)
print("Latest version: " + versionreq.text)
if version != versionreq.text:
    print("Please update to the latest version.")

@client.event
async def on_ready():
    print(f'Discord ID Watcher has started.')

@client.event
async def on_message(message):
    if message.channel.id in allowed_channels:
        if message.author == client.user:
            return

        if message.content.startswith('$ping'):
            print("Pong")

        robloxlink = re.compile(r'https?://www\.roblox\.com/catalog/(\d+)(?:/.+)?')
        match = robloxlink.search(message.content)

        if not match and message.embeds:
            for embed in message.embeds:
                if embed.author:
                    match = robloxlink.search(embed.author.url)
                    if match:
                        break
                if embed.url:
                    match = robloxlink.search(embed.url)
                    if match:
                        break

        if match:
            global asset_id
            global game_id
            asset_id = match.group(1)
            print(f"Found asset ID: {asset_id}")
            async with aiohttp.ClientSession(cookies={".ROBLOSECURITY": roblosecurity}) as session:
                # Get asset details
                async with session.get(f"https://economy.roblox.com/v2/assets/{asset_id}/details") as economyreq:
                    if economyreq.status != 200:
                        print("Roblox didn't properly respond.")
                        asset_id = None
                    else:
                        economy_data = await economyreq.json()
                        if economy_data["SaleLocation"] is None or len(economy_data["SaleLocation"].get("UniverseIds", [])) == 0:
                            print("No game associated with this asset.")
                            asset_id = None
                        else:
                            universe_ids = economy_data['SaleLocation'].get('UniverseIds', [])
                            # Get game details
                            async with session.get(f"https://games.roblox.com/v1/games?universeIds={','.join(str(id) for id in universe_ids)}") as gamereq:
                                if gamereq.status != 200:
                                    print("Roblox didn't properly respond.")
                                    asset_id = None
                                else:
                                    game_data = await gamereq.json()
                                    game_id = str(game_data["data"][0]['rootPlaceId'])
                                    print(f"Found game ID: {game_id}")
                                    await asyncio.sleep(5)
                                    game_id = None
                                    asset_id = None

async def send_game_and_asset_ids(websocket):
    while game_id is None or asset_id is None:
        await asyncio.sleep(1)
    # Send game and asset ids to the LuaU script
    data = {"gameId": game_id, "assetId": asset_id}
    await websocket.send(json.dumps(data))

async def start_websocket_server(ip, port):
    # Start the server
    start_server = websockets.serve(send_game_and_asset_ids, ip, port) # type: ignore
    print("Server started on ws://" + ip + ":" + str(port) + "/")
    await start_server
    
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    start_websocket_server(ip, port),
    client.start(bottoken),
))

loop.close()