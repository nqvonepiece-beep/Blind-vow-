--!strict
-- Điểm khởi động phía server.

local CombatService = require(script.Parent:WaitForChild("Combat"):WaitForChild("CombatService"))
local SwordGiver = require(script.Parent:WaitForChild("Combat"):WaitForChild("SwordGiver"))
local DummySpawner = require(script.Parent:WaitForChild("World"):WaitForChild("DummySpawner"))
local AvatarRig = require(script.Parent:WaitForChild("World"):WaitForChild("AvatarRig"))

print("Blind Vow khởi động (server)")

CombatService.init()
SwordGiver.init() -- trước AvatarRig: nếu nhân vật bị sinh lại, kiếm đã có sẵn trong StarterPack
AvatarRig.init()
DummySpawner.init()
