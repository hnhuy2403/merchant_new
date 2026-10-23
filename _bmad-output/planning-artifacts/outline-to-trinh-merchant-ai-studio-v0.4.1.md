# Thanh toán cho khách quốc tế tại merchant VTT – Outline tờ trình phê duyệt chủ trương

Cập nhật: 2026-10-21 · Huyhn8 · v0.4.1

> **Thay đổi ở v0.4** (theo góp ý của chị Xuân, P.DVTK): đổi trục câu chuyện từ "Merchant AI Studio" sang **giải pháp thanh toán cho khách quốc tế**. Merchant AI Studio trở thành một phần trong giải pháp của VDF. Thêm slide về NAPAS, phân tích đối thủ và case thế giới. Mô hình hợp tác chuyển thành hai bên VDF – VTT. Tammi vẫn chỉ phục vụ người dùng Việt. Bản v0.3 lưu tại `outline-to-trinh-merchant-ai-studio-v0.3.md`.
>
> **Chỉnh ở v0.4.1:**
> - Giải pháp thanh toán của VDF **chỉ gồm Tap to Phone và link thanh toán** (dùng khi không chạm được). Chưa triển khai việc khách dùng app nước mình quét QR.
> - Thêm slide 11 so sánh giải pháp thanh toán của VDF với các giải pháp khác.
> - Bỏ slide tóm tắt và đề xuất. Nội dung xin duyệt chuyển xuống slide kiến nghị.
> - Đổi thứ tự phần bối cảnh: thị trường merchant trong nước → du khách quốc tế → cách khách đang trả tiền → NAPAS → đối thủ.
> - Slide NAPAS chỉ nêu các nước đã kết nối.
> - Slide đối thủ thêm VNPAY hợp tác Mastercard, tập trung vào giải pháp đối thủ đã có và khoảng trống cho VDF.

## Thông tin chung

Báo cáo xin Tổng giám đốc VDF **phê duyệt chủ trương** để VDF cung cấp giải pháp và hạ tầng thanh toán cho khách quốc tế tại các merchant của VTT.

- **Hình thức:** slide, họp trực tiếp
- **Thời lượng:** khoảng 25 phút, 20 slide chính và phụ lục
- **Đơn vị đề xuất:** VDF
- **Bối cảnh:** VDF đã có dự án cung cấp nền tảng thanh toán cho Tammi, nhưng bài toán merchant chưa từng được báo cáo Tổng giám đốc. Tài liệu đề xuất v0.1 mới lưu hành nội bộ, chưa làm việc chính thức với Tendoo và Tammi.
- **Thông điệp chính:** VDF giúp merchant Tendoo nhận tiền của khách quốc tế ngay trên điện thoại sẵn có. Khách chạm thẻ hoặc điện thoại vào điện thoại của cửa hàng (Tap to Phone), hoặc trả qua link nếu không chạm được. Kèm theo là trợ lý AI đa ngôn ngữ giúp khách hỏi được, hiểu được rồi mới mua. VTT phát triển merchant. Sau đó mở rộng sang khách Việt trên Tammi.

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
- Từ 01/01/2026 hộ kinh doanh bỏ thuế khoán, chuyển sang tự kê khai (NQ 198/2025/QH15). Đến 14/5/2026 đã có hơn 308.000 hộ kinh doanh đăng ký hóa đơn điện tử từ máy tính tiền, tăng 35% so với cuối 2025 (Bộ Tài chính). Nhu cầu số hóa bán hàng và thanh toán tăng mạnh.
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
    - Thu MDR thẻ quốc tế, cao hơn nội địa.
    - Không phụ thuộc Tammi, chạy được ngay với Tendoo.
- *Cần bổ sung: mức chi tiêu bình quân của khách quốc tế, phần chi cho mua sắm và ăn uống; cơ cấu phương tiện thanh toán theo quốc tịch (thẻ, ví, tiền mặt).*

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
- *Cần bổ sung: khảo sát hoặc số liệu về khó khăn thanh toán của du khách (xin từ NAPAS, tổ chức thẻ).*

### Slide 5 – NAPAS đang triển khai thế nào

