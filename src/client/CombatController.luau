--!strict
-- Nhận thao tác đánh của người chơi và gửi yêu cầu lên server.
-- Client không quyết định trúng hay sát thương.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Remotes = require(Shared:WaitForChild("Remotes"))
local WeaponConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponConfig"))

local CombatController = {}

local player = Players.LocalPlayer
local hookedTools: { [Tool]: boolean } = {}
local lastAttackTime = 0

local function playSwing(tool: Tool, duration: number)
	-- Hiệu ứng vung kiếm tạm bằng cách xoay Grip, chưa dùng animation.
	local restGrip = tool.Grip
	local swingGrip = restGrip * CFrame.Angles(math.rad(-80), 0, 0)
	local half = TweenInfo.new(duration / 2, Enum.EasingStyle.Quad)
	local down = TweenService:Create(tool, half, { Grip = swingGrip })
	down.Completed:Once(function()
		TweenService:Create(tool, half, { Grip = restGrip }):Play()
	end)
	down:Play()
end

local function hookTool(tool: Tool, attackRequest: RemoteEvent)
	local stats = WeaponConfig[tool.Name]
	if not stats or hookedTools[tool] then
		return
	end
	hookedTools[tool] = true

	tool.Activated:Connect(function()
		local now = os.clock()
		if now - lastAttackTime < stats.cooldown then
			return
		end
		lastAttackTime = now
		attackRequest:FireServer()
		playSwing(tool, stats.cooldown * 0.6)
	end)

	tool.Destroying:Connect(function()
		hookedTools[tool] = nil
	end)
end

local function watchContainer(container: Instance, attackRequest: RemoteEvent)
	for _, child in container:GetChildren() do
		if child:IsA("Tool") then
			hookTool(child, attackRequest)
		end
	end
	container.ChildAdded:Connect(function(child: Instance)
		if child:IsA("Tool") then
			hookTool(child, attackRequest)
		end
	end)
end

function CombatController.init()
	local attackRequest = Remotes.get(Remotes.Names.AttackRequest)

	local function onCharacterAdded(character: Model)
		watchContainer(character, attackRequest)
		watchContainer(player:WaitForChild("Backpack"), attackRequest)
	end

	if player.Character then
		onCharacterAdded(player.Character)
	end
	player.CharacterAdded:Connect(onCharacterAdded)
end

return CombatController
