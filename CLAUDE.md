# Blind Vow - Luật dự án

## Bối cảnh
- Chủ dự án: Vinny, người mới hoàn toàn, chưa biết lập trình.
- Game Roblox "Blind Vow": RPG hành động thế giới mở, fantasy trung cổ châu Âu pha isekai, combat nhanh và căng, nhân vật chết là mất vĩnh viễn.
- Vinny chỉ test game ở tiệm net khoảng 3 giờ mỗi ngày bằng Roblox Studio và Rojo. Code làm cùng Claude trong kho này.
- Thiết kế game: xem `docs/GDD.md`. Hướng dẫn cài đặt: xem `docs/SETUP.md`.

## Cách giao tiếp
- Nói tiếng Việt với Vinny, giải thích ngắn gọn, dễ hiểu, tránh thuật ngữ khó.
- Code và tên biến viết bằng tiếng Anh. Tài liệu viết bằng tiếng Việt.

## Luật kỹ thuật
- Dùng Luau (ưu tiên `--!strict`).
- Server quyết định mọi kết quả quan trọng: sát thương, parry, cái chết. Không tin dữ liệu từ client.
- Chia module nhỏ, mỗi module một việc.
- Thông số vũ khí, quái, kỹ năng đặt trong file config riêng, không ghi cứng rải rác trong code.
- Lỗi lưu dữ liệu không bao giờ được xóa nhầm nhân vật.

## Quy trình làm việc
- Mỗi việc một commit rõ ràng.
- Làm trên nhánh riêng và mở Pull Request.
- Trước mỗi việc lớn, tóm tắt kế hoạch để Vinny duyệt, chờ Vinny trả lời "ok" rồi mới làm.
- Cuối mỗi nhiệm vụ, nói rõ: (1) cách test trong Studio, (2) việc nào đã kiểm tra thật, (3) việc nào chưa kiểm tra được. Không được nói đã test nếu chưa chạy.

## Bản quyền
- Không sao chép nội dung của game khác.
- Chỉ dùng tài nguyên (hình, âm thanh, mô hình) có bản quyền hợp lệ.

## Bảo mật
- Kho này công khai: không đưa mật khẩu, khóa, token hay thông tin cá nhân vào file.
