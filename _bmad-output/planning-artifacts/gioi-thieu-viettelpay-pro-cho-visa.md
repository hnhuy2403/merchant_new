# Giới thiệu ứng dụng ViettelPay Pro

---

## 1. Tóm tắt

ViettelPay Pro là ứng dụng di động mà kênh phân phối của Viettel dùng để bán các dịch vụ tài chính số cho khách hàng. Người dùng app không phải người tiêu dùng, mà là đại lý, điểm bán lẻ, cộng tác viên bán hàng, nhân viên địa bàn và nhân viên quản lý kênh của Viettel trên cả nước. Nhiều người trong số họ ở khu vực nông thôn và ven đô.

Trên app, điểm bán có thể:
- Nạp tiền điện thoại, bán thẻ cào và thẻ game.
- Thu hộ hóa đơn: điện, nước, internet/truyền hình, trả góp, bảo hiểm, học phí, nạp tiền thu phí tự động VETC.
- Chuyển tiền và giao tiền mặt.
- Nạp tiền vào tài khoản ngân hàng và ví.
- Định danh khách hàng Viettel Money.
- Nhận thanh toán qua mã QR.


## 2. Vị trí của ViettelPay Pro trong hệ sinh thái Viettel Money

Viettel Money phục vụ trực tiếp người tiêu dùng. ViettelPay Pro phục vụ những người đứng ra giao dịch giúp khách tại điểm bán. Đây là kênh giao dịch có người hỗ trợ.

Khách hàng không tự dùng ví, hoặc cần nạp/rút tiền mặt, sẽ đến điểm bán Viettel gần nhất. Điểm bán thực hiện giao dịch trên ViettelPay Pro, còn khách trả bằng tiền mặt.

```
 Khách hàng (tiền mặt, QR; sắp tới: thẻ)
          │
          ▼
 Điểm bán / đại lý dùng ViettelPay Pro
          │  trả tiền từ tài khoản ký quỹ đã nạp trước
          ▼
 Nền tảng Viettel (Bankplus / BCCS / Viettel Money)
          │
          ▼
 Nhà cung cấp dịch vụ, nhà mạng, ngân hàng, trường học, bảo hiểm, giao thông...
```

## 3. Đối tượng sử dụng

| Đối tượng | Mô tả | Cách đăng nhập | Cách hạch toán giao dịch |
|---|---|---|---|
| Đại lý cấp 1/2/3 | Doanh nghiệp phân phối dịch vụ Viettel. Đại lý cấp 1 do Viettel quản lý; đại lý cấp 2, 3 là đại lý con do cấp trên tạo | Mã đại lý + PIN + OTP | Trừ tiền tài khoản ký quỹ |
| Điểm bán | Cửa hàng bán lẻ (tạp hóa, cửa hàng điện thoại...) | Mã điểm bán + PIN + OTP | Trừ tiền tài khoản ký quỹ |
| Nhân viên Bưu chính, Công trình, AM | Nhân viên thuộc Tập đoàn bán dịch vụ tại địa bàn | Tài khoản nhân viên + PIN + OTP | Trừ tiền tài khoản ký quỹ |
| CTV đa dịch vụ / hộ kinh doanh | Cá nhân bán hàng tự do | Tài khoản CTV + PIN + OTP | Giao dịch viễn thông ghi nhận công nợ; dịch vụ khác trừ tiền tài khoản ký quỹ |
| Nhân viên quản lý kênh (NVQL) | Nhân viên Viettel quản lý các điểm bán | Tài khoản NVQL + PIN + OTP | Giao dịch viễn thông ghi nhận công nợ; dịch vụ khác trừ tiền tài khoản ký quỹ |
| Giao dịch viên | Nhân viên tại cửa hàng Viettel | Tài khoản giao dịch viên + PIN + OTP | Ghi nhận công nợ cho tài khoản giao dịch viên |

**Mô hình đại lý 3 cấp.** Trên app, đại lý cấp trên có thể:
- Tạo đại lý con và cấp lại mật khẩu cho đại lý con.
- Chuyển tiền ký quỹ cho đại lý con.
- Khai báo mức chiết khấu và phí bán hàng cho đại lý con.

