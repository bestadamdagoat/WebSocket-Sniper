<div align="center">

# ANNOUNCEMENT: Join the Discord server [here](https://discord.gg/8fpAGnyqgW)

<div align="left">

# WebSocket-Sniper
A Roblox item sniper that uses websockets to automatically bring you to a game.

[![Watch the video](https://img.youtube.com/vi/darNLq4yFiI/mqdefault.jpg)](https://youtu.be/darNLq4yFiI)

You can visit [this board](https://github.com/users/bestadamdagoat/projects/3/views/1) to see upcoming features.

Made for Electron, but should be compatible with any executor that supports these UNC functions:
- [WebSockets](https://github.com/unified-naming-convention/NamingStandard/blob/main/api/WebSocket.md)
- [queue_on_teleport](https://github.com/unified-naming-convention/NamingStandard/blob/main/api/misc.md#queue_on_teleport) <sub><sup>(optional)</sup></sub>
- ~~MarketplaceService~~ <sub><sup>(no longer working after the Roblox update)</sup></sub>

## How do I use this?
You must have a server to connect to. This can be done by running wsSniperServer.py or by connecting to an external server. After that, you'll need to run the sniper script in your executor. The client script is the script that teleports your character and buys your item. You can view the logs by pressing F9 (highly recommended). Both the server and client will check for updates, but only the client will automatically update (if you run the correct script). The client will also automatically check for compatibility with your executor.

## Server (wsSniperServer.py)
The server is the thing that sends the information to the sniper (or client). Currently, the sniper finds assetIDs by using a Discord Self-Bot (or a fake user) to snoop in different servers. You must modify the server by changing the domain, port, ROBLOSECURITY cookie, bot token, and allowed channels (or Channel IDs). The cookie and bot token can be from a dummy account. Since it's a self-bot, you must use a token from a normal account, not a bot account. The server will automatically find the asset ID from a Roblox link and its associated game ID. You can also ping the bot by using the command `$ping`, it'll output to the terminal to decrease chances of detection. The only libraries you'll need to install are `websockets`, `requests`, `discord.py-self`, and `aiohttp`.

## Sniper (wsSniperClient.lua)
The sniper teleports you to the game ~~and buys the asset that was provided after being teleported~~ <sub><sup>(autobuy is no longer working after the Roblox update)</sup></sub> automatically. It gets this information from the server and logs all information into the console (access the console by pressing F9). You must be in a game that supports 3rd Party Teleports to be teleported automatically. If you want to modify the script that's queued to run on teleport (like adding [input](https://github.com/unified-naming-convention/NamingStandard/blob/main/api/input.md) support to purchase items), you can do that by changing out the purchase script. Now, to run this script while getting the latest updates, put the following script into your executor and edit the `DOMAINHERE` value to the server's domain (ex: `github.com`) and the `VERSIONHERE` domain to the websocket version you want to use (either `ws` or `wss`):
```lua
getgenv().domain = "DOMAINHERE"
getgenv().wsversion = "VERSIONHERE"
loadstring(game:HttpGet('https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/wsSniperClient.lua'))()
```
After putting that in, press execute. To use the script, you do need to be trying to connect to an active server, but the server doesn't need to be broadcasting any information.

## IMPORTANT NOTE ABOUT THE SERVER
During my testing, I observed that you can't actually access the server if it's being ran on localhost (or any local ip like 127.0.0.1, 0.0.0.0, etc.). I don't know if this is an Electron exclusive thing or something, as there's very little documentation on how to use websockets with Roblox. I got around this by using ngrok as a proxy (as seen in the linked video).
