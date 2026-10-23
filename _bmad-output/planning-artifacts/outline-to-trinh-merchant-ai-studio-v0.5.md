# Thanh toán cho khách quốc tế tại merchant VTT – Outline tờ trình phê duyệt chủ trương

Cập nhật: 2026-10-21 · Huyhn8 · v0.5

> **Thay đổi ở v0.5:** giải pháp thanh toán của VDF được xác định là **Visa Accept**, theo tài liệu "VDS – Acquiring discussion" Visa trình bày tháng 10/2026. Cửa hàng nhận thẻ bằng điện thoại có NFC (Tap to Phone); khi khách không chạm được thì trả qua link. Các thay đổi:
> - Viết lại slide 11 (giải pháp thanh toán) và slide 12 (so sánh).
> - Thêm VPBank, Sacombank, VIB vào slide đối thủ, vì ba ngân hàng này đã ra mắt Visa Accept.
> - Mô hình doanh thu đổi theo hướng: Visa Accept gần như không thu MDR, doanh thu đến khi merchant lên gói SMB.
> - Lộ trình thêm bước nâng merchant lên gói SMB và phương án Visa QR Connector.
> - Rủi ro, câu hỏi xoáy và thông tin còn thiếu cập nhật theo Visa Accept.
>
> Bản v0.4.1 lưu tại `outline-to-trinh-merchant-ai-studio-v0.4.1.md`.
>
> **Lưu ý bảo mật:** số liệu về Visa Accept (hạn mức, phí, lộ trình nâng gói) lấy từ tài liệu *Visa Confidential*. Chỉ dùng trong tờ trình nội bộ, không trích ra tài liệu gửi bên ngoài.

## Thông tin chung

Báo cáo xin Tổng giám đốc VDF **phê duyệt chủ trương** để VDF cung cấp giải pháp và hạ tầng thanh toán cho khách quốc tế tại các merchant của VTT, dựa trên Visa Accept.

- **Hình thức:** slide, họp trực tiếp
- **Thời lượng:** khoảng 25 phút, 20 slide chính và phụ lục
- **Đơn vị đề xuất:** VDF
- **Bối cảnh:** VDF đã có dự án cung cấp nền tảng thanh toán cho Tammi, nhưng bài toán merchant chưa từng được báo cáo Tổng giám đốc. Tài liệu đề xuất v0.1 mới lưu hành nội bộ, chưa làm việc chính thức với Tendoo và Tammi. Visa đã trình bày Visa Accept cho Viettel (10/2026).
- **Thông điệp chính:** VDF triển khai Visa Accept để merchant Tendoo nhận thẻ của khách quốc tế ngay trên điện thoại. Khách chạm thẻ hoặc điện thoại; nếu không chạm được thì trả qua link. Gần như không mất phí, tiền về gần như tức thì. Kèm theo là trợ lý AI đa ngôn ngữ giúp khách hỏi được, hiểu được rồi mới mua. VTT phát triển merchant. Sau đó nâng merchant lên gói nhận thẻ đầy đủ và mở rộng sang khách Việt trên Tammi.

| Phần | Slide | Thời gian |
| --- | --- | --- |
| Mở đầu | 1 | 0,5 phút |
| I. Bối cảnh và vấn đề | 2–8 | 8 phút |
| II. Cơ hội cho VDF | 9 | 1 phút |
| III. Giải pháp | 10–16 | 9 phút |
| IV. Mô hình hợp tác | 17–18 | 3 phút |
| V. Lộ trình và kiến nghị | 19–20 | 3,5 phút |

## Mở đầu

### Slide 1 – Trang bìa

- Tên tờ trình (đề xuất): *Giải pháp thanh toán cho khách quốc tế tại merchant Tendoo – Tammi*. Đơn vị trình (VDF), ngày trình.

## Phần I – Bối cảnh và vấn đề (khoảng 8 phút)

### Slide 2 – Thị trường merchant trong nước

- Khoảng **5 triệu hộ kinh doanh**, đóng góp gần 30% GDP.
- Từ 01/01/2026 hộ kinh doanh bỏ thuế khoán, chuyển sang tự kê khai (NQ 198/2025/QH15). Đến 14/5/2026, hơn 308.000 hộ kinh doanh đã đăng ký hóa đơn điện tử từ máy tính tiền, tăng 35% so với cuối 2025 (Bộ Tài chính). Nhu cầu số hóa bán hàng và thanh toán tăng mạnh.
- Livestream chiếm khoảng 20% doanh thu thương mại điện tử (AccessTrade, đầu 2026).
- AI đã thành tính năng phổ biến: các phần mềm bán hàng đều có AI nhập liệu và chatbot. Lợi thế chuyển sang **trợ lý biết hành động**, gắn với kênh bán và dòng tiền thật.
- Kết luận của slide: merchant cần công cụ mang thêm khách và doanh thu, không chỉ công cụ quản lý.

### Slide 3 – Xu hướng du khách quốc tế: vì sao chọn phân khúc này

- 9 tháng 2026: **17,7 triệu lượt khách quốc tế, tăng 14,5%**, đạt gần 71% mục tiêu 25 triệu lượt cả năm. Cùng kỳ, du lịch quốc tế toàn cầu (6 tháng đầu năm) chỉ tăng 0,4%.
- Trung Quốc (khoảng 3,9 triệu lượt) và Hàn Quốc (khoảng 3 triệu lượt) chiếm gần 40% lượng khách.
- Năm 2025: 21,2 triệu lượt khách quốc tế, tổng thu du lịch khoảng 1 triệu tỷ đồng.
- **Vì sao tập trung phân khúc này:**
    - Tệp khách lớn, tăng nhanh, chi tiêu cao, nhưng chưa được phục vụ tốt ở cửa hàng nhỏ.
    - Tạo ra doanh thu mới cho merchant (bán được cho khách trước đây bỏ đi), chứ không chỉ chuyển giao dịch từ tiền mặt sang thẻ.
    - Là cửa ngõ để kéo merchant vào hệ sinh thái VDF. Merchant tăng doanh số sẽ được nâng lên gói nhận thẻ có thu phí.
    - Không phụ thuộc Tammi, chạy được ngay với Tendoo.
- *Cần bổ sung: mức chi tiêu bình quân của khách quốc tế, phần chi cho mua sắm và ăn uống; cơ cấu phương tiện thanh toán theo quốc tịch (thẻ Visa, thẻ khác, ví, tiền mặt).*