- **Mô hình VietQR Global:** ví hoặc app ngân hàng nước ngoài kết nối với NAPAS, merchant nhận tiền VND qua mã VietQR. Có hai chiều: chiều vào (du khách trả tiền tại VN) và chiều ra (người Việt trả tiền ở nước ngoài).
- **Các nước đã kết nối (6 nước):** Thái Lan, Lào, Campuchia, Trung Quốc, Hàn Quốc, Singapore. Đang mở rộng sang Nhật Bản, Ấn Độ, Malaysia.
- Kết luận của slide: QR xuyên biên giới là hướng của quốc gia, nhưng **chỉ phục vụ khách từ các nước đã kết nối**, và mới khoảng 6% điểm chấp nhận. Khách từ các nước còn lại (châu Âu, Mỹ, Úc, Nhật Bản, Ấn Độ…) vẫn phải dùng thẻ quốc tế.

### Slide 6 – Đối thủ đã có giải pháp gì, khoảng trống ở đâu

- **Các giải pháp đối thủ đã có:**

| Đối thủ | Giải pháp cho khách quốc tế | Hạn chế |
| --- | --- | --- |
| **VNPAY** – QR | Khách Trung Quốc, Hàn Quốc, Thái Lan, Lào, Campuchia, Singapore quét VNPAY-QR bằng app nước mình (WeChat Pay, Alipay, UnionPay, Toss Pay…). Đã có tại chuỗi Thế Giới Di Động, Điện Máy Xanh, TopZone (từ 9/2026) | Chỉ khách từ các nước đã kết nối; tập trung chuỗi lớn |
| **VNPAY** – app cho du khách | Hợp tác Mastercard: khách quốc tế tải app VNPAY, liên kết thẻ rồi quét QR thanh toán *(cần nguồn xác nhận)* | Khách phải tải thêm app, đăng ký, liên kết thẻ trong chuyến đi ngắn |
| **VNPAY** – SoftPOS | Biến điện thoại Android thành máy nhận thẻ không tiếp xúc (Visa, Apple Pay, Google Pay, Samsung Pay), đạt chuẩn PCI CPoC | Là app thanh toán riêng, không gắn với quản lý bán hàng của hộ kinh doanh |
| **Ngân hàng** (VCB Tap to Phone…) | Cửa hàng nhận thẻ không tiếp xúc trên điện thoại Android | Chủ tiệm dùng thêm một app riêng; chưa có phương án khi khách không chạm được |
| **MoMo** | Tập trung chiều ra (người Việt dùng MoMo quét Alipay+ ở nước ngoài), làm du lịch cùng Saigontourist | Chưa phục vụ du khách trả tiền tại VN |
| **Phần mềm bán hàng** (KiotViet, Sapo, MISA) | Quản lý bán hàng, có kết nối máy POS hoặc QR nội địa | Chưa có giải pháp riêng cho khách quốc tế |

- **Khoảng trống để VDF giải quyết:**
    1. **Thanh toán tách khỏi bán hàng:** các giải pháp nhận thẻ đều là app riêng, chủ tiệm phải ghi sổ lại bằng tay.
    2. **Mới giúp khách trả tiền, chưa giúp khách mua:** khách không hỏi được, không hiểu sản phẩm thì không mua. Chưa giải pháp nào giải quyết rào cản ngôn ngữ.
    3. **Hộ kinh doanh nhỏ ở điểm du lịch chưa được phủ:** đối thủ đi qua chuỗi lớn trước.
    4. **Thiếu phương án dự phòng:** khi khách không có thẻ chạm hoặc chạm lỗi, giao dịch mất.
- *Cần nghiên cứu thêm: nguồn xác nhận hợp tác VNPAY – Mastercard; số điểm chấp nhận và phí MDR quốc tế của VNPAY; chính sách cho hộ kinh doanh nhỏ; các trung gian khác (9Pay, AppotaPay).*

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

- **Doanh thu từ phí giao dịch thẻ quốc tế:** bắt đầu tại quầy (Tap to Phone, link thanh toán), sau đó là thanh toán online.
- **Lấp khoảng trống đối thủ chưa phủ:** hộ kinh doanh nhỏ ở điểm du lịch, cần cả nhận tiền lẫn giao tiếp với khách, và cần thanh toán gắn với sổ sách.
- **Có sẵn tệp merchant:** 200.000 merchant Tendoo và đội kênh bán thực địa của VTT, không phải đi tìm merchant từ đầu như đối thủ.
- **Mở rộng quan hệ chiến lược với VTT:** từ "cung cấp thanh toán cho Tammi" (dự án đang chạy) lên thành "đồng kiến tạo lớp thương mại".

