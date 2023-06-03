getgenv().afterassetid = readfile("afterassetid.txt")
getgenv().loopmplaceservice = true
while loopmplaceservice == true do
    game:GetService("MarketplaceService"):PromptPurchase(game.Players.LocalPlayer, afterassetid)
    wait(1)
end