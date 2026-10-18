--!strict
-- Đeo vỏ kiếm bên hông phải. Khi kiếm chưa rút, chuôi kiếm nằm trong vỏ;
-- khi đã rút (Tool nằm trong nhân vật), chuôi trong vỏ ẩn đi để không thấy hai thanh kiếm.
-- Chạy trên server để người chơi khác cũng nhìn thấy.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local WeaponModelConfig = require(Shared:WaitForChild("Config"):WaitForChild("WeaponModelConfig"))
local WeaponAssets = require(script.Parent:WaitForChild("WeaponAssets"))

local HOLSTER_NAME = "WeaponHolster"
local TOOL_WAIT_SECONDS = 10
local APPEARANCE_WAIT_SECONDS = 5

local WeaponHolster = {}

local function weldTo(anchor: BasePart, part: BasePart, offset: CFrame, parent: Instance)
	WeaponAssets.makeVisualOnly(part)
	part.CFrame = anchor.CFrame * offset
	local weld = Instance.new("Weld")
	weld.Part0 = anchor
	weld.Part1 = part
	weld.C0 = offset
	weld.Parent = part
	part.Parent = parent
end

local function attach(character: Model, tool: Tool, config: WeaponModelConfig.WeaponModel)
	local anchor = character:FindFirstChild(config.holsterPartName)
	local sword = WeaponAssets.findModel(config.modelName)
	local scabbard = WeaponAssets.findModel(config.scabbardModelName)
	if not anchor or not anchor:IsA("BasePart") or not sword or not scabbard then
		warn(`[WeaponHolster] Không gắn được vỏ kiếm cho {character.Name}: thiếu {config.holsterPartName} hoặc model.`)
		return
	end
	local swordGrip = sword:FindFirstChild(config.handlePartName)
	if not swordGrip or not swordGrip:IsA("BasePart") then
		warn(`[WeaponHolster] Model {config.modelName} thiếu phần {config.handlePartName}.`)
		return
	end

	local old = character:FindFirstChild(HOLSTER_NAME)
	if old then
		old:Destroy()
	end

	-- Vị trí tâm chuôi kiếm khi nằm trong vỏ: mũi kiếm chúc xuống và ngả ra sau,
	-- mặt phẳng lưỡi kiếm áp theo hông (lưỡi sắc hướng lên trên và xuống dưới).
	local holsterGrip = CFrame.new(config.holsterGripPosition)
		* CFrame.Angles(math.rad(180 - config.holsterTiltDegrees), 0, 0)
		* CFrame.Angles(0, math.rad(90), 0)

	local holster = Instance.new("Model")
	holster.Name = HOLSTER_NAME

	-- Vỏ kiếm: các phần đã lưu theo tọa độ của tâm chuôi kiếm.
	for _, part in scabbard:GetDescendants() do
		if part:IsA("BasePart") then
			weldTo(anchor, part:Clone(), holsterGrip * part.CFrame, holster)
		end
	end

	-- Chuôi kiếm lộ ra khỏi vỏ.
	local hiltParts: { BasePart } = {}
	for _, partName in config.holsterHiltParts do
		local part = sword:FindFirstChild(partName)
		if part and part:IsA("BasePart") then
			local clone = part:Clone()
			weldTo(anchor, clone, holsterGrip * swordGrip.CFrame:ToObjectSpace(part.CFrame), holster)
			table.insert(hiltParts, clone)
		end
	end

	holster.Parent = character

	local function update()
		local drawn = tool.Parent == character
		for _, part in hiltParts do
			part.Transparency = if drawn then 1 else 0
		end
	end
	local connection = tool.AncestryChanged:Connect(update)
	holster.Destroying:Connect(function()
		connection:Disconnect()
	end)
	update()
end

local function onCharacterAdded(player: Player, character: Model)
	-- CharacterAdded chạy trước khi nhân vật được đặt vào Workspace, và Roblox còn thay các bộ phận
	-- cơ thể khi tải ngoại hình. Chờ cả hai xong rồi mới gắn vỏ, để mối hàn không bị mất.
	local function isCurrent(): boolean
		return player.Character == character
	end
	local deadline = os.clock() + APPEARANCE_WAIT_SECONDS
	while isCurrent() and os.clock() < deadline and (not character.Parent or not player:HasAppearanceLoaded()) do
		task.wait(0.1)
	end
	if not isCurrent() or not character.Parent then
		return
	end

	for toolName, config in WeaponModelConfig do
		-- Tool được phát từ StarterPack vào Backpack ngay sau khi nhân vật xuất hiện.
		local toolDeadline = os.clock() + TOOL_WAIT_SECONDS
		local tool: Instance? = nil
		repeat
			local backpack = player:FindFirstChildOfClass("Backpack")
			tool = (backpack and backpack:FindFirstChild(toolName)) or character:FindFirstChild(toolName)
			if not tool then
				task.wait(0.1)
			end
		until tool or os.clock() > toolDeadline or not isCurrent()
		if tool and tool:IsA("Tool") and isCurrent() then
			local weapon: Tool = tool
			attach(character, weapon, config)
			-- Nếu bộ phận gắn vỏ bị thay (ví dụ đổi ngoại hình), gắn lại.
			character.ChildAdded:Connect(function(child: Instance)
				if child.Name == config.holsterPartName and child:IsA("BasePart") then
					attach(character, weapon, config)
				end
			end)
		elseif isCurrent() then
			warn(`[WeaponHolster] {player.Name} không có Tool {toolName}, không gắn vỏ kiếm.`)
		end
	end
end

function WeaponHolster.init()
	local function onPlayer(player: Player)
		if player.Character then
			task.spawn(onCharacterAdded, player, player.Character)
		end
		player.CharacterAdded:Connect(function(character: Model)
			onCharacterAdded(player, character)
		end)
	end
	for _, player in Players:GetPlayers() do
		onPlayer(player)
	end
	Players.PlayerAdded:Connect(onPlayer)
end

return WeaponHolster
