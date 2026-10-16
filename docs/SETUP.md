# Hướng dẫn cài đặt (cho người mới, dùng ở máy tiệm net)

Nguyên tắc: **mọi thứ nằm trong kho GitHub**. Máy tiệm net có thể bị xóa sau mỗi buổi, nên mỗi lần bạn cài lại từ đầu. Phần lớn các bước chỉ mất vài phút.

Mục tiêu: code nằm trong kho này, Rojo đẩy code vào Roblox Studio để bạn chạy thử.

Các lệnh bên dưới gõ trong **PowerShell** hoặc **Command Prompt**, trừ khi ghi khác.

## Checklist khi mở máy (mỗi buổi)

1. Mở Roblox Studio, đăng nhập.
2. Cài Git và Rojo nếu máy chưa có, rồi kiểm tra phiên bản (Bước 1, Bước 2).
3. Lấy code: `git clone` (lần đầu trên máy) hoặc `git pull` (nếu thư mục còn) (Bước 4).
4. Đặt tên và email Git cho thư mục dự án (Bước 5).
5. Chạy `rojo serve`, rồi Connect trong Studio (Bước 6, Bước 7).
6. Bấm Play và xem cửa sổ Output (Bước 8).

## Checklist trước khi rời máy

Làm **đúng thứ tự**. Chi tiết ở mục [Sao lưu dự án](#sao-lưu-dự-án) và [Bảo mật cuối buổi](#bảo-mật-cuối-buổi).

1. Kiểm tra mọi thay đổi đã được đẩy lên GitHub.
2. Tắt `rojo serve` và Roblox Studio.
3. Đăng xuất GitHub CLI (`gh auth logout`).
4. Xóa mật khẩu GitHub mà Git đã lưu trong Windows.
5. Đăng xuất Roblox, GitHub, Claude và mọi tài khoản trên trình duyệt và ứng dụng.
6. Kiểm tra lần cuối.

## Bước 1. Cài Git

Tải ở https://git-scm.com, cài với các lựa chọn mặc định. Mở lại cửa sổ dòng lệnh sau khi cài.

Kiểm tra:

```
git --version
```

Phải thấy dòng kiểu `git version 2.xx`.

Nếu máy không cho cài chương trình: nhắn Claude, chúng ta sẽ tìm cách khác (ví dụ tải kho dạng file ZIP từ nút **Code → Download ZIP** trên GitHub).

## Bước 2. Cài Rojo CLI (chương trình trên máy)

Dự án dùng **Rojo 7.7.1**. Dùng đúng phiên bản này để khớp với plugin trong Studio.

**Kiểm tra trước, có thể máy đã có sẵn:**

```
rojo --version
```

- Thấy `Rojo 7.7.1`: bỏ qua phần cài, sang Bước 3.
- Thấy phiên bản khác, hoặc báo không nhận lệnh: cài theo cách dưới đây.

**Cách cài (không cần quyền quản trị):**

1. Vào https://github.com/rojo-rbx/rojo/releases/tag/v7.7.1
2. Ở mục **Assets**, tải file `rojo-7.7.1-windows-x86_64.zip`, giải nén.
3. Chép file `rojo.exe` vào thư mục dự án `Blind-vow-`. File này đã được `.gitignore` chặn, nên không bị đưa lên kho.
4. Kiểm tra, trong thư mục `Blind-vow-`:

   ```
   .\rojo.exe --version
   ```

   Phải thấy `Rojo 7.7.1`.

Khi dùng `rojo.exe` trong thư mục dự án, mọi lệnh `rojo ...` trong hướng dẫn này đổi thành `.\rojo.exe ...`.

## Bước 3. Cài plugin Rojo trong Roblox Studio

1. Mở Roblox Studio, vào tab **Plugins** rồi **Manage Plugins**.
2. Tìm "Rojo" và cài bản chính thức. Bản plugin phải **cùng phiên bản 7.7.1** với Rojo CLI ở Bước 2. Nếu lệch, Studio có thể báo lỗi khi Connect.
3. Khởi động lại Studio nếu cần. Bạn sẽ thấy nút **Rojo** trong tab Plugins.

## Bước 4. Lấy code về máy

Lần đầu trên máy:

```
git clone https://github.com/nqvonepiece-beep/Blind-vow-.git
cd Blind-vow-
```

Những buổi sau, nếu thư mục còn trên máy:

```
cd Blind-vow-
git pull
```

## Bước 5. Đặt tên và email Git (mỗi buổi)

Git cần biết ai là người tạo commit. Nếu chưa đặt, Git sẽ từ chối lưu code với lỗi "Author identity unknown".

Trong thư mục `Blind-vow-`, chạy:

```
git config --local user.name "nqvonepiece-beep"
git config --local user.email "288598750+nqvonepiece-beep@users.noreply.github.com"
```

Kiểm tra:

```
git config --local user.name
git config --local user.email
```

Phải thấy đúng hai giá trị ở trên.

Lưu ý quan trọng:

- **Luôn dùng `--local`, không bao giờ dùng `--global`.** `--local` chỉ ghi vào thư mục dự án này, không ảnh hưởng người dùng khác trên máy tiệm net.
- Email trên là email ẩn do GitHub cấp, không lộ email thật của bạn trong kho công khai.
- Nếu thư mục dự án bị xóa, cài đặt này mất theo. Buổi sau chạy lại bước này.

## Bước 6. Chạy Rojo

Trong thư mục `Blind-vow-`, chạy:

```
rojo serve
```

(Nếu bạn để `rojo.exe` trong thư mục dự án, chạy `.\rojo.exe serve`.)

Nếu thấy dòng kiểu "Rojo server listening on port 34872" thì Rojo đã chạy. Đừng đóng cửa sổ này khi đang test.

## Bước 7. Kết nối Studio

1. Trong Roblox Studio, tạo một **Baseplate** mới (File, New, Baseplate).
2. Vào tab Plugins, bấm **Rojo**, rồi bấm **Connect** (giữ địa chỉ mặc định `localhost:34872`).
3. Studio sẽ nhận code từ kho. Trong Explorer sẽ có:
   - `ServerScriptService/Server/Main`, cùng hai thư mục `Combat` và `World`
   - `StarterPlayer/StarterPlayerScripts/Client/Main`, `CombatController`, `HitFeedback`
   - `ReplicatedStorage/Shared/Hello`, `Remotes`, cùng thư mục `Config`

## Bước 8. Chạy thử

1. Bấm **Play** (hoặc F5) trong Studio.
2. Mở cửa sổ **Output** (View, Output).
3. Bạn phải thấy hai dòng:
   - `Blind Vow khởi động (server)`
   - `Blind Vow khởi động (client)`

Nếu thấy cả hai, khung dự án đã chạy đúng.

Theo code hiện tại, bạn còn sẽ có một thanh kiếm trong túi đồ và một hình nộm tập đánh trước mặt. Phần combat này **chưa được test trong Studio**. Nếu có lỗi, hãy dán nguyên văn cho Claude.

## Khi làm việc hằng ngày

- Không sửa script trực tiếp trong Studio. Code gốc nằm trong thư mục `src` của kho. Sửa trong Studio sẽ bị ghi đè lần kết nối sau.
- Không lưu file `.rbxl` vào kho (đã được `.gitignore` chặn).

## Sao lưu dự án

Chỉ những gì **đã đẩy lên GitHub** mới an toàn. Mọi thứ chỉ nằm trên máy tiệm net có thể mất bất cứ lúc nào.

**Cái gì được sao lưu:** các file trong kho (`src`, `docs`, file cấu hình), sau khi đã commit và push.

**Cái gì KHÔNG được sao lưu:**

- Những gì bạn dựng tay trong Studio (part, model, bản đồ) và file place `.rbxl`. Nếu muốn giữ thứ gì dựng trong Studio, hãy hỏi Claude cách đưa nó vào kho trước khi rời máy.
- Cài đặt Git ở Bước 5 và file `rojo.exe`. Buổi sau làm lại.

**Kiểm tra đã đẩy hết lên GitHub chưa.** Trong thư mục `Blind-vow-`, chạy:

```
git status
```

Phải thấy cả hai:

- `nothing to commit, working tree clean` (không còn thay đổi chưa commit)
- `Your branch is up to date with 'origin/...'` (không còn commit chưa đẩy)

Sau đó chạy:

```
git log --branches --not --remotes --oneline
```

Lệnh này liệt kê các commit **chưa có trên GitHub**, ở mọi nhánh. **Phải không in ra dòng nào.** Nếu có dòng nào, nhờ Claude đẩy lên trước khi làm tiếp.

Cuối cùng, mở trang kho trên GitHub bằng trình duyệt và xem commit mới nhất của bạn đã có ở đó chưa.

## Bảo mật cuối buổi

Máy tiệm net là máy công cộng. Nếu để lại đăng nhập, người dùng sau có thể sửa hoặc xóa kho Blind Vow. Làm các bước này **sau khi** đã kiểm tra sao lưu ở mục trên. Sau khi đăng xuất, Claude sẽ không đẩy code lên được nữa.

**1. Tắt Rojo và Studio.** Ở cửa sổ đang chạy `rojo serve`, bấm `Ctrl+C`. Đóng Roblox Studio.

**2. Đăng xuất GitHub CLI.** Nếu máy có lệnh `gh`, kiểm tra:

```
gh auth status
```

Nếu thấy `Logged in to github.com`, chạy:

```
gh auth logout
```

Chọn tài khoản `nqvonepiece-beep` và xác nhận. Chạy lại `gh auth status`, phải thấy báo chưa đăng nhập (`You are not logged into any GitHub hosts`).

**3. Xóa mật khẩu GitHub còn lưu trong Windows.** Cả `gh` và Git đều có thể lưu đăng nhập trong **Windows Credential Manager**. Xem còn mục nào của GitHub:

```
cmdkey /list | findstr /i github
```

Các mục thường gặp:

- `Target: LegacyGeneric:target=gh:github.com:...`: do `gh` lưu. Bước 2 thường đã xóa, nếu còn thì xóa tiếp.
- `Target: LegacyGeneric:target=git:https://github.com`: do Git lưu khi bạn đẩy code.

Cách xóa (dùng chuột, dễ nhất): mở **Control Panel**, chọn **Credential Manager**, rồi **Windows Credentials**. Trong mục **Generic Credentials**, bấm vào từng mục có chữ `github`, chọn **Remove**.

Cách xóa bằng lệnh: với mỗi dòng ở trên, lấy phần nằm **sau** `target=` và chạy, ví dụ:

```
cmdkey /delete:git:https://github.com
```

Chạy lại `cmdkey /list | findstr /i github`, **phải không in ra dòng nào**.

**4. Đăng xuất mọi tài khoản khác.**

- Roblox Studio và trang roblox.com.
- github.com trên trình duyệt.
- Claude (ứng dụng và trang claude.ai).
- Email và mọi trang khác bạn đã đăng nhập.
- Đóng hết cửa sổ trình duyệt.

**5. Kiểm tra lần cuối.**

- [ ] `git log --branches --not --remotes --oneline` không in ra gì (đã làm trước khi đăng xuất).
- [ ] `gh auth status` báo chưa đăng nhập.
- [ ] `cmdkey /list | findstr /i github` không in ra gì.
- [ ] Đã đăng xuất Roblox, GitHub, Claude trên trình duyệt và ứng dụng.
- [ ] Không để mật khẩu hay token trong file, ghi chú hay clipboard.

## Gặp lỗi?

**Hãy dán nguyên văn thông báo lỗi từ cửa sổ Output của Studio** (hoặc từ cửa sổ dòng lệnh) cho Claude, đừng tóm tắt.

- **`rojo` không nhận lệnh:** đóng và mở lại cửa sổ dòng lệnh, hoặc chạy bằng `.\rojo.exe` trong đúng thư mục chứa nó.
- **Studio không kết nối được:** kiểm tra `rojo serve` còn chạy, plugin cùng phiên bản 7.7.1, và bật Allow HTTP Requests nếu plugin yêu cầu.
- **Git báo "Author identity unknown":** làm lại Bước 5.
- **Máy tiệm net chặn cài đặt hoặc chặn mạng:** nhắn lại cho Claude để tìm cách khác.
