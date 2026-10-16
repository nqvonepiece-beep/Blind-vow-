--!strict
-- Điểm khởi động phía server.

local CombatService = require(script.Parent:WaitForChild("Combat"):WaitForChild("CombatService"))
local SwordGiver = require(script.Parent:WaitForChild("Combat"):WaitForChild("SwordGiver"))
local WeaponHolster = require(script.Parent:WaitForChild("Combat"):WaitForChild("WeaponHolster"))
local DummySpawner = require(script.Parent:WaitForChild("World"):WaitForChild("DummySpawner"))

print("Blind Vow khởi động (server)")

CombatService.init()
SwordGiver.init()
WeaponHolster.init()
DummySpawner.init()
