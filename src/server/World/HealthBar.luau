--!strict
-- Thanh máu nổi trên đầu một Humanoid.

local HealthBar = {}

function HealthBar.attach(humanoid: Humanoid, adornee: BasePart)
	local gui = Instance.new("BillboardGui")
	gui.Name = "HealthBar"
	gui.Size = UDim2.fromOffset(120, 12)
	gui.StudsOffset = Vector3.new(0, 2, 0)
	gui.AlwaysOnTop = true
	gui.Adornee = adornee

	local background = Instance.new("Frame")
	background.Size = UDim2.fromScale(1, 1)
	background.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
	background.BorderSizePixel = 0
	background.Parent = gui

	local fill = Instance.new("Frame")
	fill.BackgroundColor3 = Color3.fromRGB(200, 40, 40)
	fill.BorderSizePixel = 0
	fill.Parent = background

	local function update()
		local ratio = if humanoid.MaxHealth > 0 then humanoid.Health / humanoid.MaxHealth else 0
		fill.Size = UDim2.fromScale(math.clamp(ratio, 0, 1), 1)
	end

	humanoid.HealthChanged:Connect(update)
	update()

	gui.Parent = adornee
end

return HealthBar