### Slide 4 – Khách quốc tế đang trả tiền thế nào tại Việt Nam

- Ba cách khách đang trả tiền và hạn chế của từng cách:
    - **Tiền mặt, đổi ngoại tệ:** bất tiện, rủi ro, khách thường mang ít.
    - **Thẻ quốc tế qua máy POS:** chủ yếu ở khách sạn, trung tâm thương mại, chuỗi lớn. Cửa hàng nhỏ ít có máy và ngại phí.
    - **QR xuyên biên giới** (khách quét mã bằng app nước mình): đang mở rộng nhưng chỉ dùng được với các nước đã kết nối và mới phủ ít điểm.
- Số liệu chính:
    - Chỉ khoảng 6% trong hơn 2,5 triệu điểm chấp nhận thanh toán nhận QR quốc tế (NHNN, 25/9/2026).
    - Nhu cầu là có thật: giao dịch VietQR Global của khách Thái Lan, Lào, Campuchia 8 tháng 2026 tăng khoảng 8 lần so với 2025. Giao dịch của khách Trung Quốc tăng khoảng 3 lần (NAPAS).
    - Cửa hàng đặc sản, quán ăn ở địa phương còn vướng rào cản thiết bị và chi phí (VCCI).
- Kết luận của slide: **khách có tiền và muốn trả, nhưng cửa hàng nhỏ chưa có cách nhận.**
- *Cần bổ sung: khảo sát hoặc số liệu về khó khăn thanh toán của du khách (xin từ NAPAS, Visa).*

### Slide 5 – NAPAS đang triển khai thế nào

- **Mô hình VietQR Global:** ví hoặc app ngân hàng nước ngoài kết nối với NAPAS, merchant nhận tiền VND qua mã VietQR. Có hai chiều: chiều vào (du khách trả tiền tại VN) và chiều ra (người Việt trả tiền ở nước ngoài).
- **Các nước đã kết nối (6 nước):** Thái Lan, Lào, Campuchia, Trung Quốc, Hàn Quốc, Singapore. Đang mở rộng sang Nhật Bản, Ấn Độ, Malaysia.
- Kết luận của slide: QR xuyên biên giới là hướng của quốc gia, nhưng **chỉ phục vụ khách từ các nước đã kết nối**, và mới khoảng 6% điểm chấp nhận. Khách từ các nước còn lại (châu Âu, Mỹ, Úc, Nhật Bản, Ấn Độ…) vẫn phải dùng thẻ quốc tế.

### Slide 6 – Đối thủ đã có giải pháp gì, khoảng trống ở đâu

- **Các giải pháp đối thủ đã có:**

| Đối thủ | Giải pháp cho khách quốc tế | Hạn chế |
| --- | --- | --- |
| **VPBank, Sacombank, VIB** – Visa Accept | Đã ra mắt Visa Accept trong app ngân hàng (VPBank TapLink, VIB BizPay…): chủ thẻ Visa ghi nợ thành người bán, nhận thẻ bằng điện thoại, không cần thiết bị | Chỉ cho khách hàng của ngân hàng; là tính năng nhận tiền trong app ngân hàng, không gắn với quản lý bán hàng; ngân hàng không có đội phát triển merchant thực địa |
| **VNPAY** – QR | Khách Trung Quốc, Hàn Quốc, Thái Lan, Lào, Campuchia, Singapore quét VNPAY-QR bằng app nước mình (WeChat Pay, Alipay, UnionPay, Toss Pay…). Đã có tại chuỗi Thế Giới Di Động, Điện Máy Xanh, TopZone (từ 9/2026) | Chỉ khách từ các nước đã kết nối; tập trung chuỗi lớn |
| **VNPAY** – app cho du khách | Hợp tác Mastercard: khách quốc tế tải app VNPAY, liên kết thẻ rồi quét QR thanh toán *(cần nguồn xác nhận)* | Khách phải tải thêm app, đăng ký, liên kết thẻ trong chuyến đi ngắn |
| **VNPAY** – SoftPOS | Biến điện thoại Android thành máy nhận thẻ không tiếp xúc (Visa, Apple Pay, Google Pay, Samsung Pay), đạt chuẩn PCI CPoC | Là app thanh toán riêng, không gắn với quản lý bán hàng của hộ kinh doanh |
| **Ngân hàng** (VCB Tap to Phone…) | Cửa hàng nhận thẻ không tiếp xúc trên điện thoại Android | Chủ tiệm dùng thêm một app riêng; chưa có phương án khi khách không chạm được |
| **MoMo** | Tập trung chiều ra (người Việt dùng MoMo quét Alipay+ ở nước ngoài), làm du lịch cùng Saigontourist | Chưa phục vụ du khách trả tiền tại VN |
| **Phần mềm bán hàng** (KiotViet, Sapo, MISA) | Quản lý bán hàng, có kết nối máy POS hoặc QR nội địa | Chưa có giải pháp riêng cho khách quốc tế |

- **Khoảng trống để VDF giải quyết:**
    1. **Thanh toán tách khỏi bán hàng:** các giải pháp nhận thẻ đều là app riêng hoặc tính năng trong app ngân hàng, chủ tiệm phải ghi sổ lại bằng tay.
    2. **Mới giúp khách trả tiền, chưa giúp khách mua:** khách không hỏi được, không hiểu sản phẩm thì không mua. Chưa giải pháp nào giải quyết rào cản ngôn ngữ.
    3. **Hộ kinh doanh nhỏ ở điểm du lịch chưa được phủ:** ngân hàng chờ khách hàng tự bật tính năng, VNPAY đi qua chuỗi lớn trước.
- Thông điệp của slide: **Visa Accept đã có ở ba ngân hàng, nên công nghệ không phải là khác biệt. Khác biệt nằm ở tệp merchant, kênh phát triển và việc gắn với bán hàng.**
- *Cần nghiên cứu thêm: kết quả triển khai Visa Accept của VPBank, Sacombank, VIB; nguồn xác nhận hợp tác VNPAY – Mastercard; số điểm chấp nhận và phí MDR quốc tế của VNPAY.*

### Slide 7 – Bài học từ thế giới: app chat và thanh toán

