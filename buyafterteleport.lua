while true do
    game:GetService("MarketplaceService"):PromptPurchase(game.Players.LocalPlayer, assetId)
    wait(1)
end