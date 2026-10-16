--!strict
-- Tư thế khi đã rút vũ khí. Chỉ là hình ảnh, không ảnh hưởng đòn đánh hay sát thương.
--   hold: tay phải cầm kiếm, chạy suốt lúc kiếm trong tay (cả khi đi, nhảy).
--   readyIdle: tư thế thủ cả người (không gồm tay phải) khi đứng yên trên mặt đất.
-- Hai animation điều khiển các khớp khác nhau nên không tranh nhau.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Config = Shared:WaitForChild("Config")
local WeaponConfig = require(Config:WaitForChild("WeaponConfig"))
local WeaponAnimationConfig = require(Config:WaitForChild("WeaponAnimationConfig"))
local AnimationLoader = require(script.Parent:WaitForChild("AnimationLoader"))

local WeaponStance = {}

local player = Players.LocalPlayer

local function isGrounded(humanoid: Humanoid): boolean
	local state = humanoid:GetState()
	return (state == Enum.HumanoidStateType.Running or state == Enum.HumanoidStateType.RunningNoPhysics)
		and humanoid.FloorMaterial ~= Enum.Material.Air
end

local function setPlaying(track: AnimationTrack, shouldPlay: boolean, fadeTime: number)
	if shouldPlay and not track.IsPlaying then
		track:Play(fadeTime)
	elseif not shouldPlay and track.IsPlaying then
		track:Stop(fadeTime)
	end
end

local function runStance(character: Model, tool: Tool)
	local config = WeaponAnimationConfig[tool.Name]
	local stats = WeaponConfig[tool.Name]
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local animator = humanoid and humanoid:FindFirstChildOfClass("Animator")
	if not config or not humanoid or not animator then
		return
	end
	local hold = AnimationLoader.load(animator, config.hold)
	local idle = AnimationLoader.load(animator, config.readyIdle)
	if not hold or not idle then
		return
	end
	hold.Priority = Enum.AnimationPriority.Action
	hold.Looped = true
	idle.Priority = Enum.AnimationPriority.Action
	idle.Looped = true

	-- Trong lúc vung kiếm thì tạm bỏ tư thế thủ.
	local suppressedUntil = 0
	local connections: { RBXScriptConnection } = {}

	table.insert(
		connections,
		tool.Activated:Connect(function()
			suppressedUntil = os.clock() + (if stats then stats.cooldown else 0.5)
		end)
	)

	table.insert(
		connections,
		RunService.Heartbeat:Connect(function()
			local equipped = tool.Parent == character and humanoid.Health > 0
			setPlaying(hold, equipped, config.fadeTime)
			setPlaying(
				idle,
				equipped
					and humanoid.MoveDirection.Magnitude < config.moveThreshold
					and isGrounded(humanoid)
					and os.clock() >= suppressedUntil,
				config.fadeTime
			)
		end)
	)

	local function cleanup()
		for _, connection in connections do
			connection:Disconnect()
		end
		table.clear(connections)
		hold:Stop(config.fadeTime)
		idle:Stop(config.fadeTime)
		task.delay(config.fadeTime, function()
			hold:Destroy()
			idle:Destroy()
		end)
	end

	table.insert(
		connections,
		tool.AncestryChanged:Connect(function()
			if tool.Parent ~= character then
				cleanup()
			end
		end)
	)
	table.insert(connections, humanoid.Died:Connect(cleanup))
end

local function watchCharacter(character: Model)
	local function onChild(child: Instance)
		if child:IsA("Tool") and WeaponAnimationConfig[child.Name] then
			runStance(character, child)
		end
	end
	for _, child in character:GetChildren() do
		onChild(child)
	end
	character.ChildAdded:Connect(onChild)
end

function WeaponStance.init()
	if player.Character then
		watchCharacter(player.Character)
	end
	player.CharacterAdded:Connect(watchCharacter)
end

return WeaponStance