- **WeChat Pay (Trung Quốc):** đưa thanh toán vào app chat (2013), bùng nổ nhờ lì xì điện tử dịp Tết 2014. Người nhận phải liên kết tài khoản để rút tiền, biến thói quen chat thành thói quen thanh toán. Thị phần WeChat Pay tăng gấp đôi sau chiến dịch. Đến 2018, Alipay và WeChat Pay chiếm khoảng 92,7% thanh toán bên thứ ba.
- **KakaoPay (Hàn Quốc):** thanh toán gắn với KakaoTalk, đạt 5 triệu người dùng trong năm đầu, khoảng 24 triệu MAU cuối 2024, khoảng 650.000 merchant offline. Người dùng cả KakaoTalk Pay và app KakaoPay tạo doanh thu gấp 2,4 lần.
- **Alipay, WeChat Pay mở cho du khách (Trung Quốc 2023–2025):** cho liên kết thẻ quốc tế, miễn phí giao dịch dưới 200 tệ. Năm 2024, giao dịch của du khách trên Alipay tăng khoảng 10 lần, người dùng hoạt động tăng khoảng 6 lần. Dịp Quốc khánh 2025, chi tiêu của khách quốc tế qua Alipay tăng gần 40%, thanh toán chạm tăng 500%.
- **Bài học cho Viettel:**
    - Thanh toán gắn vào app dùng hằng ngày là con đường nhanh nhất để có người dùng. Đây là hướng cho Tammi với người dùng Việt.
    - Khi trả tiền dễ hơn, du khách chi tiêu nhiều hơn ngay, và thanh toán chạm tăng nhanh nhất. Ở Việt Nam, cái thiếu là **phía cửa hàng nhận tiền**. VDF lấp đúng chỗ này.
- *Lưu ý: các số liệu trên chủ yếu do doanh nghiệp công bố. Cần kiểm tra lại trước khi trình.*

### Slide 8 – Vấn đề của Tendoo và Tammi

- **Tendoo:**
    - Khoảng 200.000 merchant, phần lớn không hoạt động. Công cụ quản lý chưa tạo thêm khách và thêm doanh thu, nên người bán chưa có lý do gắn bó.
    - Merchant không nhận được thẻ quốc tế, không trao đổi được với khách nước ngoài, nên mất khách.
    - Thanh toán chưa gắn với hàng hóa, đơn và sổ sách trên Tendoo.
- **Tammi:**
    - Khoảng 10 triệu người dùng Việt đã xác thực, chat hằng ngày, nhưng chưa có lớp thương mại (chưa có cửa hàng, livestream hay công cụ cho người bán).
    - Người mua sợ lừa đảo khi mua online, phải chuyển qua lại nhiều app để xem, nhắn, trả tiền.
- **Hai tài sản đang tách rời:** người bán và người mua gặp nhau qua nền tảng ngoài với phí cao, dữ liệu và dòng tiền nằm ngoài hệ sinh thái. Minh họa: sơ đồ "Trước" trong tài liệu đề xuất (mục 2).
- *Cần bổ sung: số merchant Tendoo chính xác (tổng, active); MAU Tammi; số đơn và GMV hiện tại trên Tendoo.*
- *Lưu ý: số công bố công khai của Tammi là 5 triệu+ (8/2026). Ghi rõ 10 triệu là số nội bộ và thời điểm.*

## Phần II – Cơ hội cho VDF (khoảng 1 phút)

### Slide 9 – Cơ hội cho VDF

- **Có thêm merchant và chủ thẻ:** mỗi merchant dùng Visa Accept cần một thẻ Visa ghi nợ hoặc trả trước để nhận tiền. VDF phát hành thẻ này *(cần xác nhận)*, nên có thêm khách hàng thẻ và dòng tiền đổ về hệ sinh thái.
- **Doanh thu khi merchant lớn lên:** merchant vượt hạn mức Visa Accept được nâng lên gói SMB (MDR dưới 1%), rồi lên gói nhận thẻ đầy đủ. VDF giữ được merchant từ lúc nhỏ đến lúc lớn.
- **Lấp khoảng trống đối thủ chưa phủ:** hộ kinh doanh nhỏ ở điểm du lịch, cần cả nhận tiền lẫn giao tiếp với khách, và cần thanh toán gắn với sổ sách.
- **Có sẵn tệp merchant:** 200.000 merchant Tendoo và đội kênh bán thực địa của VTT, không phải chờ merchant tự tìm đến như ngân hàng.
- **Mở rộng quan hệ chiến lược:** với Visa (Visa Accept, sau đó là các sản phẩm nhận thẻ khác) và với VTT, từ "cung cấp thanh toán cho Tammi" lên thành "đồng kiến tạo lớp thương mại".

## Phần III – Giải pháp (khoảng 9 phút)

### Slide 10 – Giải pháp tổng thể

- Định nghĩa trong một câu: *VDF dùng Visa Accept để merchant Tendoo nhận tiền của khách quốc tế ngay trên điện thoại, kèm trợ lý AI đa ngôn ngữ; sau đó nâng merchant lên gói nhận thẻ đầy đủ và mở rộng sang bán cho khách Việt trên Tammi.*
- Minh họa: sơ đồ "Sau" vẽ lại với **thanh toán của VDF ở trung tâm**. Ba lớp:
    1. **Thanh toán VDF:** Visa Accept (Tap to Phone và link thanh toán), sau đó là gói SMB và thanh toán nội địa đa nguồn tiền.
    2. **Merchant AI Studio:** trợ lý AI tư vấn và bán hàng, tạo từ dữ liệu cửa hàng có sẵn trên Tendoo.
    3. **Kênh khách hàng:** du khách quốc tế tại cửa hàng (làm ngay), người dùng Tammi (mở rộng sau).
- Mục tiêu cốt lõi: **tăng dòng tiền cho merchant Tendoo**. Mọi giao dịch đi qua thanh toán VDF và tự ghi sổ trên Tendoo.

### Slide 11 – Giải pháp chi tiết 1: Visa Accept – nhận thẻ của khách quốc tế ngay trên điện thoại

- **Visa Accept là gì:** sản phẩm của Visa, biến chủ thẻ Visa ghi nợ hoặc trả trước thành người bán. Đã ra mắt tại Việt Nam qua VPBank, Sacombank, VIB.
- **Hai cách nhận tiền:**
    - **Tap to Phone:** khách chạm thẻ hoặc điện thoại, đồng hồ có ví (Apple Pay, Google Pay…) vào điện thoại có NFC của cửa hàng. Không cần máy POS.
    - **Pay by Link:** khi khách không chạm được, khách quét mã QR trên điện thoại của cửa hàng để mở link thanh toán, hoặc nhận link qua SMS, email. Khách nhập thẻ, xác thực 3-D Secure, có hỗ trợ Click to Pay.
