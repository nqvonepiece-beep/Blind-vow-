# Blind Vow

RPG hành động thế giới mở trên Roblox, fantasy trung cổ châu Âu pha yếu tố isekai. Combat nhanh và căng (parry, block, né, stamina, posture), chết vĩnh viễn, chơi một mình hoặc chơi nhóm.

Dự án đang ở giai đoạn prototype đầu tiên: Human + Warrior, một căn phòng, một thanh kiếm, một con quái.

## Tài liệu

- [Hướng dẫn cài đặt và làm việc hằng ngày](docs/SETUP.md): cài Git và Rojo, chạy thử trong Studio, sao lưu, bảo mật cuối buổi ở máy tiệm net.
- [Buổi sau làm tiếp từ đâu](docs/NEXT_SESSION.md): việc đang dở, cái gì đã và chưa kiểm tra.
- [Tài liệu thiết kế (GDD)](docs/GDD.md): cốt truyện, chủng tộc, class, combat, lộ trình.
- [Luật dự án](CLAUDE.md): cách làm việc và quy tắc kỹ thuật.

## Cấu trúc

Code viết bằng Luau, đồng bộ vào Roblox Studio bằng [Rojo](https://rojo.space) 7.7.1 (xem `default.project.json`):

- `src/server`: code chạy trên server (`ServerScriptService`)
- `src/client`: code chạy trên máy người chơi (`StarterPlayerScripts`)
- `src/shared`: code và cấu hình dùng chung (`ReplicatedStorage`)
