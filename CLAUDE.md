# Blind Vow - Luật dự án

File này được đọc tự động mỗi lần mở phiên. Thiết kế đầy đủ nằm trong `docs/GDD.md`, hướng dẫn cài đặt trong `docs/SETUP.md`.

## 1. Về người dùng và cách làm việc

- Tên: Vinny. Người đi làm, làm game như sở thích, **chưa có kinh nghiệm lập trình, animation hay VFX**. Chỉ biết sơ về Roblox Studio và Blender.
- **Giao tiếp bằng tiếng Việt**, giải thích ngắn gọn, dễ hiểu, như đang dạy người mới. Code và tên biến viết bằng tiếng Anh; tài liệu viết bằng tiếng Việt.
- Vinny không có máy tính riêng. Thuê máy tiệm net khoảng 3 giờ mỗi ngày để mở Roblox Studio, cài Rojo và chơi thử. Mọi thứ phải nằm trong kho GitHub, không lưu gì trên máy tiệm net.
- Vinny cung cấp ý tưởng, ảnh và video tham chiếu. Phần còn lại (code, hệ thống, cấu hình, UI bằng code, VFX bằng code) giao cho Claude Code.
- Vinny là người quyết định cuối cùng về hướng sáng tạo.

### Luật làm việc
1. **Tự động làm theo lộ trình** trong `docs/GDD.md`, không cần chờ "ok" cho từng bước. Chỉ hỏi Vinny khi cần quyết định sáng tạo (cốt truyện, tên, phong cách) hoặc việc khó hoàn tác. Báo cáo ngắn gọn, bỏ các bước không quan trọng để tiết kiệm token.
2. Mỗi nhiệm vụ nhỏ, một commit rõ ràng, làm trên nhánh riêng, mở Pull Request. Vinny xác nhận trước khi gộp vào `main`. Rojo đọc từ thư mục trên máy, nên có thể test ngay trên nhánh.
3. Cuối mỗi nhiệm vụ nói rõ: cách test trong Studio, việc nào đã kiểm tra thật, việc nào chưa kiểm tra được. **Không nói đã test nếu chưa chạy.**
4. Khi có lỗi, hướng dẫn Vinny dán nguyên văn thông báo lỗi từ cửa sổ Output của Studio.
5. Server quyết định các kết quả quan trọng (sát thương, parry, cái chết). Không tin dữ liệu từ client.
6. Chia module nhỏ. Thông số vũ khí, quái, kỹ năng đặt trong file config riêng, không ghi cứng rải rác.
7. Chỉ dùng tài nguyên có bản quyền hợp lệ. Không sao chép nội dung của game khác (Deepwoken, Rune Slayer...), chỉ lấy cảm hứng.
8. Ưu tiên một bản nhỏ nhưng chạy được hơn là nhiều tính năng dở dang. Không để hàm trống rồi nói là hoàn thành.

## 2. Tóm tắt game

- **Blind Vow**: RPG hành động thế giới mở trên Roblox, fantasy trung cổ châu Âu pha yếu tố isekai.
- Combat nhanh và căng kiểu Deepwoken: parry, block, né, stamina, posture.
- Chết vĩnh viễn. Server quyết định cái chết. Lỗi lưu dữ liệu tạm thời không bao giờ được xóa nhầm nhân vật.
- Chơi một mình hoặc chơi nhóm.
- Prototype đầu tiên: chỉ Human + Warrior, một căn phòng, một thanh kiếm, một con quái.

## 3. Kỹ thuật

- Dùng Luau, ưu tiên `--!strict`.
- Cấu trúc Rojo: `src/server`, `src/client`, `src/shared` (xem `default.project.json`).

## 4. Bảo mật

- Kho này công khai: không đưa mật khẩu, khóa, token hay thông tin cá nhân vào file.
