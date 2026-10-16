--!strict
-- Mô hình 3D của từng vũ khí và cách cầm. Chỉnh số ở đây, không ghi cứng trong code.
-- Model nằm ở ServerStorage.Assets.Weapons (Rojo lấy từ assets/roblox/weapons, xem default.project.json).

export type WeaponModel = {
	modelName: string, -- tên Model trong ServerStorage.Assets.Weapons
	handlePartName: string, -- phần mà bàn tay cầm, sẽ đổi tên thành "Handle"
	gripOffset: Vector3, -- điểm bàn tay nắm, tính trong không gian của phần Handle (studs)
	gripTurnDegrees: number, -- xoay quanh trục lưỡi kiếm để lưỡi sắc hướng ra trước
	gripTiltDegrees: number, -- nghiêng lưỡi kiếm ra trước (âm) hoặc ra sau (dương)
}

local WeaponModelConfig: { [string]: WeaponModel } = {
	-- Khóa trùng tên Tool và khóa trong WeaponConfig.
	Sword = {
		modelName = "StarterLongsword",
		handlePartName = "Grip",
		gripOffset = Vector3.new(0, 0.2, 0),
		gripTurnDegrees = 90,
		gripTiltDegrees = -20,
	},
}

return WeaponModelConfig