Khi đại lý con phát sinh giao dịch, hệ thống tự tính và trả chiết khấu cho tất cả các cấp ngay lập tức.

## 4. Mô hình tài khoản và dòng tiền

Mỗi người dùng có một **tài khoản ký quỹ** (tài khoản Bankplus-BCCS), nạp tiền trước để giao dịch. Phần lớn dịch vụ được thanh toán từ số dư này.

- **Nạp tiền vào tài khoản:** từ tài khoản ngân hàng hoặc tài khoản Viettel Money đã liên kết. NVQL cũng có thể thu tiền mặt rồi nạp hộ; người nhận xác nhận trên app.
- **Rút tiền:** rút về tài khoản ngân hàng hoặc ví đã liên kết.
- **Chuyển tiền giữa các đại lý:** đại lý cấp trên chuyển tiền cho đại lý con, đại lý con chuyển trả lại cấp trên.
- **Theo dõi:** số dư khả dụng, tổng số dư, dòng tiền trong tháng (căn cứ tính mức chiết khấu) và lịch sử biến động số dư.
- **Thu nhập của kênh:** kênh được hưởng chiết khấu khi bán sản phẩm viễn thông, và phí bán hàng khi làm dịch vụ thu hộ, chuyển tiền, tài chính. Kênh xem các khoản này trong báo cáo trên app.

Mô hình này liên quan trực tiếp đến việc nhận thẻ. Mỗi điểm bán đã có sẵn một tài khoản thanh toán trong hệ thống Viettel, có thể dùng để nhận tiền từ các giao dịch thẻ.

## 5. Các dịch vụ hiện có

| Nhóm | Dịch vụ |
|---|---|
| Viễn thông | Nạp tiền điện thoại cho mọi nhà mạng (Viettel, Vinaphone, Mobifone, Vietnamobile, Gmobile); thanh toán cước trả sau Viettel; bán thẻ cào mọi nhà mạng; bán thẻ game (Garena, Zing, Vcoin, Funtap, Gate...); thanh toán internet, truyền hình, cố định của Viettel và đối tác; gạch nợ thuê bao Viettel đã cắt hủy |
| Thu hộ | Tiền điện (EVN); tiền nước (nhiều công ty cấp nước các tỉnh); trả góp tài chính (Home Credit, FE Credit, Mcredit, OCB Credit, Shinhan Finance...); bán bảo hiểm (Bảo Việt, Prudential, MB Ageas...); học phí; nạp tiền thu phí tự động VETC; vé tàu |
| Chuyển tiền và tiền mặt | Chuyển tiền mặt trong nước (nhận tại quầy Viettel hoặc nhận tại nhà); giao tiền mặt cho người nhận; nạp tiền vào tài khoản ngân hàng theo số thẻ hoặc số tài khoản; nạp tiền vào tài khoản MB / Viettel Money theo số điện thoại; nạp tiền vào Viettel Money |
| Định danh khách hàng | Định danh (eKYC) khách hàng Viettel Money, kể cả tại nhà khách: CTV chụp giấy tờ tùy thân, khách xác nhận bằng OTP |
| Quản lý công việc địa bàn | NVQL giao việc giao tiền tận nhà và định danh tại nhà cho CTV. CTV nhận hoặc từ chối việc, xin ứng tiền, giải trình việc quá hạn. Mỗi bước có thời hạn và cảnh báo qua SMS |
| Nhận thanh toán QR | Mỗi điểm bán có một mã QR tĩnh riêng (MyQR). Khách dùng app Viettel Money hoặc Bankplus quét mã để trả tiền hàng; điểm bán xem doanh thu và lịch sử giao dịch QR trên app |

---

*Nguồn: Hướng dẫn sử dụng app ViettelPay Pro (QT.VDS.SP.08, cập nhật 2021–2022) và thông tin công khai trên kho ứng dụng. Danh sách dịch vụ và giao diện có thể đã thay đổi ở phiên bản hiện tại.*
