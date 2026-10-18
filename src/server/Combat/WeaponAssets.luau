--!strict
-- Tìm mô hình vũ khí trong ServerStorage.Assets.Weapons và chuẩn bị các phần để gắn lên nhân vật.

local ServerStorage = game:GetService("ServerStorage")

local WeaponAssets = {}

function WeaponAssets.findModel(modelName: string): Model?
	local assets = ServerStorage:FindFirstChild("Assets")
	local weapons = assets and assets:FindFirstChild("Weapons")
	local model = weapons and weapons:FindFirstChild(modelName)
	if model and model:IsA("Model") then
		return model
	end
	warn(`[WeaponAssets] Không tìm thấy ServerStorage.Assets.Weapons.{modelName}. Kiểm tra Rojo đã sync assets/roblox/weapons chưa.`)
	return nil
end

-- Phần chỉ để nhìn: không va chạm, không nặng, không neo, để không cản di chuyển.
-- Sát thương do server tính bằng hitbox riêng (CombatService), không dùng va chạm của vũ khí.
function WeaponAssets.makeVisualOnly(part: BasePart)
	part.Anchored = false
	part.CanCollide = false
	part.CanTouch = false
	part.CanQuery = false
	part.Massless = true
end

return WeaponAssets