- **Luồng của merchant:**
    - Đăng ký trong app của VDF: xác minh hộ kinh doanh (KYB), chọn thẻ Visa nhận tiền, đặt tên cửa hàng.
    - Bán hàng: nhập số tiền hoặc chọn hàng, cho khách chạm thẻ hoặc gửi link.
    - Theo dõi doanh số, lịch sử giao dịch, hoàn tiền ngay trong app.
- **Luồng của du khách:** chạm thẻ hoặc mở link → thanh toán → nhận biên lai.
- **Điều kiện chính (theo Visa):**

| Nội dung | Visa Accept |
| --- | --- |
| Hạn mức mỗi tháng | Tối đa khoảng 100 triệu đồng (4.000 USD), 2.000 giao dịch |
| Hạn mức mỗi giao dịch | Khoảng 8 triệu đồng (300 USD) |
| Phí với merchant | MDR gần như bằng 0 |
| Phí mạng lưới | Đến 31/01/2027: IRF và phí acquirer mỗi loại 10bps, tối đa 250đ mỗi giao dịch. Từ 01/02/2027: giao dịch dưới 200.000đ miễn phí; từ 200.000đ trở lên IRF 200đ và phí acquirer 0,002 USD |
| Tiền về | Gần như tức thì, vào thẻ Visa của merchant |
| Kiểm soát rủi ro | Theo dõi tần suất giao dịch, giới hạn hạn mức, 3-D Secure cho giao dịch qua link, có chức năng hoàn tiền, báo cáo đối soát |

- **Lộ trình nâng gói của Visa:** merchant chạm hạn mức Visa Accept → nâng lên gói SMB (MDR dưới 1%, khoảng 180 triệu đồng mỗi tháng, không giới hạn số giao dịch và giá trị mỗi giao dịch) → gói nhận thẻ đầy đủ theo biểu phí chuẩn, nhiều loại thiết bị.
- **Điểm VDF làm thêm:** đưa Visa Accept vào trải nghiệm bán hàng của Tendoo, để giao dịch tự ghi sổ và gắn với đơn hàng.
- *Cần xác nhận với Visa:*
    - *SDK Visa Accept nằm trong app của bên phát hành thẻ (Viettel Money). Có tích hợp được vào Tendoo hay chỉ đồng bộ dữ liệu giao dịch sang Tendoo?*
    - *VDF có đủ điều kiện làm bên phát hành thẻ Visa ghi nợ hoặc trả trước cho merchant không?*
    - *Visa Accept nhận những loại thẻ nào (chỉ Visa hay cả Mastercard)? Có chạy trên iPhone không?*
    - *Phí IRF và phí acquirer do bên nào trả, bên nào nhận?*

### Slide 12 – Vì sao giải pháp của VDF vượt trội

| Tiêu chí | Máy POS ngân hàng | SoftPOS của ngân hàng, VNPAY | Visa Accept trong app ngân hàng (VPBank, Sacombank, VIB) | QR xuyên biên giới (VietQR Global, VNPAY-QR) | **VDF: Visa Accept + Tendoo + trợ lý AI** |
| --- | --- | --- | --- | --- | --- |
| Khách từ nước nào cũng trả được | Có (thẻ) | Có (thẻ, ví chạm) | Có (thẻ Visa, ví chạm) | Chỉ 6 nước đã kết nối | **Có (thẻ Visa, ví chạm, link)** |
| Khách không phải cài thêm app | Có | Có | Có | Có | **Có** |
| Cửa hàng không cần mua thiết bị | Không | Có | Có | Có | **Có** |
| Phí với cửa hàng | MDR theo hợp đồng | MDR theo hợp đồng | Gần như 0 | Theo đơn vị cung cấp | **Gần như 0, có lộ trình nâng gói** |
| Tiền về | Theo chu kỳ quyết toán | Theo chu kỳ quyết toán | Gần như tức thì | Theo đơn vị cung cấp | **Gần như tức thì** |
| Có phương án khi không chạm được | Quẹt, cắm chip | Không | Có (link) | Không áp dụng | **Có (link)** |
| Giao dịch tự ghi sổ bán hàng, phục vụ thuế | Không | Không | Không | Một phần | **Có** |
| Tư vấn khách bằng tiếng nước họ | Không | Không | Không | Không | **Có (trợ lý AI, slide 13)** |
| Kênh đưa giải pháp đến hộ kinh doanh | Nhân viên ngân hàng | Nhân viên ngân hàng, đại lý | Khách hàng tự bật trong app | Ngân hàng, trung gian | **200.000 merchant Tendoo, đội kênh bán VTT** |

- Thông điệp: *ngân hàng đã có Visa Accept nhưng chỉ là nút nhận tiền trong app ngân hàng. VDF đưa Visa Accept đến tận hộ kinh doanh qua Tendoo và đội kênh bán, gắn với bán hàng, sổ sách và trợ lý tư vấn đa ngôn ngữ.*
- **Điểm yếu cần nói thật:**
    - Chưa phục vụ khách chỉ dùng ví nước mình như Alipay, WeChat Pay (phần lớn khách Trung Quốc).
    - Có thể chỉ nhận thẻ Visa (cần xác nhận).
    - Hạn mức khoảng 8 triệu đồng mỗi giao dịch và 100 triệu đồng mỗi tháng. Cửa hàng lớn cần lên gói SMB.
- *Ghi chú trên slide: đánh giá sơ bộ theo thông tin đến 10/2026. Cần kiểm tra lại bảng trước khi trình.*

### Slide 13 – Giải pháp chi tiết 2: trợ lý AI tư vấn khách quốc tế tại cửa hàng

- Khách quét QR tại cửa hàng để mở trang web của trợ lý, không cần cài app. Trợ lý nói nhiều ngôn ngữ (Trung, Hàn, Anh…).
- Trợ lý giải đáp về sản phẩm, giá, cách dùng theo dữ liệu cửa hàng trên Tendoo; nhận đặt hàng thay nhân viên; gửi link thanh toán Visa Accept ngay trong cuộc trò chuyện.
- Chủ tiệm tạo trợ lý trong vài phút từ dữ liệu cửa hàng sẵn có.

