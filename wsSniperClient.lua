local executor = identifyexecutor()
local checkedexecutor = false

print("Executor: " .. executor)
if executor == "Electron" then
    print(executor .. " is confirmed to be supported.")
    checkedexecutor = true
end
if executor == "Celery" or not identifyexecutor() then
    print(executor .. " is not supported (yet).")
    checkedexecutor = true
end
if executor == "ArceusX" or executor == "Evon" or executor == "Valyse" then
    print(executor .. " is malware. Get rid of it ASAP.")
    checkedexecutor = true
end
if checkedexecutor == false then
    print(executor .. " MIGHT be supported. Make sure it's compatible with UNC and MarketplaceService. If your executor is supported and you see this message, send a screenshot of this to BestAdam#9280 on Discord.")
    checkedexecutor = true
end

local versionreq = request({
	Url = "https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/CLIENTVERSION.md",
	Method = "GET",
})
print("\nVersion 1.1\nLatest version is " .. versionreq.Body .. "\nMake sure to launch using the script provided in the README. If you don't, you'll be running an outdated version! bestadamdagoat/WebSocket-Sniper")

local HttpService = game:GetService("HttpService")
print("Attempting to connect to websocket")
print(wsversion .. "://" .. domain)
local ws = WebSocket.connect(wsversion .. "://" .. domain)
print("Connected to websocket")

ws.OnMessage:Connect(function(message)
    print("Message recieved: " .. message)
    local data = HttpService:JSONDecode(message)
    local gameId = data.gameId
    print("GameId: " .. gameId)
    getgenv().assetId = data.assetId
    print("AssetId: " .. assetId)

    queue_on_teleport("loadstring(game:HttpGet('https://raw.githubusercontent.com/bestadamdagoat/WebSocket-Sniper/main/buyafterteleport.lua'))()")
    print("Queued buyafterteleport.lua")
    game:GetService("TeleportService"):Teleport(gameId, game:GetService("Players").LocalPlayer)
    warn("If you see this, you either failed to teleport or your computer is slow. If you failed to teleport, make sure you're in a game that supports 3rd Party Teleports. If your computer is slow, please wait a few seconds and then run the script again.")
end)

ws.OnClose:Connect(function()
	warn("The server has closed the connection.")
end)