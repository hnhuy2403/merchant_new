# Hướng dẫn cài đặt (dành cho người dùng mới)

> Tài liệu này giúp bạn cài Confluence Skill để dùng Confluence công ty **bằng cách chat với Claude** — không cần biết kỹ thuật. Toàn bộ chỉ mất khoảng 3 phút.

---

## Bạn cần có sẵn

- ✅ **Claude Code** (đã cài và dùng được)
- ✅ **Google Chrome** (hầu như máy nào cũng có)
- ✅ **Node.js** (thường đã có sẵn nếu bạn dùng Claude Code)

Nếu chưa có Node.js, tải tại: https://nodejs.org (chọn bản "LTS").

---

## Cài đặt: chỉ 2 dòng lệnh, làm 1 lần duy nhất

Mở **Terminal** (trên máy Mac: bấm `Cmd + Space`, gõ "Terminal", Enter), rồi dán lần lượt 2 dòng sau:

**Dòng 1** — tải skill về:
```
git clone <ĐỊA-CHỈ-BITBUCKET> confluence-vds-skill
```
> Thay `<ĐỊA-CHỈ-BITBUCKET>` bằng link repo mà đồng nghiệp/quản trị gửi cho bạn.

**Dòng 2** — vào thư mục và chạy cài đặt:
```
cd confluence-vds-skill && node setup.js
```

Chờ một chút. Khi thấy dòng **"🎉 CÀI ĐẶT XONG!"** là thành công.

Trình cài đặt sẽ tự lo hết:
- Cài các thư viện cần thiết
- Thiết lập sẵn 2 Confluence công ty (sản xuất + đối tác) — bạn **không cần biết địa chỉ IP**
- Cài skill vào Claude

---

## Dùng thử: chỉ cần CHAT

Sau khi cài xong:

1. **Mở lại Claude Code** (đóng và mở lại để Claude nhận skill mới).
2. Gõ:
   > **Kết nối Confluence sản xuất giúp tôi**
3. Claude sẽ hỏi **API token** của bạn (chỉ cần token, không cần mật khẩu).

### Lấy API token ở đâu?

1. Mở Confluence trên trình duyệt, đăng nhập.
2. Bấm vào ảnh đại diện (góc trên bên phải) → **Settings** (Cài đặt).
3. Tìm mục **Personal Access Tokens** → **Create token**.
4. Đặt tên bất kỳ (vd "Claude"), tạo, rồi **copy** chuỗi token.
5. Dán token đó cho Claude khi được hỏi.

> 🔒 Token được lưu **riêng trên máy bạn**, không gửi đi đâu, không ai khác thấy.

Khi Claude báo **"✅ Đã kết nối!"** — xong, bạn dùng được rồi.

---

## Bạn có thể nói gì với Claude?

- "Liệt kê các space trong Confluence"
- "Tìm trang về [chủ đề]"
- "Đẩy file báo cáo này lên Confluence, đặt tên 'Báo cáo Q1'" *(kèm đường dẫn file)*
- "Sửa lại tài liệu tôi đã đẩy hôm trước"
- "Chuyển sang Confluence đối tác"

Xem thêm câu mẫu trong file hướng dẫn chi tiết: [skills/confluence-vds-skill/references/usage-vi.md](skills/confluence-vds-skill/references/usage-vi.md)

---

## Gặp trục trặc?

| Hiện tượng | Cách xử lý |
|---|---|
| Claude không hiểu khi nói "kết nối Confluence" | Đóng hẳn Claude Code rồi mở lại (để nhận skill mới) |
| Báo "Token sai hoặc hết hạn" | Tạo token mới theo hướng dẫn trên, đưa lại cho Claude |
| Báo "chưa được cấp quyền dùng Confluence" | Token của bạn đúng, nhưng tài khoản chưa được mở quyền trên domain đó. Liên hệ **bộ phận quản trị Confluence nội bộ** để xin cấp quyền. Có thể thử domain còn lại trong lúc chờ. |
| `node setup.js` báo lỗi Node quá cũ | Cài Node bản LTS mới tại nodejs.org rồi chạy lại |
| Biểu đồ Mermaid không hiện | Cài Google Chrome rồi đẩy lại tài liệu |
| Không biết chạy lệnh ở đâu | Nhờ một đồng nghiệp rành kỹ thuật chạy giúp 2 dòng lệnh cài đặt |

Mọi việc sau khi cài xong đều **chỉ cần chat** — nếu kẹt, cứ hỏi thẳng Claude bằng tiếng Việt.
