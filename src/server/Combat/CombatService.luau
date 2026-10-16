--!strict
-- Server quyết định đòn đánh: kiểm tra hồi chiêu, tính hitbox, trừ máu.
-- Client chỉ gửi "tôi muốn đánh", không gửi mục tiêu hay sát thương.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Remotes = require(Shared:WaitForChild("Remotes"))
local WeaponConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponConfig"))

local CombatService = {}

local lastAttackTime: { [Player]: number } = {}

local function getAliveParts(player: Player): (Model?, Humanoid?, BasePart?)
	local character = player.Character
	if not character then
		return nil, nil, nil
	end
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local root = character:FindFirstChild("HumanoidRootPart")
	if not humanoid or humanoid.Health <= 0 or not root or not root:IsA("BasePart") then
		return nil, nil, nil
	end
	return character, humanoid, root
end

local function getEquippedStats(character: Model): WeaponConfig.WeaponStats?
	local tool = character:FindFirstChildOfClass("Tool")
	if not tool then
		return nil
	end
	return WeaponConfig[tool.Name]
end

local function resolveHit(player: Player, stats: WeaponConfig.WeaponStats, hitConfirmed: RemoteEvent)
	-- Kiểm tra lại sau thời gian báo hiệu: người đánh có thể đã chết hoặc cất vũ khí.
	local character, _, root = getAliveParts(player)
	if not character or not root or getEquippedStats(character) ~= stats then
		return
	end

	local params = OverlapParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = { character }

	local hitboxCFrame = root.CFrame * CFrame.new(0, 0, -stats.hitboxOffset)
	local parts = workspace:GetPartBoundsInBox(hitboxCFrame, stats.hitboxSize, params)

	local alreadyHit: { [Humanoid]: boolean } = {}
	for _, part in parts do
		local model = part:FindFirstAncestorOfClass("Model")
		local humanoid = model and model:FindFirstChildOfClass("Humanoid")
		if model and humanoid and humanoid.Health > 0 and not alreadyHit[humanoid] then
			alreadyHit[humanoid] = true
			humanoid:TakeDamage(stats.damage)
			hitConfirmed:FireAllClients(model, stats.damage)
		end
	end
end

function CombatService.init()
	local attackRequest = Remotes.get(Remotes.Names.AttackRequest)
	local hitConfirmed = Remotes.get(Remotes.Names.HitConfirmed)

	attackRequest.OnServerEvent:Connect(function(player: Player)
		local character = getAliveParts(player)
		if not character then
			return
		end
		local stats = getEquippedStats(character)
		if not stats then
			return
		end

		local now = os.clock()
		if now - (lastAttackTime[player] or 0) < stats.cooldown then
			return
		end
		lastAttackTime[player] = now

		task.delay(stats.windup, resolveHit, player, stats, hitConfirmed)
	end)

	Players.PlayerRemoving:Connect(function(player: Player)
		lastAttackTime[player] = nil
	end)
end

return CombatService