## Phần III – Giải pháp (khoảng 9 phút)

### Slide 10 – Giải pháp tổng thể

- Định nghĩa trong một câu: *VDF cung cấp cho merchant Tendoo cách nhận tiền của khách quốc tế ngay trên điện thoại, trong app Tendoo, kèm trợ lý AI đa ngôn ngữ, sau đó mở rộng sang bán cho khách Việt trên Tammi.*
- Minh họa: sơ đồ "Sau" vẽ lại với **thanh toán của VDF ở trung tâm**. Ba lớp:
    1. **Thanh toán VDF:** Tap to Phone và link thanh toán cho thẻ quốc tế; thanh toán nội địa đa nguồn tiền ở giai đoạn sau.
    2. **Merchant AI Studio:** trợ lý AI tư vấn và bán hàng, tạo từ dữ liệu cửa hàng có sẵn trên Tendoo.
    3. **Kênh khách hàng:** du khách quốc tế tại cửa hàng (làm ngay), người dùng Tammi (mở rộng sau).
- Mục tiêu cốt lõi: **tăng dòng tiền cho merchant Tendoo**. Mọi giao dịch đi qua thanh toán VDF và tự ghi sổ trên Tendoo.

### Slide 11 – Giải pháp chi tiết 1: thanh toán cho khách quốc tế tại cửa hàng

- **Hai cách nhận tiền, tích hợp sẵn trong app Tendoo:**
    - **Tap to Phone:** khách chạm thẻ quốc tế (Visa, Mastercard…) hoặc điện thoại, đồng hồ có Apple Pay, Google Pay vào điện thoại của cửa hàng. Không cần máy POS.
    - **Link thanh toán:** khi khách không có thẻ chạm hoặc chạm không được, cửa hàng gửi link hoặc mã để khách nhập thẻ trên điện thoại của mình.
- **Luồng của merchant:** đăng ký trong Tendoo → xác thực → bật nhận thẻ quốc tế → nhận tiền VND về tài khoản. Giao dịch tự ghi sổ, phục vụ kê khai thuế.
- **Luồng của du khách:** chọn hàng → chạm thẻ hoặc mở link → xem giá quy đổi sang tiền nước mình → nhận hóa đơn điện tử.
- *Cần xác nhận: ngân hàng thanh toán (acquirer) và đối tác SoftPOS; các loại thẻ được nhận (Visa, Mastercard, JCB, UnionPay, Amex); hỗ trợ iPhone hay chỉ Android có NFC; mức MDR.*

### Slide 12 – Vì sao giải pháp thanh toán của VDF vượt trội

| Tiêu chí | Máy POS ngân hàng | Tap to Phone của ngân hàng, VNPAY SoftPOS | QR xuyên biên giới (VietQR Global, VNPAY-QR) | App VNPAY cho du khách (liên kết Mastercard) | **VDF: Tap to Phone + link trong Tendoo** |
| --- | --- | --- | --- | --- | --- |
| Khách từ nước nào cũng trả được | Có (thẻ) | Có (thẻ, ví chạm) | Chỉ 6 nước đã kết nối | Có, nếu có thẻ Mastercard | **Có (thẻ, ví chạm, nhập thẻ qua link)** |
| Khách không phải cài thêm app | Có | Có | Có (dùng app nước mình) | Không, phải tải và đăng ký | **Có** |
| Cửa hàng không cần mua thiết bị | Không | Có | Có | Có | **Có** |
| Cửa hàng không cần thêm app riêng | Không có app nhưng phải có máy | Phải dùng app riêng | Phải dùng app ngân hàng, VNPAY | Phải có mã QR VNPAY | **Có, nằm ngay trong Tendoo** |
| Giao dịch tự ghi sổ bán hàng, phục vụ thuế | Không | Không | Một phần | Không | **Có** |
| Có phương án khi không chạm được | Quẹt, cắm chip | Không | Không áp dụng | Không áp dụng | **Có (link thanh toán)** |
| Tư vấn khách bằng tiếng nước họ | Không | Không | Không | Không | **Có (trợ lý AI, slide 13)** |
| Tiếp cận hộ kinh doanh nhỏ | Ít | Trung bình | Thấp (6% điểm) | Phụ thuộc mạng lưới VNPAY | **200.000 merchant Tendoo, đội kênh bán VTT** |

