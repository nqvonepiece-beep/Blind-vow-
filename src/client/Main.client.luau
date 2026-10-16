--!strict
-- Điểm khởi động phía client.

local CombatController = require(script.Parent:WaitForChild("CombatController"))
local HitFeedback = require(script.Parent:WaitForChild("HitFeedback"))
local WeaponStance = require(script.Parent:WaitForChild("WeaponStance"))
local WeaponDrawController = require(script.Parent:WaitForChild("WeaponDrawController"))

print("Blind Vow khởi động (client)")

CombatController.init()
HitFeedback.init()
WeaponStance.init()
WeaponDrawController.init()
