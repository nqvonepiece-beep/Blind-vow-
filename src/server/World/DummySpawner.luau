--!strict
-- Tạo hình nộm tập đánh, hồi sinh sau khi bị hạ.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local DummyConfig = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Config"):WaitForChild("DummyConfig"))
local HealthBar = require(script.Parent:WaitForChild("HealthBar"))

local DummySpawner = {}

-- Các bộ phận tính theo vị trí so với HumanoidRootPart.
local BODY_PARTS = {
	{ name = "Torso", size = Vector3.new(2, 2, 1), offset = Vector3.new(0, 0, 0) },
	{ name = "Head", size = Vector3.new(2, 1, 1), offset = Vector3.new(0, 1.5, 0) },
	{ name = "Left Arm", size = Vector3.new(1, 2, 1), offset = Vector3.new(-1.5, 0, 0) },
	{ name = "Right Arm", size = Vector3.new(1, 2, 1), offset = Vector3.new(1.5, 0, 0) },
	{ name = "Left Leg", size = Vector3.new(1, 2, 1), offset = Vector3.new(-0.5, -2, 0) },
	{ name = "Right Leg", size = Vector3.new(1, 2, 1), offset = Vector3.new(0.5, -2, 0) },
}

local function buildDummy(): Model
	local model = Instance.new("Model")
	model.Name = "TrainingDummy"

	local rootCFrame = CFrame.new(DummyConfig.spawnPosition)

	local root = Instance.new("Part")
	root.Name = "HumanoidRootPart"
	root.Size = Vector3.new(2, 2, 1)
	root.CFrame = rootCFrame
	root.Transparency = 1
	root.Anchored = true
	root.Parent = model
	model.PrimaryPart = root

	local head: BasePart = root
	for _, info in BODY_PARTS do
		local part = Instance.new("Part")
		part.Name = info.name
		part.Size = info.size
		part.CFrame = rootCFrame + info.offset
		part.Color = Color3.fromRGB(160, 120, 80)
		part.Parent = model

		local weld = Instance.new("WeldConstraint")
		weld.Part0 = root
		weld.Part1 = part
		weld.Parent = part

		if info.name == "Head" then
			head = part
		end
	end

	local humanoid = Instance.new("Humanoid")
	humanoid.MaxHealth = DummyConfig.maxHealth
	humanoid.Health = DummyConfig.maxHealth
	humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
	humanoid.Parent = model

	HealthBar.attach(humanoid, head)
	return model
end

local function collapse(model: Model)
	-- Gỡ mối hàn và bỏ khóa để các bộ phận rơi xuống đất.
	for _, descendant in model:GetDescendants() do
		if descendant:IsA("WeldConstraint") then
			descendant:Destroy()
		elseif descendant:IsA("BasePart") then
			descendant.Anchored = false
		end
	end
end

local function isSpawnBlocked(): boolean
	local params = OverlapParams.new()
	local parts = workspace:GetPartBoundsInRadius(DummyConfig.spawnPosition, DummyConfig.spawnClearRadius, params)
	for _, part in parts do
		local model = part:FindFirstAncestorOfClass("Model")
		if model and Players:GetPlayerFromCharacter(model) then
			return true
		end
	end
	return false
end

local spawnDummy: () -> ()

local function respawnWhenClear()
	while isSpawnBlocked() do
		task.wait(0.5)
	end
	spawnDummy()
end

function spawnDummy()
	local model = buildDummy()
	local humanoid = model:FindFirstChildOfClass("Humanoid") :: Humanoid

	humanoid.Died:Connect(function()
		collapse(model)
		task.delay(DummyConfig.respawnDelay, function()
			model:Destroy()
			respawnWhenClear()
		end)
	end)

	model.Parent = workspace
end

function DummySpawner.init()
	spawnDummy()
end

return DummySpawner
