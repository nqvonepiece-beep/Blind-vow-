--!strict
-- Mô hình 3D của từng vũ khí, cách cầm và cách đeo bên hông. Chỉnh số ở đây, không ghi cứng trong code.
-- Model nằm ở ServerStorage.Assets.Weapons (Rojo lấy từ assets/roblox/weapons, xem default.project.json).

export type WeaponModel = {
	modelName: string, -- tên Model trong ServerStorage.Assets.Weapons
	handlePartName: string, -- phần mà bàn tay cầm, sẽ đổi tên thành "Handle"
	gripOffset: Vector3, -- điểm bàn tay nắm, tính trong không gian của phần Handle (studs)
	-- Hướng kiếm trong bàn tay phải, tính theo trục bàn tay khi tay buông thẳng:
	-- X = ra ngoài (sang phải), Y = lên (về phía vai), Z = ra sau.
	gripBladeDirection: Vector3, -- hướng mũi kiếm
	gripEdgeDirection: Vector3, -- hướng lưỡi sắc (sẽ được chỉnh cho vuông góc với mũi kiếm)

	-- Đeo bên hông khi chưa rút kiếm
	scabbardModelName: string, -- vỏ kiếm, các phần lưu theo tọa độ của tâm chuôi kiếm
	holsterPartName: string, -- phần cơ thể gắn vỏ kiếm
	holsterGripPosition: Vector3, -- vị trí tâm chuôi kiếm so với phần cơ thể đó (studs)
	holsterTiltDegrees: number, -- góc mũi kiếm ngả ra sau so với phương thẳng đứng
	holsterHiltParts: { string }, -- các phần của kiếm lộ ra ngoài vỏ (ẩn đi khi đã rút kiếm)
}

local WeaponModelConfig: { [string]: WeaponModel } = {
	-- Khóa trùng tên Tool và khóa trong WeaponConfig.
	Sword = {
		modelName = "StarterLongsword",
		handlePartName = "Grip",
		gripOffset = Vector3.new(0, -0.2, 0),
		-- Tư thế thủ: mũi kiếm chĩa ra ngoài là chính, hơi ra sau, chúc xuống gần mặt đất.
		gripBladeDirection = Vector3.new(0.74, -0.63, 0.22),
		gripEdgeDirection = Vector3.new(0.17, -0.14, -0.98),

		scabbardModelName = "StarterLongswordScabbard",
		holsterPartName = "LowerTorso",
		holsterGripPosition = Vector3.new(1.1, 0.63, -0.95),
		holsterTiltDegrees = 50,
		holsterHiltParts = { "Guard", "Grip", "Pommel" },
	},
}

return WeaponModelConfig
