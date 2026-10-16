# Hướng dẫn cài đặt (cho người mới)

Mục tiêu: code nằm trong kho này, Rojo đẩy code vào Roblox Studio để bạn chạy thử.

## Bạn cần
- Roblox Studio (đã đăng nhập).
- Git (tải ở https://git-scm.com).
- Rojo (bước 1 và 2 bên dưới).

## Bước 1. Cài Rojo (chương trình trên máy)
Cách dễ nhất là qua VS Code:
1. Cài VS Code: https://code.visualstudio.com
2. Mở VS Code, vào mục Extensions (biểu tượng ô vuông bên trái), tìm **Rojo** (tác giả: evaera / Roblox) rồi bấm Install.

Cách khác (dòng lệnh): tải file `rojo` cho Windows ở https://github.com/rojo-rbx/rojo/releases, giải nén và đặt vào thư mục có trong PATH.

## Bước 2. Cài plugin Rojo trong Roblox Studio
1. Mở Roblox Studio, vào tab **Plugins** rồi **Manage Plugins**.
2. Tìm "Rojo" và cài bản chính thức, hoặc mở extension Rojo trong VS Code và chọn "Install Roblox Studio plugin".
3. Khởi động lại Studio nếu cần. Bạn sẽ thấy nút **Rojo** trong tab Plugins.

## Bước 3. Lấy code về máy
Mở Command Prompt (hoặc PowerShell) và chạy:

```
git clone https://github.com/nqvonepiece-beep/Blind-vow-.git
cd Blind-vow-
```

## Bước 4. Chạy Rojo
Trong thư mục `Blind-vow-`, chạy:

```
rojo serve
```

Nếu thấy dòng kiểu "Rojo server listening on port 34872" thì Rojo đã chạy. Đừng đóng cửa sổ này khi đang test.

(Dùng VS Code: bấm nút **Rojo** ở thanh dưới và chọn **Start server**.)

## Bước 5. Kết nối Studio
1. Trong Roblox Studio, tạo một **Baseplate** mới (File, New, Baseplate).
2. Vào tab Plugins, bấm **Rojo**, rồi bấm **Connect** (giữ địa chỉ mặc định `localhost:34872`).
3. Studio sẽ nhận code từ kho. Trong Explorer sẽ có:
   - `ServerScriptService/Server/Main`
   - `StarterPlayer/StarterPlayerScripts/Client/Main`
   - `ReplicatedStorage/Shared/Hello`

## Bước 6. Chạy thử
1. Bấm **Play** (hoặc F5) trong Studio.
2. Mở cửa sổ **Output** (View, Output).
3. Bạn phải thấy hai dòng:
   - `Blind Vow khởi động (server)`
   - `Blind Vow khởi động (client)`

Nếu thấy cả hai, khung dự án đã chạy đúng.

## Khi làm việc hằng ngày
- Mỗi lần lên máy tiệm net: `git pull` để lấy code mới, rồi `rojo serve`, rồi Connect trong Studio.
- Không sửa script trực tiếp trong Studio. Code gốc nằm trong thư mục `src` của kho. Sửa trong Studio sẽ bị ghi đè lần kết nối sau.
- Không lưu file `.rbxl` vào kho (đã được `.gitignore` chặn).

## Gặp lỗi?
- **`rojo` không nhận lệnh:** đóng và mở lại cửa sổ dòng lệnh, hoặc kiểm tra Rojo đã nằm trong PATH.
- **Studio không kết nối được:** kiểm tra `rojo serve` còn chạy, và bật Allow HTTP Requests nếu plugin yêu cầu.
- **Máy tiệm net chặn cài đặt:** nhắn lại cho Claude, chúng ta sẽ tìm cách khác (ví dụ chạy Rojo từ thư mục di động).
