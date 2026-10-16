# Buổi sau làm tiếp từ đâu

Cập nhật: 17/10/2026. Đọc file này đầu mỗi buổi. Claude cũng đọc file này để biết việc đang dở.

## Đang làm

Nhánh **`feat/sword-ready-idle`**, chưa mở Pull Request, chưa gộp vào `main`.

Việc: kiếm đeo bên hông phải, phím **E** rút/tra kiếm, tư thế thủ theo ảnh tham khảo `SwordIdle_01` (tay phải buông thấp cạnh hông, mũi kiếm chĩa ra ngoài và chúc gần sát đất, tay trái co trước người, chân dang và khuỵu).

## Đã kiểm tra thật trong Studio (bản 2)

- Phím E rút và tra kiếm chạy; phím 1 trên thanh công cụ cũng chạy.
- Tư thế thủ gần ảnh tham khảo: kiếm chĩa ra ngoài, mũi cách nền khoảng 0,3 stud.
- Đi, nhảy, M1 vẫn chạy; Dummy mất máu đúng 12 mỗi nhát.

## Chưa kiểm tra (làm đầu buổi sau)

1. **Vỏ kiếm tự gắn vào hông phải khi vào game và sau khi hồi sinh.** Bản 2 bị lỗi không tự gắn; bản 3 đã sửa trong `src/server/Combat/WeaponHolster.luau` nhưng chưa chạy thử.
2. **Núm kiếm không lấn vào hông** khi đứng thủ (bản 3 đổi điểm nắm `gripOffset` trong `WeaponModelConfig`).
3. Vỏ kiếm còn chạm nhẹ tay phải khi buông tay (giới hạn của nhân vật khối R15). Cần Vinny xem có chấp nhận được không.

Cách thử: chạy `rojo serve`, Connect, Play. Chưa rút kiếm thì nhìn hông phải; nhấn E để rút; đứng yên để xem tư thế; nhấn E lần nữa để tra.

## Còn phải làm sau khi thử xong

- **Publish 3 animation** lên tài khoản Roblox (cần Vinny bấm): `SwordHold`, `SwordReadyIdle`, `SwordReach` nằm trong `ReplicatedStorage.Assets.Animations`. Chuột phải từng cái, chọn Save to Roblox, rồi dán ID vào `src/shared/Config/WeaponAnimationConfig.luau`. Chưa publish thì animation **chỉ chạy khi test trong Studio**, không chạy trong game thật.
- Mở Pull Request `feat/sword-ready-idle` vào `main`.
- Sau đó mới làm 4 đòn đánh cơ bản.

## File quan trọng của việc này

| Việc | File |
|---|---|
| Vỏ kiếm (Blender, texture, FBX, model Roblox) | `assets/blender/weapons/StarterLongswordScabbard.blend`, `assets/blender/weapons/textures/starter_longsword_scabbard_*.png`, `assets/roblox/weapons/StarterLongswordScabbard.fbx`, `assets/roblox/weapons/StarterLongswordScabbard.rbxmx` |
| Animation (tạo bằng script) | `tools/animations/Build-SwordAnimations.ps1` tạo ra `assets/roblox/animations/*.rbxmx` |
| Đeo vỏ bên hông (server) | `src/server/Combat/WeaponHolster.luau` |
| Rút/tra bằng E (client) | `src/client/WeaponDrawController.luau` |
| Tư thế cầm và thủ (client) | `src/client/WeaponStance.luau`, `src/client/AnimationLoader.luau` |
| Số liệu chỉnh tay | `src/shared/Config/WeaponModelConfig.luau`, `WeaponAnimationConfig.luau`, `InputConfig.luau` |

Sửa góc tay chân của tư thế: đổi số trong `tools/animations/Build-SwordAnimations.ps1`, rồi chạy lại:

```
powershell -ExecutionPolicy Bypass -File tools/animations/Build-SwordAnimations.ps1
```

## Nếu buổi sau cần Claude dùng Blender

Máy tiệm net mới sẽ không còn cài đặt Blender MCP. Chỉ cần khi phải sửa mô hình (kiếm, vỏ kiếm). Nhờ Claude cài lại, gồm:

1. Cài Blender và `uv` (chứa lệnh `uvx`).
2. Cài add-on: `uvx mcp-for-blender install-addon`, bật add-on trong Blender (Preferences → Add-ons), bấm Start MCP Server.
3. Thêm server MCP tên `blender` cho Claude Code với lệnh `uvx mcp-for-blender`, rồi mở phiên Claude mới.

Nếu cần Claude tự thao tác trong Roblox Studio: bật **Computer use** trong Settings của app Claude, rồi mở phiên mới.
