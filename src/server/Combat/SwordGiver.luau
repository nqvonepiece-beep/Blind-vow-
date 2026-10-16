--!strict
-- Tạo Tool kiếm từ mô hình 3D thật (ServerStorage.Assets.Weapons) và phát cho người chơi.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")
local StarterPack = game:GetService("StarterPack")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local WeaponModelConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponModelConfig"))

-- Phải trùng khóa trong WeaponConfig, combat tìm thông số theo tên Tool.
local SWORD_NAME = "Sword"

local SwordGiver = {}

local function findModel(modelName: string): Model?
	local assets = ServerStorage:FindFirstChild("Assets")
	local weapons = assets and assets:FindFirstChild("Weapons")
	local model = weapons and weapons:FindFirstChild(modelName)
	if model and model:IsA("Model") then
		return model
	end
	return nil
end

local function buildSword(): Tool?
	local config = WeaponModelConfig[SWORD_NAME]
	local source = findModel(config.modelName)
	if not source then
		warn(`[SwordGiver] Không tìm thấy ServerStorage.Assets.Weapons.{config.modelName}. Kiểm tra Rojo đã sync assets/roblox/weapons chưa.`)
		return nil
	end

	local model = source:Clone()
	local handle = model:FindFirstChild(config.handlePartName)
	if not handle or not handle:IsA("BasePart") then
		warn(`[SwordGiver] Model {config.modelName} thiếu phần {config.handlePartName}.`)
		model:Destroy()
		return nil
	end

	local tool = Instance.new("Tool")
	tool.Name = SWORD_NAME
	tool.RequiresHandle = true
	tool.CanBeDropped = false

	-- Kiếm chỉ để nhìn: không va chạm, không nặng, không neo, để không cản di chuyển.
	-- Sát thương do server tính bằng hitbox riêng (CombatService), không dùng va chạm của kiếm.
	for _, descendant in model:GetDescendants() do
		if descendant:IsA("BasePart") then
			descendant.Anchored = false
			descendant.CanCollide = false
			descendant.CanTouch = false
			descendant.CanQuery = false
			descendant.Massless = true
			if descendant ~= handle then
				local weld = Instance.new("WeldConstraint")
				weld.Part0 = handle
				weld.Part1 = descendant
				weld.Parent = descendant
			end
		end
	end

	handle.Name = "Handle"
	for _, child in model:GetChildren() do
		child.Parent = tool
	end
	model:Destroy()

	-- Tool.Grip: điểm nắm tay và hướng của kiếm so với Handle.
	local orientation = CFrame.Angles(math.rad(config.gripTiltDegrees), 0, 0)
		* CFrame.Angles(0, math.rad(config.gripTurnDegrees), 0)
	tool.Grip = CFrame.new(config.gripOffset) * orientation:Inverse()

	return tool
end

function SwordGiver.init()
	local template = buildSword()
	if not template then
		return
	end
	template.Parent = StarterPack

	-- Người chơi đã vào trước khi script chạy sẽ không nhận từ StarterPack.
	for _, player in Players:GetPlayers() do
		local backpack = player:FindFirstChildOfClass("Backpack")
		if backpack and not backpack:FindFirstChild(SWORD_NAME) then
			template:Clone().Parent = backpack
		end
	end
end

return SwordGiver
