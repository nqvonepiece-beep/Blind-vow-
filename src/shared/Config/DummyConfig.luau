--!strict
-- Thông số hình nộm tập đánh.

local DummyConfig = {
	maxHealth = 100,
	respawnDelay = 3, -- giây trước khi hình nộm mới xuất hiện
	spawnPosition = Vector3.new(0, 3, -15),
	spawnClearRadius = 4, -- chờ người chơi rời vùng này rồi mới hồi sinh, tránh chồng lên nhau
}

return DummyConfig
