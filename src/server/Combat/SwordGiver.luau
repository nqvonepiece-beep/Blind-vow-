--!strict
-- Tạo Tool kiếm từ mô hình 3D thật (ServerStorage.Assets.Weapons) và phát cho người chơi.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local StarterPack = game:GetService("StarterPack")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local WeaponModelConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponModelConfig"))
local WeaponAssets = require(script.Parent:WaitForChild("WeaponAssets"))

-- Phải trùng khóa trong WeaponConfig, combat tìm thông số theo tên Tool.
local SWORD_NAME = "Sword"

local SwordGiver = {}

-- Tool.Grip từ hướng kiếm trong bàn tay (xem WeaponModelConfig).
local function buildGrip(config: WeaponModelConfig.WeaponModel): CFrame
	-- Đổi từ trục bàn tay sang trục RightGripAttachment (xoay -90° quanh X so với bàn tay).
	local function toAttachment(v: Vector3): Vector3
		return Vector3.new(v.X, -v.Z, v.Y)
	end
	local blade = toAttachment(config.gripBladeDirection).Unit
	local edge = toAttachment(config.gripEdgeDirection)
	edge = (edge - blade * edge:Dot(blade)).Unit
	-- Hướng của Handle so với bàn tay: trục X của kiếm = lưỡi sắc, trục Y = mũi kiếm.
	local orientation = CFrame.fromMatrix(Vector3.zero, edge, blade)
	return CFrame.new(config.gripOffset) * orientation:Inverse()
end

local function buildSword(): Tool?
	local config = WeaponModelConfig[SWORD_NAME]
	local source = WeaponAssets.findModel(config.modelName)
	if not source then
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

	for _, descendant in model:GetDescendants() do
		if descendant:IsA("BasePart") then
			WeaponAssets.makeVisualOnly(descendant)
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

	tool.Grip = buildGrip(config)
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
