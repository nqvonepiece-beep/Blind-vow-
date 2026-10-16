--!strict
-- Hiệu ứng khi server xác nhận trúng đòn: nháy sáng và hiện số sát thương.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local Remotes = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Remotes"))

local FLASH_TIME = 0.15
local NUMBER_TIME = 0.8

local HitFeedback = {}

local function flash(model: Model)
	local highlight = Instance.new("Highlight")
	highlight.FillColor = Color3.new(1, 1, 1)
	highlight.FillTransparency = 0.3
	highlight.OutlineTransparency = 1
	highlight.Parent = model
	task.delay(FLASH_TIME, function()
		highlight:Destroy()
	end)
end

local function showDamage(model: Model, damage: number)
	local adornee = model.PrimaryPart or model:FindFirstChildWhichIsA("BasePart")
	if not adornee then
		return
	end

	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.fromOffset(80, 30)
	gui.StudsOffset = Vector3.new(math.random(-10, 10) / 10, 3, 0)
	gui.AlwaysOnTop = true
	gui.Adornee = adornee

	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Text = tostring(damage)
	label.TextColor3 = Color3.fromRGB(255, 220, 80)
	label.TextStrokeTransparency = 0
	label.TextScaled = true
	label.Font = Enum.Font.GothamBold
	label.Parent = gui

	gui.Parent = adornee

	local info = TweenInfo.new(NUMBER_TIME)
	TweenService:Create(gui, info, { StudsOffset = gui.StudsOffset + Vector3.new(0, 1.5, 0) }):Play()
	TweenService:Create(label, info, { TextTransparency = 1, TextStrokeTransparency = 1 }):Play()
	task.delay(NUMBER_TIME, function()
		gui:Destroy()
	end)
end

function HitFeedback.init()
	local hitConfirmed = Remotes.get(Remotes.Names.HitConfirmed)
	hitConfirmed.OnClientEvent:Connect(function(model: Model, damage: number)
		if typeof(model) ~= "Instance" or not model:IsA("Model") then
			return
		end
		flash(model)
		showDamage(model, damage)
	end)
end

return HitFeedback