- Thông điệp: *đối thủ giúp khách trả được tiền; VDF giúp cửa hàng nhận được tiền của mọi du khách ngay trên điện thoại, không thêm app, không ghi sổ lại, và giúp khách hỏi được rồi mới mua.*
- **Điểm yếu cần nói thật:** chưa phục vụ khách chỉ dùng ví nước mình như Alipay, WeChat Pay (phần lớn khách Trung Quốc). Đề xuất xem xét bổ sung QR xuyên biên giới ở phase sau (slide 19).
- *Ghi chú trên slide: đánh giá sơ bộ theo thông tin công khai đến 10/2026. Cần kiểm tra lại bảng trước khi trình.*

### Slide 13 – Giải pháp chi tiết 2: trợ lý AI tư vấn khách quốc tế tại cửa hàng

- Khách quét QR tại cửa hàng để mở trang web của trợ lý, không cần cài app. Trợ lý nói nhiều ngôn ngữ (Trung, Hàn, Anh…).
- Trợ lý giải đáp về sản phẩm, giá, cách dùng theo dữ liệu cửa hàng trên Tendoo; nhận đặt hàng thay nhân viên; gửi link thanh toán ngay trong cuộc trò chuyện.
- Chủ tiệm tạo trợ lý trong vài phút từ dữ liệu cửa hàng sẵn có.

### Slide 14 – Giải pháp chi tiết 3: mở rộng sang khách Việt trên Tammi

- Các trợ lý online trên Tammi (nêu ngắn, triển khai ở các phase sau):
    - Trợ lý bán hàng trên OA cửa hàng: trực tin nhắn ngoài giờ, tạo đơn trong chat.
    - Trợ lý livestream: trả lời và tạo đơn khi live.
    - Trợ lý Tammi OA: đặt món nhóm, tìm hàng nhiều shop.
- Thanh toán đa nguồn tiền của VDF ngay trong chat: Viettel Money, tài khoản ngân hàng, thẻ nội địa và quốc tế.
- Đơn, kho, sổ sách tự đồng bộ về Tendoo.

### Slide 15 – Demo

- Khoảng 2–2,5 phút, kịch bản tập trung vào du khách: khách Hàn Quốc vào cửa hàng ở Hội An, quét QR hỏi trợ lý bằng tiếng Hàn, đặt hàng, chạm thẻ vào điện thoại của chủ tiệm, đơn tự ghi sổ trên Tendoo.
- *Kịch bản chi tiết bổ sung sau.*

### Slide 16 – Vì sao Viettel làm được

- Ba lợi thế mà đối thủ không có đủ cả chuỗi:
    - **Có sẵn merchant và đội kênh bán:** 200.000 merchant Tendoo và đội kênh bán thực địa của VTT.
    - **Thanh toán gắn với quản lý bán hàng:** giao dịch tự ghi sổ trên Tendoo, phục vụ kê khai thuế.
    - **Trợ lý biết hành động:** tư vấn đa ngôn ngữ, tạo đơn, gửi link thanh toán, đồng bộ kho.
- Thêm cho giai đoạn sau: kênh người mua Việt của Tammi, đã xác thực bằng thuê bao.

## Phần IV – Mô hình hợp tác (khoảng 3 phút)

### Slide 17 – Mô hình hợp tác và vai trò hai bên

| Bên | Vai trò |
| --- | --- |
| **VDF** | Cung cấp **giải pháp và hạ tầng thanh toán merchant quốc tế**: Tap to Phone và link thanh toán thẻ quốc tế (cùng ngân hàng đối tác), thanh toán nội địa đa nguồn tiền ở giai đoạn sau; Merchant AI Studio và các mẫu trợ lý; hỗ trợ, vận hành, đối soát |
| **VTT** (Tendoo, Tammi) | **Phát triển merchant**: tích hợp giải pháp vào app Tendoo, cung cấp dữ liệu hàng hóa và đơn, tuyển và hỗ trợ cửa hàng qua đội kênh bán; Tammi xây lớp thương mại cho người dùng Việt ở các phase sau |