### Slide 14 – Giải pháp chi tiết 3: mở rộng sang khách Việt trên Tammi

- Các trợ lý online trên Tammi (nêu ngắn, triển khai ở các phase sau):
    - Trợ lý bán hàng trên OA cửa hàng: trực tin nhắn ngoài giờ, tạo đơn trong chat.
    - Trợ lý livestream: trả lời và tạo đơn khi live.
    - Trợ lý Tammi OA: đặt món nhóm, tìm hàng nhiều shop.
- Thanh toán đa nguồn tiền của VDF ngay trong chat: Viettel Money, tài khoản ngân hàng, thẻ nội địa và quốc tế.
- Đơn, kho, sổ sách tự đồng bộ về Tendoo.

### Slide 15 – Demo

- Khoảng 2–2,5 phút, kịch bản tập trung vào du khách: khách Hàn Quốc vào cửa hàng ở Hội An, quét QR hỏi trợ lý bằng tiếng Hàn, đặt hàng, chạm thẻ Visa vào điện thoại của chủ tiệm, đơn tự ghi sổ trên Tendoo. Thêm tình huống khách không chạm được: chủ tiệm gửi link, khách trả bằng thẻ.
- Có thể dùng màn hình mẫu Visa Accept trong tài liệu của Visa làm tham khảo.
- *Kịch bản chi tiết bổ sung sau.*

### Slide 16 – Vì sao Viettel làm được

- Ba lợi thế mà ngân hàng và đối thủ không có đủ cả chuỗi:
    - **Có sẵn merchant và đội kênh bán:** 200.000 merchant Tendoo và đội kênh bán thực địa của VTT.
    - **Thanh toán gắn với quản lý bán hàng:** giao dịch tự ghi sổ trên Tendoo, phục vụ kê khai thuế.
    - **Trợ lý biết hành động:** tư vấn đa ngôn ngữ, tạo đơn, gửi link thanh toán, đồng bộ kho.
- Thêm: Visa đã chủ động đề xuất hợp tác với Viettel trên nhiều sản phẩm (Visa Accept, QR Connector, Visa Acceptance Platform).
- Cho giai đoạn sau: kênh người mua Việt của Tammi, đã xác thực bằng thuê bao.

## Phần IV – Mô hình hợp tác (khoảng 3 phút)

### Slide 17 – Mô hình hợp tác và vai trò hai bên

| Bên | Vai trò |
| --- | --- |
| **VDF** | Cung cấp **giải pháp và hạ tầng thanh toán merchant quốc tế**: triển khai Visa Accept (phát hành thẻ nhận tiền cho merchant, xác minh hộ kinh doanh, quyết toán, xử lý rủi ro); nâng merchant lên gói SMB; Merchant AI Studio và các mẫu trợ lý; hỗ trợ, vận hành, đối soát |
| **VTT** (Tendoo, Tammi) | **Phát triển merchant**: tích hợp giải pháp vào app Tendoo, cung cấp dữ liệu hàng hóa và đơn, tuyển và hỗ trợ cửa hàng qua đội kênh bán; Tammi xây lớp thương mại cho người dùng Việt ở các phase sau |

- **Đối tác bên ngoài:** Visa (sản phẩm Visa Accept, SDK, mạng lưới thẻ, công cụ chống gian lận); ngân hàng thanh toán nếu cần.
- Hiện trạng: chưa làm việc chính thức với VTT. Đây là lý do của nội dung xin duyệt số 2.
- Các điểm cần thống nhất: chia sẻ doanh thu, quyền sở hữu dữ liệu, chi phí vận hành, chỉ tiêu kênh bán.
- *Chưa rõ: Viettel Post (giao hàng), Viettel Telecom, Viettel AI.*

### Slide 18 – Mô hình doanh thu và ước tính sơ bộ

- **Nguyên tắc:** ở giai đoạn Visa Accept, MDR gần như bằng 0. Mục tiêu giai đoạn này là **có merchant và chủ thẻ**. Doanh thu đến khi merchant lớn lên và khi mở rộng dịch vụ.

| Dòng thu | Phase |
| --- | --- |
| Phát hành thẻ Visa cho merchant: số dư, chi tiêu bằng thẻ, dịch vụ tài chính đi kèm *(cần xác nhận cơ chế)* | 1 |
| Phần phí mạng lưới VDF được nhận từ giao dịch Visa Accept *(cần xác nhận với Visa)* | 1 |
| MDR khi merchant nâng lên gói SMB (dưới 1%) và gói nhận thẻ đầy đủ | 2 |
| MDR thanh toán trong chat: Viettel Money, tài khoản ngân hàng, thẻ nội địa | 2 |
| Thanh toán trên Tammi Shop và livestream | 2 |
| Gói dịch vụ AI cho người bán *(cần thống nhất bên nào thu)* | 2 |
| QR cho khách dùng ví nước mình (Visa QR Connector hoặc VietQR Global) | 3 |
| Thanh toán xuyên biên giới cho người Việt ra nước ngoài | 3 |

- Ước tính theo 3 kịch bản (thận trọng, cơ sở, tích cực):
    - Số merchant dùng Visa Accept × tỉ lệ merchant nâng lên gói SMB × GMV mỗi merchant × MDR.
    - Cộng thêm doanh thu từ thẻ phát hành cho merchant.
- *Cần bổ sung: dự phóng năm 1–3; tỉ lệ merchant nâng gói (xin số tham khảo từ Visa).*

## Phần V – Lộ trình và kiến nghị (khoảng 3,5 phút)

### Slide 19 – Lộ trình triển khai và pilot

| Phase | Trọng tâm | Phụ thuộc |
| --- | --- | --- |
| 0 – Chuẩn bị | Làm việc với VTT, chốt phạm vi và đầu mối; ký hợp tác Visa Accept với Visa, nhận SDK; xác nhận VDF làm bên phát hành thẻ; nhận API và dữ liệu mẫu của Tendoo | Đồng thuận của VTT; Visa |
| 1 – Pilot khách quốc tế | **Bước 1a:** mở Visa Accept (Tap to Phone, Pay by Link) cho merchant Tendoo, giao dịch đồng bộ về Tendoo. **Bước 1b:** bật trợ lý tư vấn đa ngôn ngữ tại cửa hàng | VDF, Visa, Tendoo; không cần Tammi |
| 2 – Mở rộng | Nhân rộng ra các điểm du lịch qua đội kênh bán VTT; **nâng merchant vượt hạn mức lên gói SMB** (Visa Acceptance Platform, thêm loại thẻ); trợ lý trên OA cửa hàng và livestream cho người dùng Việt trên Tammi | Visa; Tammi tích hợp AI vào OA, xây Shop và Live |
| 3 – Hệ sinh thái | QR cho khách dùng ví nước mình: **Visa QR Connector** (Viettel Money làm cầu nối QR, du khách quét bằng ví có thẻ Visa) hoặc VietQR Global; Tammi OA đầy đủ; thanh toán cho người Việt ra nước ngoài | Visa, NAPAS, giấy phép |

