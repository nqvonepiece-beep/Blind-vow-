# Bộ animation kiếm: thủ + 4 đòn M1

Cập nhật: 18/10/2026. Trạng thái: **đã tạo trong Blender và xuất file, CHƯA nhập vào Roblox Studio, CHƯA publish, CHƯA gắn vào code combat.**

## 1. Video tham khảo: những gì đã quan sát thật

Nguồn: video Deepwoken PvP Vinny gửi (12,7 giây, 576x1024, 30 khung/giây). Chỉ học nhịp và cách cơ thể chuyển động, không sao chép gì.

Hạn chế: nhân vật nhỏ, nhiều hiệu ứng (lửa, băng) che khuất từ khoảng 5,0 đến 6,5 giây, 8,0 đến 9,0 giây và 10,3 đến 12,0 giây. Video là đánh PvP có parry và kỹ năng xen kẽ, **không có đoạn nào là một chuỗi 4 đòn M1 liền mạch**. Thứ tự 4 đòn dưới đây là thiết kế dựa trên các nhát chém nhìn thấy, không phải chép một chuỗi có sẵn.

| Thời điểm trong video | Quan sát |
| --- | --- |
| 1,47 đến 1,80 giây | Kiếm dựng đứng cạnh vai phải, rồi chém chéo từ trên-phải xuống dưới-trái. Kết thúc với kiếm chĩa sang trái, thấp, tay vắt qua người. |
| 2,10 đến 2,30 giây | Hạ thấp người, áp sát, kiếm ở dưới bên trái. |
| 2,43 đến 2,83 giây | Chém trái tay ngang hông từ trái sang phải. Kết thúc kiếm bên phải, mũi chĩa ra ngoài, thân xoay phải, chân dang rộng. |
| 2,97 và 3,40 giây | Kiếm lại được giương đứng cạnh vai phải, chân trụ rộng: tư thế chuẩn bị cho nhát chéo tiếp theo. |
| 3,67 đến 3,87 giây | Nhát chéo xuống thứ hai, kết thúc kiếm nằm ngang bên trái ngang hông. |
| 4,20 đến 4,40 giây | Nhát trái tay quét về bên phải, thấp. |
| 9,95 đến 10,25 giây | Một nhát quét rộng, cao (ngang vai) từ trái sang phải, vệt chém lớn. |

Nhịp: bản thân nhát chém chỉ khoảng 0,10 đến 0,15 giây. Cứ 0,4 đến 0,5 giây có một nhát mới. Đòn xen kẽ thuận tay rồi trái tay, điểm kết thúc của nhát này là điểm bắt đầu của nhát sau. Chân ít bước, chủ yếu khuỵu gối, dồn trọng tâm và xoay hông, ngực.

## 2. Các animation đã tạo

Rig R15 (16 khớp, tên khớp giống Roblox), 30 khung/giây.

| Tên | Khung | Thời lượng | Lặp | Priority | Marker | Mô tả |
| --- | --- | --- | --- | --- | --- | --- |
| `Sword_CombatIdle` | 0 đến 96 | 3,2 giây | Có | Action | (không có) | Tư thế thủ đã thử trong Studio (`SwordHold` + `SwordReadyIdle` của nhánh `feat/sword-ready-idle`) gộp thành một animation cả người, giữ nguyên số góc, có nhịp thở. |
| `Sword_M1_01` | 0 đến 18 | 0,6 giây | Không | Action2 | `Hit` khung 5 (0,167 giây), `ComboWindow` khung 10 | Từ thế thủ giương kiếm đứng cạnh vai phải, chém chéo xuống trái. |
| `Sword_M1_02` | 0 đến 18 | 0,6 giây | Không | Action2 | `Hit` khung 5, `ComboWindow` khung 10 | Chém trái tay ngang hông, trái sang phải. Tay trái vươn ra giữ thăng bằng. |
| `Sword_M1_03` | 0 đến 18 | 0,6 giây | Không | Action2 | `Hit` khung 5, `ComboWindow` khung 10 | Giương cao hơn đòn 1 rồi chém chéo dốc (khoảng 62°), người đổ thấp và nghiêng về trước nhiều hơn. |
| `Sword_M1_04` | 0 đến 27 | 0,9 giây | Không | Action2 | `Hit` khung 6 (0,2 giây), `Recover` khung 15 | Đòn kết: chân trái bước lên (khung 1 đến 5), quét rộng ngang vai trái sang phải, giữ thế, bước về (khung 19 đến 24), hạ kiếm về thế thủ. |

Nối chuỗi: khung cuối của mỗi đòn trùng khít khung đầu của đòn sau (lệch 0°). Đòn 4 kết thúc đúng tư thế thủ.

Thời gian khớp với server hiện tại (`WeaponConfig.Sword`): `windup` 0,15 giây gần với marker `Hit` 0,167 giây; `cooldown` 0,6 giây bằng độ dài đòn 1 đến 3. Không đổi gì trong hệ thống combat.

Kiếm: dùng nguyên mô hình `StarterLongsword` và đúng cách cầm `gripBladeDirection` / `gripEdgeDirection` / `gripOffset` trong `WeaponModelConfig` (nhánh `feat/sword-ready-idle`). Animation chỉ xoay khớp tay, kiếm vẫn gắn bằng Tool.Grip như cũ, hitbox và sát thương không đổi.