- Đối tác bên ngoài: ngân hàng thanh toán, đối tác SoftPOS, tổ chức thẻ.
- Hiện trạng: chưa làm việc chính thức với VTT. Đây là lý do của nội dung xin duyệt số 2.
- Các điểm cần thống nhất: chia sẻ doanh thu, quyền sở hữu dữ liệu, chi phí vận hành, chỉ tiêu kênh bán.
- *Chưa rõ: Viettel Post (giao hàng), Viettel Telecom, Viettel AI.*

### Slide 18 – Mô hình doanh thu và ước tính sơ bộ

| Dòng thu | Phase |
| --- | --- |
| MDR thẻ quốc tế qua Tap to Phone và link thanh toán tại quầy | 1 |
| MDR thanh toán trong chat: Viettel Money, tài khoản ngân hàng, thẻ nội địa | 2 |
| Thanh toán trên Tammi Shop và livestream | 2 |
| QR xuyên biên giới cho khách dùng ví nước mình (nếu triển khai) | 3 |
| Chia tiền nhóm, thanh toán gộp nhiều shop | 3 |
| Thanh toán xuyên biên giới cho người Việt ra nước ngoài | 3 |

- Ước tính theo 3 kịch bản (thận trọng, cơ sở, tích cực). Công thức: số merchant hoạt động × số đơn mỗi tháng × giá trị đơn trung bình × MDR, tách riêng nội địa và thẻ quốc tế.
- Mở rộng sau: gói dịch vụ AI cho người bán. *Cần thống nhất bên nào thu.*
- *Cần bổ sung: dự phóng năm 1–3.*

## Phần V – Lộ trình và kiến nghị (khoảng 3,5 phút)

### Slide 19 – Lộ trình triển khai và pilot

| Phase | Trọng tâm | Phụ thuộc |
| --- | --- | --- |
| 0 – Chuẩn bị | Làm việc với VTT, chốt phạm vi và đầu mối; chốt ngân hàng thanh toán và đối tác SoftPOS; nhận API và dữ liệu mẫu của Tendoo | Đồng thuận của VTT; ngân hàng, đối tác SoftPOS |
| 1 – Pilot khách quốc tế | **Bước 1a:** mở Tap to Phone và link thanh toán thẻ quốc tế cho merchant Tendoo. **Bước 1b:** bật trợ lý tư vấn đa ngôn ngữ tại cửa hàng | Tendoo, VDF và ngân hàng đối tác; không cần Tammi |
| 2 – Mở rộng | Nhân rộng ra các điểm du lịch qua đội kênh bán VTT; trợ lý trên OA cửa hàng và livestream cho người dùng Việt trên Tammi | Tammi tích hợp AI vào OA, xây Shop và Live |
| 3 – Hệ sinh thái | Xem xét QR xuyên biên giới cho khách dùng ví nước mình; Tammi OA đầy đủ; thanh toán cho người Việt ra nước ngoài | NAPAS, giấy phép, đối tác thanh toán xuyên biên giới |

- **Pilot:** một nhóm cửa hàng đông khách quốc tế (ví dụ Hội An, Đà Nẵng, Phú Quốc), merchant vừa và nhỏ, hộ kinh doanh, mọi ngành hàng. Ưu tiên điểm có nhiều khách dùng thẻ (Hàn Quốc, châu Âu, Mỹ, Úc). Chỉ tiêu kênh bán theo **cửa hàng phát sinh giao dịch**, không theo số tài khoản mở.
- **KPI chính: GMV của cửa hàng qua thanh toán VDF**, tách riêng phần thẻ quốc tế. GMV ở bước 1a là mốc nền, bước 1b đo phần tăng thêm từ các đơn có tương tác với trợ lý. Theo dõi tỉ lệ cửa hàng còn giao dịch sau 30 ngày.
- *Cần bổ sung: mốc thời gian từng phase (sau khi chốt phạm vi); ngưỡng go/no-go.*

### Slide 20 – Kiến nghị và bước tiếp theo

- **Ba nội dung xin duyệt** (đề xuất, cần chốt):
    1. Chấp thuận chủ trương VDF cung cấp giải pháp và hạ tầng thanh toán cho khách quốc tế tại merchant VTT, trong đó có Merchant AI Studio.
    2. Giao VDF làm đầu mối làm việc và đàm phán hợp tác với VTT (Tendoo, Tammi): phân vai, chia sẻ doanh thu, dữ liệu.
    3. Phê duyệt lộ trình và mốc thời gian triển khai Phase 0 và Phase 1 (pilot khách quốc tế).
