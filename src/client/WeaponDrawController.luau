--!strict
-- Rút và tra kiếm bằng phím (mặc định E, xem InputConfig).
-- Tay phải với xuống chuôi kiếm ở hông, đúng lúc tay chạm chuôi thì kiếm chuyển giữa vỏ và tay.
-- Rút = cầm Tool, tra = cất Tool vào Backpack; vỏ kiếm bên hông do server (WeaponHolster) hiển thị.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Config = Shared:WaitForChild("Config")
local InputConfig = require(Config:WaitForChild("InputConfig"))
local WeaponAnimationConfig = require(Config:WaitForChild("WeaponAnimationConfig"))
local AnimationLoader = require(script.Parent:WaitForChild("AnimationLoader"))

local WeaponDrawController = {}

local player = Players.LocalPlayer
local busy = false
local drawTracks: { [Animator]: AnimationTrack } = {}

-- Vũ khí có animation: đang cầm thì trả về Tool trong nhân vật, chưa cầm thì Tool trong Backpack.
local function findWeapon(character: Model): Tool?
	for _, container in { character, player:FindFirstChildOfClass("Backpack") } do
		if container then
			for _, child in container:GetChildren() do
				if child:IsA("Tool") and WeaponAnimationConfig[child.Name] then
					return child
				end
			end
		end
	end
	return nil
end

local function toggleWeapon()
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if busy or not character or not humanoid or humanoid.Health <= 0 then
		return
	end
	local tool = findWeapon(character)
	if not tool then
		return
	end
	local config = WeaponAnimationConfig[tool.Name]
	local drawing = tool.Parent ~= character

	busy = true
	local animator = humanoid:FindFirstChildOfClass("Animator")
	local track = animator and drawTracks[animator]
	if animator and not track then
		track = AnimationLoader.load(animator, config.draw)
		if track then
			track.Priority = Enum.AnimationPriority.Action2
			drawTracks[animator] = track
		end
	end
	if track then
		track:Play(0.1)
	end

	task.wait(config.drawSwapTime)
	if humanoid.Health > 0 and tool.Parent then
		if drawing then
			humanoid:EquipTool(tool)
		else
			humanoid:UnequipTools()
		end
	end

	task.wait(math.max(0, config.drawDuration - config.drawSwapTime))
	if track then
		track:Stop(config.fadeTime)
	end
	busy = false
end

function WeaponDrawController.init()
	UserInputService.InputBegan:Connect(function(input: InputObject, gameProcessed: boolean)
		if not gameProcessed and input.KeyCode == InputConfig.toggleWeapon then
			task.spawn(toggleWeapon)
		end
	end)
	player.CharacterAdded:Connect(function()
		table.clear(drawTracks)
		busy = false
	end)
end

return WeaponDrawController
