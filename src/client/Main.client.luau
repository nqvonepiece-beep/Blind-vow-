--!strict
-- Điểm khởi động phía client.

local CombatController = require(script.Parent:WaitForChild("CombatController"))
local HitFeedback = require(script.Parent:WaitForChild("HitFeedback"))

print("Blind Vow khởi động (client)")

CombatController.init()
HitFeedback.init()