- **Pilot:** một nhóm cửa hàng đông khách quốc tế (ví dụ Hội An, Đà Nẵng, Phú Quốc), hộ kinh doanh vừa và nhỏ, mọi ngành hàng. Ưu tiên điểm có nhiều khách dùng thẻ Visa (Hàn Quốc, châu Âu, Mỹ, Úc). Chỉ tiêu kênh bán theo **cửa hàng phát sinh giao dịch**, không theo số tài khoản mở.
- **KPI chính: GMV của cửa hàng qua Visa Accept.** GMV ở bước 1a là mốc nền, bước 1b đo phần tăng thêm từ các đơn có tương tác với trợ lý.
- **Chỉ số theo dõi:** tỉ lệ cửa hàng còn giao dịch sau 30 ngày; số merchant chạm hạn mức và nâng gói.
- *Cần bổ sung: mốc thời gian từng phase (sau khi chốt phạm vi với Visa và VTT); ngưỡng go/no-go.*

### Slide 20 – Kiến nghị và bước tiếp theo

- **Ba nội dung xin duyệt** (đề xuất, cần chốt):
    1. Chấp thuận chủ trương VDF cung cấp giải pháp thanh toán cho khách quốc tế tại merchant VTT trên nền Visa Accept, kèm Merchant AI Studio.
    2. Giao VDF làm đầu mối làm việc và đàm phán hợp tác với VTT (Tendoo, Tammi) và với Visa: phân vai, chia sẻ doanh thu, dữ liệu.
    3. Phê duyệt lộ trình và mốc thời gian triển khai Phase 0 và Phase 1 (pilot khách quốc tế).
- **Ba rủi ro chính và hướng xử lý:**
    - Merchant không dùng thật: chỉ tiêu kênh bán theo cửa hàng có giao dịch.
    - Ngân hàng đã có Visa Accept: khác biệt bằng tệp merchant Tendoo, đội kênh bán, việc gắn với bán hàng và trợ lý AI.
    - Doanh thu giai đoạn đầu thấp do MDR gần như bằng 0: đo tỉ lệ nâng gói, coi Phase 1 là giai đoạn có merchant.
- Các việc trong 30, 60 và 90 ngày tới nếu được duyệt, bắt đầu bằng buổi làm việc VDF – VTT và chốt điều khoản Visa Accept với Visa.

## Phụ lục

- Rủi ro chi tiết và hướng xử lý:

| Rủi ro | Hướng xử lý |
| --- | --- |
| Merchant vẫn không dùng thật | Chỉ tiêu kênh bán theo cửa hàng có giao dịch; pilot đo GMV và tỉ lệ còn giao dịch sau 30 ngày |
| VPBank, Sacombank, VIB đã có Visa Accept | Tập trung hộ kinh doanh của Tendoo; khác biệt bằng kênh bán thực địa, gắn với bán hàng, sổ sách, trợ lý đa ngôn ngữ |
| SDK Visa Accept chỉ chạy trong app của bên phát hành thẻ, khó tích hợp vào Tendoo | Xác nhận với Visa ở Phase 0; phương án dự phòng là bán hàng trong Viettel Money và đồng bộ giao dịch về Tendoo qua API |
| Chỉ nhận thẻ Visa, chưa nhận thẻ khác và ví nước ngoài | Pilot ưu tiên điểm nhiều khách dùng thẻ Visa; thêm loại thẻ ở gói SMB; QR cho ví nước ngoài ở Phase 3 |
| Hạn mức Visa Accept thấp với cửa hàng lớn | Nâng lên gói SMB khi chạm hạn mức |
| Doanh thu giai đoạn đầu thấp do MDR gần như bằng 0 | Đặt mục tiêu Phase 1 là có merchant và chủ thẻ; theo dõi tỉ lệ nâng gói |
| Merchant phải mở thẻ Visa và qua bước xác minh hộ kinh doanh | Đội kênh bán hỗ trợ tại chỗ; đơn giản hóa xác minh qua dữ liệu Tendoo |
| Điện thoại của cửa hàng không hỗ trợ NFC | Dùng Pay by Link; xác nhận danh sách thiết bị hỗ trợ |
| Gian lận thẻ | Theo dõi tần suất, giới hạn hạn mức của Visa Accept; 3-D Secure cho giao dịch qua link; cân nhắc Decision Manager của Visa khi lên gói SMB |
| Phụ thuộc lộ trình Tammi (tích hợp AI vào OA, Shop, Live) | Phase 1 không cần Tammi |
| Tammi chưa hình thành thói quen mua sắm | Kiểm chứng ở Phase 2 trước khi đầu tư lớn |
| Phối hợp nhiều đơn vị | Giao VDF làm đầu mối (nội dung xin duyệt số 2) |
| Pháp lý AI: Luật Trí tuệ nhân tạo 134/2025 | Luôn gắn nhãn "Trợ lý AI" và nút "Gặp người thật" |
| Dữ liệu cá nhân: Nghị định 13/2023 | Chỉ dùng dữ liệu khi người dùng đồng ý; khách quốc tế dùng web không cần đăng ký; dữ liệu lưu tại Việt Nam |
| AI tư vấn sai, giao dịch sai | Chỉ trả lời theo dữ liệu cửa hàng; trợ lý không tự trừ tiền; khiếu nại, hoàn tiền luôn chuyển người thật |