## 3. File

| File | Là gì |
| --- | --- |
| `assets/blender/animations/SwordCombat.blend` | File Blender sửa được: rig `BV_R15_Rig`, 5 action, kiếm gắn tay phải, khối cơ thể và sàn để xem thử. |
| `assets/roblox/animations_fbx/Sword_*.fbx` | FBX từng animation (chỉ khung xương R15, tư thế gốc R15, 1 đơn vị = 1 stud, Y lên, -Z trước). Để ngoài thư mục Rojo đồng bộ. |
| `assets/roblox/animations/Sword_*.rbxmx` | KeyframeSequence cho Roblox, cùng định dạng với `SwordReadyIdle.rbxmx` đã chạy trong Studio. Rojo đồng bộ vào `ReplicatedStorage.Assets.Animations`. |
| `tools/animations/blender/*.py` | Công cụ tạo lại toàn bộ. Tư thế khóa nằm ở `bv_poses.py`. |
| `docs/animations/sword_combat_report.json` | Kết quả kiểm tra tự động. |

Tạo lại tất cả (ở thư mục gốc kho, cần Blender 5.2 hoặc `pip install bpy==5.2.2`):

```
blender --background --python tools/animations/blender/bv_sword_combat.py -- --repo .
blender --background --python tools/animations/blender/bv_verify.py -- --repo .
```

File `StarterLongsword.blend` gốc không bị sửa: kiếm được chép (append) vào file mới, texture trỏ về `assets/blender/weapons/textures`.

## 4. Đã kiểm tra thật và chưa kiểm tra

Đã kiểm tra (chạy thật trong Blender 5.2.2, không phải Blender MCP):
- Tư thế thủ dựng lại đúng số góc đã thử trong Studio (lệch 0°), hai bàn chân chạm đất (lệch tối đa 0,03 stud trên rig xấp xỉ).
- Chân không trượt khi đang chạm đất: xê dịch tối đa 0,007 stud mỗi khung (sai số làm tròn, mắt không thấy). Đòn 4 chỉ dời chân khi đã nhấc lên.
- Lưỡi kiếm không xuyên qua thân, đầu, chân hay tay trái ở bất kỳ khung nào. Mũi kiếm luôn cao hơn mặt đất (thấp nhất 0,10 stud ở thế thủ, 0,12 stud khi đánh).
- Khuỷu tay và đầu gối trong giới hạn. Cổ tay phải gập tối đa khoảng 16°.
- Đã xem hình render từng khung từ 3 góc (sau lưng, trước mặt, ngang) và đường đi của mũi kiếm.
- File `.blend`, FBX (nhập lại vào Blender) và `.rbxmx` (đọc lại XML) chứa đúng cùng một chuyển động: lệch 0,0000°.

Chưa kiểm tra:
- **Chưa nhập vào Roblox Studio, chưa chạy trong game, chưa publish, chưa có Animation ID.** Không có ID nào trong dự án là thật cho các animation này.
- Kích thước rig trong Blender là xấp xỉ R15 khối. Trong Studio, vị trí mũi kiếm có thể lệch vài phần mười stud, đặc biệt với avatar có tỉ lệ khác (Rthro).
- Đường FBX vào Animation Editor (Import, From FBX Animation) chưa thử. Đường `.rbxmx` là đường đã có tiền lệ chạy được trong dự án.

## 5. Bước còn lại trong Studio (ít nhất)

1. Đưa các file trên vào kho, trên một nhánh mới dựa trên `feat/sword-ready-idle` (cần Vinny đồng ý). `git pull` ở máy tiệm net.
2. Chạy `rojo serve` + Connect, hoặc nếu plugin lỗi: `.\rojo.exe build default.project.json -o BlindVow.rbxl` rồi mở file.
3. Trong Explorer, kiểm tra `ReplicatedStorage › Assets › Animations` có 5 mục `Sword_*`.
4. Xem thử từng animation trên một rig R15 (tab Avatar, Rig Builder, R15, Block). Cách FBX: chọn rig, mở Animation Editor, Import, From FBX Animation, chọn `assets/roblox/animations_fbx/Sword_M1_01.fbx`.
5. Publish: chuột phải từng `Sword_*`, chọn **Save to Roblox**, chép ID vào config (giống hướng dẫn trong `docs/NEXT_SESSION.md`).
6. Sau khi Vinny thấy ổn mới gắn vào M1: client chọn đòn theo số thứ tự combo khi `Tool.Activated`, chỉ để hiển thị. Server vẫn quyết định trúng và sát thương. Khi nhảy, bị choáng hoặc cất kiếm thì `Stop(0.15)`.

## 6. Cần Vinny quyết định

- Nhánh: công việc này cần nhánh `feat/sword-ready-idle` (tư thế thủ, thư mục animation trong Rojo, AnimationLoader). Gộp nhánh đó vào `main` trước, hay làm nhánh mới dựa trên nó?
- Đòn 4 dài 0,9 giây nhưng `cooldown` hiện là 0,6 giây cho mọi đòn: có muốn đòn kết có thời gian hồi riêng không (là thay đổi gameplay, chưa làm)?
