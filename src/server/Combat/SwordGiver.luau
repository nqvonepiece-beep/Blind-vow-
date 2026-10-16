--!strict
-- Tạo thanh kiếm tạm (khối đơn giản) và phát cho người chơi.
-- Sau này thay bằng mô hình kiếm có bản quyền hợp lệ.

local Players = game:GetService("Players")
local StarterPack = game:GetService("StarterPack")

local SWORD_NAME = "Sword"

local SwordGiver = {}

local function buildSword(): Tool
	local tool = Instance.new("Tool")
	tool.Name = SWORD_NAME
	tool.RequiresHandle = true
	tool.CanBeDropped = false
	tool.Grip = CFrame.new(0, 0, -1.6)

	local handle = Instance.new("Part")
	handle.Name = "Handle"
	handle.Size = Vector3.new(0.25, 0.25, 4)
	handle.Color = Color3.fromRGB(190, 190, 200)
	handle.Material = Enum.Material.Metal
	handle.CanCollide = false
	handle.Massless = true
	handle.Parent = tool

	return tool
end

function SwordGiver.init()
	local template = buildSword()
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
