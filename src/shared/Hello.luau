--!strict
-- Module dùng chung giữa server và client. Chỉ để chạy thử.

local Hello = {}

function Hello.start(side: string)
	print("Blind Vow khởi động (shared, gọi từ " .. side .. ")")
end

return Hello
