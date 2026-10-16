--!strict
-- Ép nhân vật người chơi dùng khung xương theo AvatarConfig (mặc định R15),
-- không cần chỉnh Avatar Settings trên Roblox.
-- Cách làm: tạo mẫu "StarterCharacter" trong StarterPlayer; Roblox sẽ sinh
-- nhân vật từ mẫu này. Sau đó áp ngoại hình avatar của người chơi lên.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterPlayer = game:GetService("StarterPlayer")

local AvatarConfig = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Config"):WaitForChild("AvatarConfig"))

local AvatarRig = {}

local function buildStarterCharacter()
	local model = Players:CreateHumanoidModelFromDescription(Instance.new("HumanoidDescription"), AvatarConfig.rigType)
	model.Name = "StarterCharacter"
	model.Parent = StarterPlayer
end

local function applyAppearance(player: Player, character: Model)
	if not AvatarConfig.useOwnAppearance or player.UserId <= 0 then
		return
	end
	local ok, description = pcall(function()
		return Players:GetHumanoidDescriptionFromUserId(player.UserId)
	end)
	if not ok then
		warn("Không tải được ngoại hình của " .. player.Name .. ": " .. tostring(description))
		return
	end
	if not character.Parent then
		character.AncestryChanged:Wait()
	end
	local humanoid = character:WaitForChild("Humanoid", 5)
	if humanoid and humanoid:IsA("Humanoid") and character.Parent then
		local applied, err = pcall(function()
			humanoid:ApplyDescription(description)
		end)
		if not applied then
			warn("Không áp được ngoại hình cho " .. player.Name .. ": " .. tostring(err))
		end
	end
end

local function watchPlayer(player: Player)
	player.CharacterAdded:Connect(function(character)
		applyAppearance(player, character)
	end)

	-- Nhân vật sinh ra trước khi có mẫu thì sinh lại cho đúng khung xương.
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if humanoid and humanoid.RigType ~= AvatarConfig.rigType then
		player:LoadCharacter()
	elseif character then
		task.spawn(applyAppearance, player, character)
	end
end

function AvatarRig.init()
	buildStarterCharacter()
	Players.PlayerAdded:Connect(watchPlayer)
	for _, player in Players:GetPlayers() do
		watchPlayer(player)
	end
end

return AvatarRig