- **Ba rủi ro chính và hướng xử lý:**
    - Merchant không dùng thật: chỉ tiêu kênh bán theo cửa hàng có giao dịch.
    - Đối thủ VNPAY đi trước: tập trung hộ kinh doanh nhỏ, khác biệt bằng thanh toán nằm trong Tendoo, trợ lý AI và sổ sách.
    - Phối hợp nhiều đơn vị: giao VDF làm đầu mối.
- Các việc trong 30, 60 và 90 ngày tới nếu được duyệt, bắt đầu bằng buổi làm việc VDF – VTT và chốt ngân hàng đối tác.

## Phụ lục

- Rủi ro chi tiết và hướng xử lý:

| Rủi ro | Hướng xử lý |
| --- | --- |
| Merchant vẫn không dùng thật | Chỉ tiêu kênh bán theo cửa hàng có giao dịch; pilot đo GMV và tỉ lệ còn giao dịch sau 30 ngày |
| VNPAY và ngân hàng đã có giải pháp nhận thẻ, QR quốc tế | Tập trung hộ kinh doanh nhỏ của Tendoo; khác biệt bằng thanh toán trong Tendoo, link dự phòng, trợ lý đa ngôn ngữ, sổ sách tự động |
| Khách chỉ dùng ví nước mình (Alipay, WeChat Pay) chưa trả được | Pilot ưu tiên điểm nhiều khách dùng thẻ; xem xét QR xuyên biên giới ở Phase 3 |
| Điện thoại của cửa hàng không hỗ trợ NFC | Dùng link thanh toán; xác nhận danh sách thiết bị hỗ trợ |
| Phụ thuộc lộ trình Tammi (tích hợp AI vào OA, Shop, Live) | Phase 1 không cần Tammi |
| Tammi chưa hình thành thói quen mua sắm | Kiểm chứng ở Phase 2 trước khi đầu tư lớn |
| Phối hợp và tích hợp nhiều đơn vị | Giao VDF làm đầu mối (nội dung xin duyệt số 2) |
| Pháp lý AI: Luật Trí tuệ nhân tạo 134/2025 | Luôn gắn nhãn "Trợ lý AI" và nút "Gặp người thật" |
| Dữ liệu cá nhân: Nghị định 13/2023 | Chỉ dùng dữ liệu khi người dùng đồng ý; khách quốc tế dùng web không cần đăng ký; dữ liệu lưu tại Việt Nam |
| AI tư vấn sai, giao dịch sai | Chỉ trả lời theo dữ liệu cửa hàng; trợ lý không tự trừ tiền; khiếu nại, hoàn tiền luôn chuyển người thật |
| Gian lận thẻ qua link thanh toán | Xác thực 3-D Secure; hạn mức giao dịch; theo dõi giao dịch bất thường cùng ngân hàng đối tác |

- Bảng so sánh chi tiết với phần mềm bán hàng và nền tảng thương mại (KiotViet, Sapo, MISA, Pancake/Botcake, Zalo OA, TikTok Shop, Shopee).
- Đối tác chính của NAPAS theo từng thị trường (UnionPay, Alipay, GLN, Liquid Group và các ngân hàng quyết toán).
- Trải nghiệm chi tiết theo persona: chị Lan (cửa hàng trà ở Hội An), Minh (người dùng Tammi), anh Kim Min-jun và chị Camille Laurent (du khách).
- Ví dụ theo ngành hàng: ăn uống, thời trang, quà lưu niệm, mỹ phẩm và nhà thuốc, spa, tạp hóa.
- Kiến trúc và điểm tích hợp Tendoo – Studio – Tammi – thanh toán VDF – ngân hàng đối tác.
- Giá trị cho từng bên: người bán, khách quốc tế, người dùng Tammi, Tendoo, Tammi, VDF.
- Bộ KPI đầy đủ, giả định tài chính.
- Nguồn số liệu:
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

