--!strict
-- Animation của từng vũ khí. Chỉnh số ở đây, không ghi cứng trong code.
-- File animation nằm ở ReplicatedStorage.Assets.Animations (Rojo lấy từ assets/roblox/animations,
-- tạo bằng tools/animations/Build-SwordAnimations.ps1).

export type AnimationRef = {
	name: string, -- tên KeyframeSequence trong ReplicatedStorage.Assets.Animations
	-- ID sau khi publish animation lên Roblox, dạng "rbxassetid://123".
	-- Để trống: chỉ chạy được khi test trong Studio (Studio tự tạo ID tạm từ KeyframeSequence).
	id: string,
}

export type WeaponAnimations = {
	hold: AnimationRef, -- tay phải cầm kiếm (luôn chạy khi đã rút kiếm)
	readyIdle: AnimationRef, -- tư thế thủ cả người khi đứng yên (không gồm tay phải)
	draw: AnimationRef, -- với tay xuống chuôi kiếm ở hông, dùng cho cả rút và tra kiếm
	drawSwapTime: number, -- giây sau khi bắt đầu với tay thì kiếm chuyển giữa vỏ và tay
	drawDuration: number, -- tổng thời gian rút hoặc tra kiếm
	fadeTime: number, -- giây chuyển mượt khi bắt đầu hoặc dừng tư thế
	moveThreshold: number, -- tốc độ di chuyển (MoveDirection) coi như đang đứng yên
}

local WeaponAnimationConfig: { [string]: WeaponAnimations } = {
	-- Khóa trùng tên Tool và khóa trong WeaponConfig.
	Sword = {
		hold = { name = "SwordHold", id = "" },
		readyIdle = { name = "SwordReadyIdle", id = "" },
		draw = { name = "SwordReach", id = "" },
		drawSwapTime = 0.3,
		drawDuration = 0.5,
		fadeTime = 0.25,
		moveThreshold = 0.05,
	},
}

return WeaponAnimationConfig
