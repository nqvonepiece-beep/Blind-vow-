--!strict
-- Thông số vũ khí. Chỉnh số ở đây, không ghi cứng trong code.

export type WeaponStats = {
	damage: number, -- sát thương mỗi đòn
	cooldown: number, -- giây giữa hai đòn
	windup: number, -- giây báo hiệu trước khi gây sát thương
	hitboxSize: Vector3, -- kích thước vùng trúng đòn (studs)
	hitboxOffset: number, -- khoảng cách vùng trúng đòn trước mặt nhân vật
}

local WeaponConfig: { [string]: WeaponStats } = {
	Sword = {
		damage = 12,
		cooldown = 0.6,
		windup = 0.15,
		hitboxSize = Vector3.new(5, 5, 6),
		hitboxOffset = 3.5,
	},
}

return WeaponConfig
