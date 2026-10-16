# Hướng dẫn cài đặt (cho người mới, dùng ở máy tiệm net)

Nguyên tắc: **mọi thứ nằm trong kho GitHub**. Máy tiệm net có thể bị xóa sau mỗi buổi, nên mỗi lần bạn cài lại từ đầu. Phần lớn các bước chỉ mất vài phút.

Mục tiêu: code nằm trong kho này, Rojo đẩy code vào Roblox Studio để bạn chạy thử.

## Checklist khi mở máy (mỗi buổi)

1. Mở Roblox Studio, đăng nhập.
2. Cài Git và Rojo nếu máy chưa có (xem bên dưới).
3. Lấy code: `git clone` (lần đầu trên máy) hoặc `git pull` (nếu thư mục còn).
4. Chạy `rojo serve`, rồi Connect trong Studio.
5. Bấm Play và xem cửa sổ Output.

## Checklist trước khi rời máy

1. **Không lưu gì chỉ trên máy.** File `.rbxl` bị `.gitignore` chặn, đừng cố lưu nó vào kho.
2. Nếu bạn có sửa file trong kho, nhờ Claude commit và đẩy lên GitHub trước khi đứng dậy.
3. Đăng xuất Roblox, GitHub và các tài khoản khác trên máy tiệm net.
4. Không để mật khẩu hay token lại trên máy.

## Bước 1. Cài Git

Tải ở https://git-scm.com, cài với các lựa chọn mặc định. Mở lại cửa sổ dòng lệnh sau khi cài.

Nếu máy không cho cài chương trình: nhắn Claude, chúng ta sẽ tìm cách khác (ví dụ tải kho dạng file ZIP từ nút **Code → Download ZIP** trên GitHub).

## Bước 2. Cài Rojo (chương trình trên máy)

1. Vào https://github.com/rojo-rbx/rojo/releases
2. Tải file dành cho Windows (tên có `windows`), giải nén.
3. Đặt file `rojo.exe` vào thư mục dự án `Blind-vow-` (hoặc chỗ bạn nhớ được) và chạy từ đó, ví dụ `.\rojo.exe serve`. Cách này không cần quyền quản trị.

Lưu ý: không đưa `rojo.exe` vào kho (đã tải lại mỗi buổi là đủ).

## Bước 3. Cài plugin Rojo trong Roblox Studio

1. Mở Roblox Studio, vào tab **Plugins** rồi **Manage Plugins**.
2. Tìm "Rojo" và cài bản chính thức. Bản plugin nên cùng phiên bản (hoặc gần nhất) với `rojo.exe` đã tải.
3. Khởi động lại Studio nếu cần. Bạn sẽ thấy nút **Rojo** trong tab Plugins.

## Bước 4. Lấy code về máy

Mở Command Prompt (hoặc PowerShell) và chạy:

```
git clone https://github.com/nqvonepiece-beep/Blind-vow-.git
cd Blind-vow-
```

Những buổi sau, nếu thư mục còn trên máy, chỉ cần `git pull`.

## Bước 5. Chạy Rojo

Trong thư mục `Blind-vow-`, chạy:

```
rojo serve
```

(Nếu bạn để `rojo.exe` trong thư mục dự án, chạy `.\rojo.exe serve`.)

Nếu thấy dòng kiểu "Rojo server listening on port 34872" thì Rojo đã chạy. Đừng đóng cửa sổ này khi đang test.

## Bước 6. Kết nối Studio

1. Trong Roblox Studio, tạo một **Baseplate** mới (File, New, Baseplate).
2. Vào tab Plugins, bấm **Rojo**, rồi bấm **Connect** (giữ địa chỉ mặc định `localhost:34872`).
3. Studio sẽ nhận code từ kho. Trong Explorer sẽ có:
   - `ServerScriptService/Server/Main`
   - `StarterPlayer/StarterPlayerScripts/Client/Main`
   - `ReplicatedStorage/Shared/Hello`

## Bước 7. Chạy thử

1. Bấm **Play** (hoặc F5) trong Studio.
2. Mở cửa sổ **Output** (View, Output).
3. Bạn phải thấy hai dòng:
   - `Blind Vow khởi động (server)`
   - `Blind Vow khởi động (client)`

Nếu thấy cả hai, khung dự án đã chạy đúng.

## Khi làm việc hằng ngày

- Không sửa script trực tiếp trong Studio. Code gốc nằm trong thư mục `src` của kho. Sửa trong Studio sẽ bị ghi đè lần kết nối sau.
- Không lưu file `.rbxl` vào kho (đã được `.gitignore` chặn).

## Gặp lỗi?

**Hãy dán nguyên văn thông báo lỗi từ cửa sổ Output của Studio** (hoặc từ cửa sổ dòng lệnh) cho Claude, đừng tóm tắt.

- **`rojo` không nhận lệnh:** đóng và mở lại cửa sổ dòng lệnh, hoặc chạy bằng `.\rojo.exe` trong đúng thư mục chứa nó.
- **Studio không kết nối được:** kiểm tra `rojo serve` còn chạy, và bật Allow HTTP Requests nếu plugin yêu cầu.
- **Máy tiệm net chặn cài đặt hoặc chặn mạng:** nhắn lại cho Claude để tìm cách khác.