1. **"VNPAY đã có SoftPOS, QR cho du khách, còn hợp tác cả Mastercard. VDF vào sau thì thắng ở đâu?"** Giải pháp của VNPAY là các app thanh toán riêng, đi qua chuỗi lớn. VDF đặt thanh toán ngay trong Tendoo, tự ghi sổ, có link dự phòng và trợ lý tư vấn đa ngôn ngữ, có sẵn 200.000 merchant và đội kênh bán (slide 6, 12).
2. **"NAPAS đã có QR xuyên biên giới, sao VDF lại làm Tap to Phone?"** QR chỉ dùng được với khách từ 6 nước đã kết nối. Tap to Phone nhận thẻ và ví chạm của khách từ mọi nước, không cần chờ kết nối song phương (slide 5, 12).
3. **"Khách Trung Quốc chủ yếu dùng Alipay, WeChat Pay. Tap to Phone có phục vụ được không?"** Phase 1 chưa phục vụ khách chỉ dùng ví nước mình. Pilot ưu tiên điểm nhiều khách dùng thẻ; QR xuyên biên giới được xem xét ở Phase 3 (slide 12, 19).
4. **"Ngân hàng đã cho merchant nhận thẻ qua app rồi. Cần VDF làm gì?"** Thanh toán nằm ngay trong Tendoo, tự ghi sổ và phục vụ kê khai thuế, không bắt chủ tiệm dùng thêm app. Ngân hàng chỉ giúp khách trả được tiền, VDF giúp khách hỏi được, hiểu được rồi mới mua.
5. **"Đội kênh bán của VTT chính là kênh đã tạo ra merchant ảo. Lần này khác gì?"** Chỉ tiêu theo cửa hàng phát sinh giao dịch, không theo số tài khoản mở.
6. **"Chỉ thu MDR thì doanh thu được bao nhiêu?"** Phase 1 thu MDR thẻ quốc tế, cao hơn nội địa; sau đó mở rộng nội địa, Tammi, xuyên biên giới (slide 18). Cần số theo kịch bản.
7. **"Sao không để Tammi làm app thanh toán cho du khách như Alipay?"** Tammi hiện chỉ phục vụ người dùng Việt. Du khách đã có thẻ và app nước họ, nên phía còn thiếu là cửa hàng nhận tiền. Bài học từ WeChat Pay, KakaoPay được áp dụng cho Tammi với người dùng Việt ở Phase 2.
8. **"Làm sao biết GMV tăng là nhờ AI chứ không phải nhờ nhận được thẻ?"** Bước 1a là mốc nền, bước 1b đo phần tăng thêm và tách riêng GMV từ đơn có tương tác với trợ lý (slide 19).
9. **"Nếu Tammi chậm xây Shop, Live thì sao?"** Phase 1 vẫn chạy được vì không cần Tammi.

## Thông tin còn thiếu

| Ưu tiên | Nội dung | Phục vụ slide |
| --- | --- | --- |
| Cao | Số merchant Tendoo chính xác (tổng, active) | 8, 9 |
| Cao | Ngân hàng thanh toán, đối tác SoftPOS; loại thẻ được nhận; hỗ trợ iPhone hay chỉ Android | 11, 12, 19 |
| Cao | Nguồn xác nhận hợp tác VNPAY – Mastercard cho du khách | 6, 12 |
| Cao | Chốt phạm vi Phase 1, sau đó đề xuất mốc thời gian từng phase | 19, 20 |
| Cao | Ước tính doanh thu theo kịch bản, tách nội địa và quốc tế; mức MDR thẻ quốc tế | 18 |
| Trung bình | Cơ cấu phương tiện thanh toán của du khách theo quốc tịch (thẻ, ví, tiền mặt) | 3, 12, 19 |
| Trung bình | Phân tích sâu VNPAY: số điểm chấp nhận, phí, chính sách hộ kinh doanh nhỏ | 6 |
| Trung bình | Chi tiêu bình quân của khách quốc tế cho mua sắm, ăn uống | 3 |
| Trung bình | Số liệu về khó khăn thanh toán của du khách (NAPAS, tổ chức thẻ) | 4 |
| Trung bình | Ngưỡng go/no-go của KPI GMV cửa hàng | 19 |
| Trung bình | Cơ chế chia doanh thu với VTT | 17, 18 |
| Thấp | Kiểm tra lại số liệu case thế giới (chủ yếu do doanh nghiệp công bố) | 7 |
| Thấp | Kịch bản và video demo | 15 |