- Tóm tắt các sản phẩm Visa giới thiệu cho Viettel (10/2026): Visa Pay và QR Connector, Visa Accept, Visa Acceptance Platform (Pay by Link, Tap to Phone, Token Management, Decision Manager), Visa Direct, Fintech Fast Track, SMR Wallet.
- Màn hình mẫu Visa Accept: đăng ký, bán hàng bằng chạm thẻ, bán hàng bằng link, trải nghiệm người mua.
- Bảng so sánh chi tiết với phần mềm bán hàng và nền tảng thương mại (KiotViet, Sapo, MISA, Pancake/Botcake, Zalo OA, TikTok Shop, Shopee).
- Đối tác chính của NAPAS theo từng thị trường (UnionPay, Alipay, GLN, Liquid Group và các ngân hàng quyết toán).
- Trải nghiệm chi tiết theo persona: chị Lan (cửa hàng trà ở Hội An), Minh (người dùng Tammi), anh Kim Min-jun và chị Camille Laurent (du khách).
- Ví dụ theo ngành hàng: ăn uống, thời trang, quà lưu niệm, mỹ phẩm và nhà thuốc, spa, tạp hóa.
- Kiến trúc và điểm tích hợp Tendoo – Studio – Tammi – thanh toán VDF – Visa.
- Giá trị cho từng bên: người bán, khách quốc tế, người dùng Tammi, Tendoo, Tammi, VDF.
- Bộ KPI đầy đủ, giả định tài chính.
- Nguồn số liệu:
    - Visa, "VDS – Acquiring discussion", 10/2026 (*Visa Confidential*): Visa Accept, hạn mức, phí, lộ trình nâng gói, triển khai tại VPBank, Sacombank, VIB; Visa QR Connector; Visa Acceptance Platform
    - NQ 198/2025/QH15 (bỏ thuế khoán từ 01/01/2026)
    - [Hỗ trợ hộ kinh doanh chuyển đổi số và kê khai thuế – VnEconomy](https://vneconomy.vn/ho-tro-ho-kinh-doanh-chuyen-doi-so-va-ke-khai-thue.htm)
    - [Kết quả triển khai hóa đơn điện tử – Thời báo Tài chính](https://thoibaotaichinhvietnam.vn/infographics-ket-qua-trien-khai-hoa-don-dien-tu-197840-197840.html)
    - [Tammi vượt 5 triệu người dùng – VnExpress 19/08/2026](https://vnexpress.net/ung-dung-tammi-nam-trong-top-tai-nhieu-tai-viet-nam-5110618.html)
    - [21,2 triệu lượt khách quốc tế 2025 – Báo Chính phủ](https://en.baochinhphu.vn/foreign-arrivals-soar-to-record-high-in-2025-111260106100233228.htm)
    - [Khách quốc tế 9 tháng 2026 tăng 14,5% – Báo Văn hóa](https://baovanhoa.vn/du-lich/khach-quoc-te-den-viet-nam-9-thang-2026-tang-145-271196.html)
    - [Trung Quốc, Hàn Quốc dẫn đầu nguồn khách 9 tháng 2026 – Mekong ASEAN](https://mekongasean.vn/trung-quoc-han-quoc-dan-dau-nguon-khach-quoc-te-den-viet-nam-trong-9-thang-60416.html)
    - [6,7 triệu lượt người Việt ra nước ngoài 2025 – Nhân Dân](https://nhandan.vn/khach-viet-ngay-cang-chuong-xuat-ngoai-va-sanh-du-lich-post936688.html)
    - [Livestream ~20% doanh thu TMĐT – VnBusiness, dẫn AccessTrade](https://vnbusiness.vn/ban-hang-online-chien-truong-khoc-liet-tay-mo-kho-tru.html)
    - Khoảng 6% điểm chấp nhận thanh toán nhận VietQR Global: NHNN và Cục Du lịch, hội thảo 25/9/2026
    - [VietQR Global tăng khoảng 8 lần, 8 tháng 2026 – Thị trường Tài chính Tiền tệ](https://thitruongtaichinhtiente.vn/thanh-toan-qr-xuyen-bien-gioi-mo-rong-du-dia-cho-du-lich-ban-le-85837.html)
    - [Thanh toán QR xuyên biên giới: từ kết nối được đến sử dụng hiệu quả – VNBA](https://vnba.org.vn/vi/thanh-toan-qr-xuyen-bien-gioi--tu--ket-noi-duoc--den--su-dung-hieu-qua-23681.htm)
    - [Rào cản thiết bị, chi phí của cửa hàng địa phương – VCCI](https://vcci.com.vn/news/thanh-toan-xuyen-bien-gioi-ha-tang-mem-mo-rong-khong-gian-ban-le-va-kich-cau-du-lich)
    - [QR xuyên biên giới Việt Nam – Trung Quốc – Đại biểu Nhân dân](https://daibieunhandan.vn/chinh-thuc-trien-khai-dich-vu-thanh-toan-xuyen-bien-gioi-qua-ma-qr-giua-viet-nam-va-trung-quoc-10397911.html)
    - [GLN kết nối mạng QR quốc gia Việt Nam qua NAPAS – IBS Intelligence](https://ibsintelligence.com/ibsi-news/gln-launches-nationwide-qr-payments-in-vietnam-via-napas/)
    - [Ra mắt thanh toán xuyên biên giới Việt Nam – Singapore – NHNN](https://sbv.gov.vn/en/w/ch%C3%ADnh-th%E1%BB%A9c-ra-m%E1%BA%AFt-d%E1%BB%8Bch-v%E1%BB%A5-thanh-to%C3%A1n-xuy%C3%AAn-bi%C3%AAn-gi%E1%BB%9Bi-vi%E1%BB%87t-nam-singapore)
    - [NAPAS và VNPAY hợp tác toàn diện – VNBA](https://vnba.org.vn/vi/napas-va-vnpay-hop-tac-toan-dien-mo-rong-he-sinh-thai-so-20931.htm)
    - [Du khách quốc tế thanh toán VNPAY-QR tại MWG – Điện Máy Xanh](https://www.dienmayxanh.com/khuyen-mai/du-khach-quoc-te-de-dang-thanh-toan-tai-mwg-1598740)
    - [Visa và VNPAY hợp tác về VNPAY SoftPOS – Visa](https://vn.review.visa.com/en_VN/about-visa/newsroom/press-releases/visa-and-vnpay-strengthen-partnership-to-advance-contactless-payments-with-vnpay-softpos.html)
    - [VNPAY SoftPOS đạt chuẩn PCI CPoC – VNBA](https://vnba.org.vn/vi/vnpay-dat-chuan-pci-cpoc-cho-cong-nghe-bien-dien-thoai-thanh-may-pos-8740.htm)
    - [Vietcombank ra mắt VCB Tap to Phone – Thị trường Tài chính Tiền tệ](https://thitruongtaichinhtiente.vn/vietcombank-ra-mat-giai-phap-thanh-toan-vcb-tap-to-phone-ung-dung-cong-nghe-softpos-46358.html)
    - VNPAY hợp tác Mastercard cho du khách liên kết thẻ trong app VNPAY: *cần bổ sung nguồn*
    - [MoMo và Alipay+ cho người Việt đi nước ngoài – MoMo](https://www.momo.vn/tin-tuc/khuyen-mai/vi-vu-quoc-te-cung-momo-alipay-quet-ma-thanh-toan-8778)
    - [WeChat red envelope – Wikipedia](https://en.wikipedia.org/wiki/WeChat_red_envelope)
    - [Thị phần Alipay, WeChat Pay 2018 – EqualOcean](https://equalocean.com/news/201902061410-spring-festival-gala-might-be-vent-new-third-party-payment)
    - [KakaoPay 5 triệu người dùng năm đầu – VentureBeat](https://venturebeat.com/commerce/kakao-pay-passes-5m-users-in-its-first-12-months)
    - [Understanding Kakao Pay – Antom](https://knowledge.antom.com/understanding-kakao-pay-the-south-korean-payment-and-lifestyle-app)
    - [Alipay và du lịch inbound Trung Quốc – Jing Daily](https://jingdaily.com/posts/china-inbound-international-tourism-alipay)
    - [Alipay, WeChat Pay mở cho du khách 2023 – China Daily HK](https://www.chinadailyhk.com/hk/article/344048)

## Câu hỏi Tổng giám đốc có thể hỏi xoáy

1. **"VPBank, Sacombank, VIB đã có Visa Accept rồi. VDF làm sau thì khác gì?"** Ở ngân hàng, Visa Accept chỉ là một nút trong app, chờ khách hàng tự bật. VDF đưa sản phẩm đến 200.000 merchant Tendoo qua đội kênh bán thực địa, gắn với bán hàng, sổ sách và trợ lý tư vấn đa ngôn ngữ (slide 6, 12).
2. **"MDR gần như bằng 0 thì VDF kiếm tiền ở đâu?"** Phase 1 là giai đoạn có merchant và chủ thẻ. Doanh thu đến từ thẻ phát hành cho merchant, từ MDR khi merchant nâng lên gói SMB (dưới 1%), từ thanh toán nội địa và dịch vụ AI ở các phase sau (slide 18). Cần số theo kịch bản.
3. **"Hạn mức 8 triệu mỗi giao dịch, 100 triệu mỗi tháng có đủ không?"** Đủ cho phần lớn hộ kinh doanh nhỏ phục vụ du khách. Cửa hàng vượt hạn mức được nâng lên gói SMB, đó cũng là lúc VDF bắt đầu thu MDR.
4. **"NAPAS đã có QR xuyên biên giới, sao VDF lại làm Visa Accept?"** QR chỉ dùng được với khách từ 6 nước đã kết nối. Visa Accept nhận thẻ của khách từ mọi nước, không cần chờ kết nối song phương. QR được xem xét ở Phase 3 qua Visa QR Connector hoặc VietQR Global (slide 5, 19).
5. **"Khách Trung Quốc chủ yếu dùng Alipay, WeChat Pay. Có phục vụ được không?"** Phase 1 chưa phục vụ khách chỉ dùng ví nước mình. Pilot ưu tiên điểm nhiều khách dùng thẻ Visa.
6. **"Đội kênh bán của VTT chính là kênh đã tạo ra merchant ảo. Lần này khác gì?"** Chỉ tiêu theo cửa hàng phát sinh giao dịch, không theo số tài khoản mở.
7. **"Sao không để Tammi làm app thanh toán cho du khách như Alipay?"** Tammi hiện chỉ phục vụ người dùng Việt. Du khách đã có thẻ và app nước họ, nên phía còn thiếu là cửa hàng nhận tiền. Bài học từ WeChat Pay, KakaoPay được áp dụng cho Tammi với người dùng Việt ở Phase 2.
8. **"Làm sao biết GMV tăng là nhờ AI chứ không phải nhờ nhận được thẻ?"** Bước 1a là mốc nền, bước 1b đo phần tăng thêm và tách riêng GMV từ đơn có tương tác với trợ lý (slide 19).
9. **"Nếu Tammi chậm xây Shop, Live thì sao?"** Phase 1 vẫn chạy được vì không cần Tammi.

## Thông tin còn thiếu

| Ưu tiên | Nội dung | Phục vụ slide |
| --- | --- | --- |
| Cao | SDK Visa Accept có tích hợp được vào Tendoo không, hay chỉ chạy trong app của bên phát hành thẻ | 11, 12, 19 |
| Cao | VDF có đủ điều kiện làm bên phát hành thẻ Visa ghi nợ hoặc trả trước cho merchant không | 9, 11, 17 |
| Cao | Visa Accept nhận những loại thẻ nào; có chạy trên iPhone không | 11, 12 |
| Cao | Cơ chế phí Visa Accept: IRF, phí acquirer do ai trả, ai nhận; doanh thu thực của VDF | 11, 18 |
| Cao | Số merchant Tendoo chính xác (tổng, active) | 8, 9 |
| Cao | Chốt phạm vi Phase 1 với Visa và VTT, sau đó đề xuất mốc thời gian | 19, 20 |
| Cao | Ước tính doanh thu theo kịch bản; tỉ lệ merchant nâng lên gói SMB | 18 |
| Trung bình | Kết quả triển khai Visa Accept của VPBank, Sacombank, VIB | 6, 12 |
| Trung bình | Nguồn xác nhận hợp tác VNPAY – Mastercard cho du khách | 6 |
| Trung bình | Cơ cấu phương tiện thanh toán của du khách theo quốc tịch, tỉ lệ dùng thẻ Visa | 3, 12, 19 |
| Trung bình | Chi tiêu bình quân của khách quốc tế cho mua sắm, ăn uống | 3 |
| Trung bình | Ngưỡng go/no-go của KPI GMV cửa hàng | 19 |
| Trung bình | Cơ chế chia doanh thu với VTT | 17, 18 |
| Thấp | Kiểm tra lại số liệu case thế giới (chủ yếu do doanh nghiệp công bố) | 7 |
| Thấp | Kịch bản và video demo | 15 |
