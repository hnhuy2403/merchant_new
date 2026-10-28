# Merchant thế hệ mới – Outline trình bày giải pháp

Cập nhật: 2026-10-26 · Huyhn8 · v0.8

> **Thay đổi ở v0.8 (theo feedback của sếp, 25–26/10):**
> - Đổi giải pháp thành **"Merchant thế hệ mới"**, gồm 2 kênh độc lập:
>     - **Offline:** Visa Accept tích hợp trong app Tendoo (chạm thẻ và link thanh toán). VDF chia phí giao dịch với VTT.
>     - **Online:** AI tư vấn du lịch cho khách quốc tế và khách Việt dùng thẻ quốc tế. Doanh thu từ affiliate (merchant trả) và một phần phí giao dịch booking online (đặt phòng khách sạn, đặt bàn nhà hàng).
> - Bỏ Merchant AI Studio, trợ lý AI tại quầy, trợ lý livestream và trợ lý tin nhắn.
> - **Merchant mục tiêu:** merchant vừa và nhỏ. Chỉ riêng booking online có thêm các chuỗi nhà hàng, khách sạn lớn. VTT phát triển merchant cho cả hai kênh, gồm cả các chuỗi lớn.
> - **Cấu trúc mới, 15 slide:** Bìa 1 · Bối cảnh 2–7 (merchant vừa và nhỏ; khách quốc tế; ma trận nhóm merchant × cách khách trả tiền; các giải pháp hiện có; khách tìm và đặt chỗ; vấn đề và cơ hội của VDF) · Giải pháp 8–12 (tổng thể; Visa Accept; demo Visa Accept; AI tư vấn du lịch và booking online; demo kênh online) · Phân vai 13, Nguyên tắc 14, Lộ trình 15.
> - **Bối cảnh (slide 2–6):**
>     - Gộp slide thị trường, xu hướng khách quốc tế với 2 slide khảo sát thành slide 2–3. Slide 2 có biểu đồ tròn phân tệp hộ kinh doanh (không đánh dấu tệp mục tiêu), khoảng 500 nghìn hộ quanh điểm du lịch, ý bỏ thuế khoán và hóa đơn điện tử. Slide 3 thêm nguồn khách theo thị trường 9 tháng 2026; khảo sát 10 khách chỉ nêu insight. Bỏ "30% GDP", livestream 20% và ý AI phổ biến.
>     - Slide 4: ma trận 3 nhóm merchant × các cách khách quốc tế đang trả tiền.
>     - Slide 5: gộp 3 giải pháp hiện có thành một bảng (cách hoạt động, ví dụ, hạn chế), bỏ hình minh họa từng bước. Thêm hạn chế phí Tap to Phone/SoftPOS thông thường của ngân hàng (2,5–3,9% với thẻ khách quốc tế, theo biểu phí VPBank, Techcombank); ghi rõ đây không phải phí Visa Accept.
>     - Slide 6 mới: bối cảnh cho kênh online (khách hỏi AI, đặt chỗ online, nền tảng lớn chỉ giới thiệu merchant của mình).
> - **Slide 7 – Vấn đề và cơ hội của VDF:** gộp slide Vấn đề và Cơ hội thành bảng 2 cột (tại cửa hàng, trước khi khách đến) × 3 dòng. Bỏ "Vấn đề nội tại của Tendoo và Tammi" và các ý gắn với giải pháp cũ. Dải dưới bảng đổi thành "Lợi thế khi VDF hợp tác với VTT".
> - **Giải pháp (slide 8–12):** slide 8 trình bày 2 kênh, khớp 3 tiêu chí ở slide 7 (đến được hộ nhỏ, gắn với bán hàng, chi phí thấp nhờ phí IRF của Visa). Slide 9 viết theo mục 2 tài liệu Visa. Mỗi giải pháp chi tiết có một slide demo ngay sau (`demo-visa-accept/index.html`, `demo-ai-online/index.html`). Slide 11 có kênh khách gặp AI (kênh Viettel, web app); bỏ Visa Intelligent Commerce. Slide 12 là hành trình của Minji ở Đà Nẵng.
> - **Slide 13–15:** phân vai theo 2 kênh; VDF làm mọi việc với Visa (gồm cả nâng gói) và xử lý dòng tiền của cả hai kênh. Slide 14 để trống, bộ phận kinh doanh bổ sung. Lộ trình 3 phase (Q4/2026 – Q4/2027), kênh offline pilot Q1/2027, kênh online pilot Q2/2027; KPI tách theo kênh, là đề xuất chờ xác nhận.
> - **Tách ghi chú:** ghi chú cho người trình chuyển sang `ghi-chu-nguoi-trinh-merchant-ai-studio.md`.
> - **Rà soát nhất quán (26/10):** đổi tên bài theo giải pháp mới; slide 2 không nhắc Visa Accept; thêm dòng kết luận cho slide 11, 13; viết lại Thông tin chung; phụ lục bỏ nội dung của giải pháp cũ (mô hình doanh thu cũ, bài học app chat và thanh toán, so sánh Merchant AI Studio, rủi ro về Tammi và trợ lý); cập nhật bảng Thông tin còn thiếu theo số slide mới. Doanh thu của VDF theo từng kênh bổ sung sau.
>
> Bản v0.7 lưu tại `outline-to-trinh-merchant-ai-studio-v0.7.md`.
>
> **Thay đổi ở v0.7 (theo góp ý trên slide, 23/10):**
> - Bỏ toàn bộ thời lượng (số phút) khỏi outline và slide.
> - Bỏ các ghi chú "Cần bổ sung", "cần nguồn xác nhận" khỏi slide. Các mục còn thiếu chỉ theo dõi ở bảng "Thông tin còn thiếu" cuối outline.
> - Slide 4: chỉ giữ 3 cách khách đang trả tiền và kết luận; số liệu 6%, VietQR Global, VCCI chuyển xuống ghi chú.
> - Slide 6: bỏ bước xác thực khỏi hình minh họa, còn 3 bước trước lần trả tiền đầu tiên.
> - Slide 7: bỏ hạn chế "vẫn thu MDR, chưa xử lý khi không chạm được".
> - Slide 10: không gắn nhãn "giả thuyết" trên slide (giữ trong ghi chú).
> - Slide 11: chưa nhắc Visa Accept; Visa Accept xuất hiện lần đầu ở phần Giải pháp.
> - Slide 12: làm nổi bật 2 giải pháp: thanh toán quốc tế và Merchant AI Studio tư vấn, chốt đơn; bỏ lớp "Kênh khách hàng" khỏi slide.
> - Bỏ slide "Vì sao chọn giải pháp này" khỏi phần chính, chuyển xuống phụ lục. Các slide sau lùi một số: Demo thành slide 16, Phân vai 17, Nguyên tắc 18, Lộ trình 19.
> - Slide 16 (Demo): nhúng nguyên file demo `04_demo/index.html`.
> - Slide 19: tiêu đề "Pilot khách quốc tế từ Q1/2027"; trên slide chỉ giữ bảng lộ trình và KPI chính, chi tiết pilot và chỉ số chuyển xuống ghi chú.
>
> Bản v0.6 lưu tại `outline-to-trinh-merchant-ai-studio-v0.6.md`.
>
> **Thay đổi ở v0.6:** sắp xếp lại mạch trình bày theo 5 phần: Bối cảnh → Vấn đề → Cơ hội của VDF → Giải pháp → Mô hình hợp tác và lộ trình.
> - **Bối cảnh** trình bày 3 nhóm giải pháp đang có ở Việt Nam, mỗi nhóm một slide kèm hình minh họa và hạn chế (slide 5–7): QR thanh toán quốc tế; tải app Việt Nam rồi liên kết thẻ (VNPAY – Mastercard); Tap to Phone (VPBank, Sacombank, VIB với Visa Accept; VNPAY SoftPOS; VCB Tap to Phone).
> - **Vấn đề** gom kết quả khảo sát merchant và khảo sát khách quốc tế, dùng để chứng minh các hạn chế ở phần Bối cảnh. Thêm khảo sát khách quốc tế (10 người, 16/10/2026).
> - **Giải pháp:** gộp bảng so sánh và "Vì sao Viettel làm được" thành một slide ngắn "Vì sao chọn giải pháp này" (slide 16).
> - **Mô hình hợp tác:** chỉ phân vai VTT và VDF, không nói mô hình doanh thu. Lộ trình vẽ thành bảng timeline theo quý (Phase 0 Q4/2026 đến Phase 3 Q4/2027).
> - **Bỏ khỏi phần chính:** slide bài học thế giới, mô hình doanh thu, slide kiến nghị. Mục tiêu của bài là trình bày giải pháp cho Tổng giám đốc, không xin phê duyệt. Bài học thế giới và mô hình doanh thu chuyển xuống phụ lục để dùng khi được hỏi. Rủi ro vẫn ở phụ lục.
>
> - **Bổ sung vế Merchant AI Studio (22/10):** viết lại slide 10 theo vấn đề nội tại (AI của Tendoo hướng vào trong, dữ liệu chưa đến được khách, Tammi chưa có thương mại); thêm cơ hội riêng cho AI ở slide 11; slide 12 dùng hành trình mua tại quầy để nối thanh toán và AI; slide 14 viết lại theo khuôn slide 13; slide 15 thêm bài toán online. Sửa "200.000 merchant Tendoo" thành "hơn 200.000 lượt hộ kinh doanh được hỗ trợ chuyển đổi thuế" theo nguồn công bố. Thống nhất luồng trả tiền tại quầy: chạm thẻ, link chỉ dùng khi không chạm được.
>
> Bản v0.5.2 lưu tại `outline-to-trinh-merchant-ai-studio-v0.5.2.md`.
>
> **Lưu ý bảo mật:** số liệu về Visa Accept (hạn mức, phí, lộ trình nâng gói) lấy từ tài liệu *Visa Confidential*. Chỉ dùng trong tài liệu nội bộ.

## Thông tin chung

Trình bày với Tổng giám đốc VDF về giải pháp "Merchant thế hệ mới": giúp merchant vừa và nhỏ của VTT bán được cho khách quốc tế qua hai kênh độc lập, thanh toán tại cửa hàng (offline) và AI tư vấn du lịch (online).

- **Hình thức:** slide, họp trực tiếp
- **Quy mô:** 15 slide chính và phụ lục
- **Đơn vị:** VDF, phối hợp với VTT (Tendoo, đội kênh bán, kênh viễn thông Viettel)
- **Bối cảnh:** VDF đã có dự án cung cấp nền tảng thanh toán cho Tammi, nhưng bài toán merchant chưa từng được trình bày với Tổng giám đốc. Tài liệu đề xuất v0.1 mới lưu hành nội bộ, chưa làm việc chính thức với Tendoo và Tammi. Visa đã trình bày Visa Accept cho Viettel (10/2026).
- **Thông điệp chính:**
    - **Offline:** VDF đưa Visa Accept vào app Tendoo để merchant vừa và nhỏ nhận thẻ của khách quốc tế ngay trên điện thoại: khách chạm thẻ, hoặc trả qua link nếu không chạm được. Không cần máy POS, chi phí thấp, tiền về gần như tức thì. Merchant lớn lên theo lộ trình nâng gói của Visa.
    - **Online:** AI tư vấn du lịch giới thiệu merchant vừa và nhỏ đến khách quốc tế và khách Việt dùng thẻ quốc tế, cho khách đặt phòng, đặt bàn ngay. Khách gặp AI qua kênh Viettel.
    - VDF cung cấp giải pháp, làm việc với Visa và xử lý dòng tiền; VTT phát triển merchant và đưa khách đến AI.

| Phần | Slide |
| --- | --- |
| Mở đầu | 1 |
| 1. Bối cảnh | 2–7 |
| 2. Giải pháp | 8–12 |
| 3. Mô hình hợp tác và lộ trình triển khai | 13–15 |

**Mạch lập luận:** khách quốc tế tăng nhanh nhưng cửa hàng nhỏ chưa có cách nhận tiền phù hợp → các giải pháp đang có đều còn hạn chế → khách đã hỏi AI và đặt chỗ online, nhưng merchant nhỏ chưa có mặt ở các kênh đó → merchant vừa và nhỏ mất khách ở cả hai đầu: không được khách tìm thấy, và không nhận được tiền khi khách đã ở quầy; đó cũng là hai khoảng trống VDF có cơ hội lấp → giải pháp → VTT và VDF cùng triển khai.

## Mở đầu

### Slide 1 – Trang bìa

- Tên bài (đề xuất): *Merchant thế hệ mới – Thanh toán tại cửa hàng và AI tư vấn du lịch cho merchant VTT*. Đơn vị trình bày (VDF), ngày trình bày.

## Phần 1 – Bối cảnh

### Slide 2 – Merchant vừa và nhỏ: tệp lớn, đang số hóa, chưa nhận được thẻ của khách quốc tế

- Tiêu đề: *Merchant vừa và nhỏ: tệp lớn, đang số hóa, nhưng phần lớn chưa nhận được thẻ của khách quốc tế.*
- **Bố cục:** bên trái là biểu đồ tròn số hộ kinh doanh; bên phải là 2 khối số liệu ngắn (Thị trường, Khảo sát merchant). Mỗi số một dòng.
- **Biểu đồ tròn: 5 triệu hộ kinh doanh** (ghi ở giữa hoặc trên biểu đồ). Biểu đồ chỉ để phân tệp, không tô đậm lát nào làm tệp mục tiêu:

| Lát | Số hộ |
| --- | --- |
| Có địa điểm kinh doanh cố định | 2,03 triệu |
| Đăng ký thuế, không có địa điểm cố định | 1,21 triệu |
| Chưa đăng ký thuế | khoảng 1,76 triệu |

- Chú thích nhỏ dưới biểu đồ: *5 triệu hộ: Báo Chính phủ (2025). 3,24 triệu hộ và cá nhân kinh doanh đăng ký thuế, trong đó 2,03 triệu có địa điểm cố định: Tổng cục Thuế (8/2024).*
- **Thị trường:**
    - Khoảng **500 nghìn** hộ kinh doanh quanh hơn 4.000 điểm du lịch *(ước tính VDF)*
    - Từ 01/01/2026 bỏ thuế khoán; hơn **308 nghìn** hộ đã dùng hóa đơn điện tử từ máy tính tiền (Bộ Tài chính, 5/2026)
    - Cả nước chỉ có **737 nghìn** máy POS, tính cả doanh nghiệp (NHNN, cuối 2024)
    - Chỉ khoảng **6%** điểm chấp nhận thanh toán nhận QR quốc tế (NHNN, 9/2026)
    - Chỉ **42%** doanh nghiệp nhỏ nhận thẻ; nhóm nhận thẻ có **79%** tăng doanh thu, so với 46% ở nhóm không nhận thẻ (Visa, 2023)
- **Khảo sát 132 merchant phục vụ khách quốc tế tại Hà Nội và TP.HCM (7/2026):**
    - **78%** có trên một nửa khách là khách quốc tế
    - **48,5%** coi phí POS (3–5%) là rắc rối lớn nhất
    - **58%** sẵn sàng dùng giải pháp thanh toán mới
- Kết luận của slide (1 dòng): **Tệp lớn, đang số hóa, nhưng phần lớn chưa nhận được thẻ. Đây là khoảng trống cần một cách nhận thẻ phù hợp với hộ kinh doanh nhỏ.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 2.*

### Slide 3 – Khách quốc tế: tăng nhanh, chi nhiều, quen trả không tiền mặt

- Tiêu đề: *Khách quốc tế tăng nhanh, chi tiêu nhiều, quen trả không tiền mặt, nhưng khó trả tiền ở cửa hàng nhỏ.*
- **Bố cục:** 3 khối.
- **Khối 1 – Quy mô** (mỗi số một dòng):
    - **17,7 triệu** lượt trong 9 tháng 2026, tăng 14,5%
    - Mỗi lượt khách chi khoảng **700–1.150 USD**
    - Khoảng **5–8 tỷ USD/năm** chi cho ăn uống và mua sắm
- **Khối 2 – Khách đến từ đâu** (biểu đồ cột ngang 6 thị trường lớn nhất, 9 tháng 2026; màu cột theo cách trả tiền phổ biến ở nước của khách; thị trường chưa có số liệu tô màu trung tính, ô trống trong bảng là chưa có số liệu):

| Thị trường | Lượt khách | Tỉ trọng | So với cùng kỳ | Cách trả tiền phổ biến ở nước của khách |
| --- | --- | --- | --- | --- |
| Trung Quốc | 3,9 triệu | 22% | +1,5% | Ví (Alipay, WeChat Pay) |
| Hàn Quốc | 3,0 triệu | 17% | −5,5% | Thẻ |
| Nga | 1,1 triệu | 6% | +160,6% | Thẻ nội địa Mir |
| Đài Loan | 964 nghìn | 5% | +4,1% | |
| Mỹ | 764 nghìn | 4% | | Thẻ |
| Nhật Bản | 674 nghìn | 4% | | Tiền mặt còn nhiều, thẻ |

- Dòng dưới biểu đồ: *Tăng nhanh nhất: châu Âu +55%, châu Mỹ +20%, châu Úc +21%, Ấn Độ +33%.*
- **Khối 3 – Khảo sát khách quốc tế (16/10/2026):** chỉ nêu insight, không nêu số.
    - Khách vẫn phải mang tiền mặt cho chi tiêu hằng ngày.
    - Khi cửa hàng không nhận thẻ, khách phải xoay xở: nhờ người khác trả hộ, đi rút hoặc đổi tiền; có khách sang cửa hàng khác.
    - Khó trả tiền nhất ở quán ăn, quán cà phê và điểm tham quan.
    - Khách sẵn sàng dùng cách trả tiền mới nếu tiện.
- Chú thích nhỏ dưới khối 3: *khảo sát thăm dò.*
- Kết luận của slide (1 dòng): **Khách có tiền và muốn trả không tiền mặt. Cửa hàng không nhận được thẻ thì mất khách.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 3.*

### Slide 4 – Khách quốc tế đang trả tiền thế nào, theo từng nhóm merchant

- Tiêu đề: *Merchant càng nhỏ, khách quốc tế càng ít cách trả tiền.*
- **Bố cục:** ma trận, hàng là phương thức khách đang trả, cột là 3 nhóm merchant. Mỗi ô chỉ có một ký hiệu (● phổ biến, ◐ có nhưng hạn chế, ○ gần như không có), kèm tối đa 3–4 chữ khi cần.

| Khách trả bằng | **Vừa và nhỏ, cá nhân**<br>*quán ăn, cà phê, quầy lưu niệm, sạp chợ, homestay* | **Trung bình**<br>*nhà hàng, cửa hàng có mặt bằng, spa, khách sạn nhỏ* | **Lớn (chuỗi)**<br>*khách sạn chuỗi, trung tâm thương mại, chuỗi bán lẻ, chuỗi nhà hàng* |
| --- | --- | --- | --- |
| **Tiền mặt, đổi ngoại tệ** | ● gần như duy nhất | ● | ◐ |
| **Thẻ quốc tế qua máy POS** | ○ không có máy, ngại phí | ◐ có máy, thường cộng phụ phí | ● |
| **QR quốc tế** (khách quét bằng ví, app nước mình) | ○ | ○ | ◐ chỉ ở chuỗi lớn |
| **App Việt Nam liên kết thẻ**, quét QR nội địa | ◐ cửa hàng có QR, khách ít khi dùng | ◐ | ◐ |
| **Tap to Phone** | ○ | ◐ chủ yếu qua app ngân hàng | ◐ chủ yếu qua app ngân hàng |

- Kết luận của slide (1 dòng): **Nhóm lớn đã nhận được thẻ. Nhóm vừa và nhỏ, đông nhất, vẫn chủ yếu nhận tiền mặt.** Ba giải pháp mới đang có trên thị trường (slide 5) chưa lấp được khoảng trống này.
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 4.*

### Slide 5 – Các giải pháp hiện có và hạn chế

- Tiêu đề: *Ba giải pháp đang có trên thị trường đều chưa đến được merchant vừa và nhỏ.*
- **Bố cục:** 3 cột, mỗi cột một giải pháp. Mỗi cột gồm: tên giải pháp, một câu giải thích cách hoạt động, ví dụ (chữ nhỏ), 1–2 hạn chế. Không dùng hình minh họa theo từng bước.

| | **1. QR thanh toán quốc tế** | **2. App Việt Nam liên kết thẻ** | **3. Tap to Phone của ngân hàng** |
| --- | --- | --- | --- |
| **Cách hoạt động** | Khách quét QR của cửa hàng bằng ví hoặc app ngân hàng nước mình; cửa hàng nhận tiền VND | Khách tải app thanh toán Việt Nam, đăng ký, liên kết thẻ quốc tế rồi quét QR nội địa | Điện thoại Android của cửa hàng thành máy nhận thẻ; khách chạm thẻ hoặc ví trên điện thoại |
| **Ví dụ** | NAPAS VietQR Global, VNPAY-QR | VNPAY hợp tác Mastercard | VPBank, Sacombank, VIB (Visa Accept); VNPAY SoftPOS; VCB Tap to Phone |
| **Hạn chế** | • Chỉ dùng được với khách từ 6 nước đã kết nối; khách châu Âu, Mỹ, Úc, Nhật Bản, Ấn Độ chưa dùng được<br>• Mới khoảng 6% điểm chấp nhận thanh toán nhận QR quốc tế, chủ yếu ở chuỗi lớn | • Khách phải tải app, đăng ký, liên kết thẻ ngay tại quầy, chỉ để dùng trong một chuyến đi ngắn<br>• Rào cản ở lần dùng đầu tiên, khách thường không chịu làm | • Tap to Phone/SoftPOS thông thường của ngân hàng thu phí cao với thẻ của khách quốc tế: **2,5–3,9%** mỗi giao dịch, cộng phí duy trì đến 50.000đ/tháng (biểu phí VPBank, Techcombank; không phải phí Visa Accept)<br>• Tách khỏi việc bán hàng, chủ tiệm phải ghi sổ lại bằng tay |

- Kết luận của slide (1 dòng): **Thị trường không thiếu phương thức thanh toán, mà thiếu một giải pháp đến được hộ kinh doanh nhỏ, gắn với việc bán hàng và chi phí thấp.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 5.*

### Slide 6 – Khách tìm và đặt chỗ thế nào

- Tiêu đề: *Khách đã hỏi AI và đặt chỗ online, nhưng merchant vừa và nhỏ chưa có mặt ở các kênh đó.*
- **Bố cục:** 3 khối, mỗi số một dòng.
- **Khối 1 – Khách đã chuyển sang hỏi AI khi lên kế hoạch:**
    - **56%** khách Mỹ đã dùng AI cho ít nhất một chuyến đi trong 12 tháng qua, tăng từ 33% ở nửa đầu 2025 (Phocuswright, 3/2026)
    - AI tạo sinh (ChatGPT, Gemini) chiếm **33%** việc tìm hiểu chuyến đi, gần bằng công cụ tìm kiếm (35%) (Phocuswright, 3/2026)
    - **64–69%** khách thế hệ Millennials và Gen Z dùng AI tạo sinh để lên kế hoạch du lịch (Booking.com, 32.800 người ở 34 nước, 2026)
    - **81%** khách Việt dự định dùng AI cho chuyến đi tiếp theo, cao nhất châu Á (trung bình 63%) (Agoda, 3/2026)
- **Khối 2 – Đặt chỗ đã lên mạng, và merchant đang trả phí để có khách:**
    - Du lịch trực tuyến Việt Nam khoảng **4 tỷ USD** năm 2025, tăng 16% (Google, Temasek, Bain, e-Conomy SEA 2025)
    - OTA chiếm khoảng **59%** lượt đặt phòng khách sạn năm 2025
    - Khách sạn trả OTA quốc tế **15–25%** hoa hồng mỗi lượt đặt phòng
    - Khách Việt có **50,2 triệu** thẻ quốc tế (NHNN, quý I/2025)
- **Khối 3 – Nền tảng lớn đã đưa AI vào, nhưng chỉ giới thiệu merchant có trên nền tảng của mình:**
    - Từ 10/2025, Booking.com và Expedia đã có app ngay trong ChatGPT: khách hỏi AI rồi xem và đặt khách sạn tại chỗ. Tripadvisor, TheFork (đặt bàn nhà hàng) công bố sẽ tham gia.
    - Booking.com đã có trợ lý AI lên lịch trình trong app từ 6/2023.
    - Các trợ lý này chỉ gợi ý khách sạn, nhà hàng, hoạt động đã có trên nền tảng. Quán ăn, quán cà phê, quầy lưu niệm vừa và nhỏ ít khi có mặt, nên không được AI giới thiệu.
- Kết luận của slide (1 dòng): **Khách đã hỏi AI trước khi đi và đặt chỗ online. Merchant vừa và nhỏ chưa có mặt ở các kênh này, nên chưa được AI giới thiệu đến khách.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 6.*

### Slide 7 – Vấn đề và cơ hội của VDF

- Tiêu đề: *Merchant vừa và nhỏ đang mất khách ở cả hai đầu. Đó cũng là hai khoảng trống VDF có thể lấp.*
- **Bố cục:** 2 cột theo đúng thứ tự 2 kênh ở slide 8 (cột trái: Offline, cột phải: Online). Mỗi cột có 3 dòng: vấn đề, quy mô và dấu hiệu sẵn sàng, cơ hội cho VDF. Dẫn số từ slide 2–6; số mới duy nhất là mức phí kỳ vọng (81,5%, 24,3%) từ khảo sát merchant. Chưa nhắc Visa Accept. Dưới 2 cột là một dải ngang "Lợi thế khi VDF hợp tác với VTT".

| | **1. Tại cửa hàng** | **2. Trước khi khách đến** |
| --- | --- | --- |
| **Vấn đề** | **Không nhận được tiền của khách.** Nhóm vừa và nhỏ vẫn chủ yếu nhận tiền mặt; chỉ khoảng **6%** điểm chấp nhận thanh toán nhận QR quốc tế (slide 2, 4). Khách phải mang tiền mặt, đi rút hoặc đổi tiền, có khách sang cửa hàng khác (slide 3) | **Không được khách tìm thấy.** Khách đã hỏi AI và đặt chỗ online, nhưng AI của các nền tảng lớn chỉ giới thiệu merchant có trên nền tảng của mình; merchant vừa và nhỏ chưa có mặt (slide 6) |
| **Quy mô và dấu hiệu sẵn sàng** | Khoảng **500 nghìn** hộ quanh điểm du lịch; khách quốc tế chi khoảng **5–8 tỷ USD/năm** cho ăn uống, mua sắm (slide 2, 3). **58%** merchant sẵn sàng dùng giải pháp mới; kỳ vọng phí 1–2% thì **81,5%** sẵn sàng, trên 3% thì chỉ **24,3%** | **56%** khách Mỹ đã dùng AI cho chuyến đi; **81%** khách Việt dự định dùng. Du lịch trực tuyến khoảng **4 tỷ USD**; khách Việt có **50,2 triệu** thẻ quốc tế (slide 6) |
| **Cơ hội cho VDF** | Một cách nhận thẻ đến được hộ kinh doanh nhỏ, gắn với việc bán hàng và chi phí thấp | Một kênh AI tư vấn giới thiệu được cả merchant vừa và nhỏ đến khách, và cho khách đặt chỗ ngay |

- **Lợi thế khi VDF hợp tác với VTT** (dải ngang dưới bảng): có sẵn kênh đến merchant qua tệp hộ kinh doanh Tendoo và đội kênh bán thực địa của VTT, không phải chờ merchant tự tìm đến.
- Kết luận của slide (1 dòng): **Hai vấn đề, hai cơ hội độc lập, cần hai cách giải quyết riêng. Cùng VTT, VDF có kênh đến merchant để lấp cả hai.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 7.*

## Phần 2 – Giải pháp

### Slide 8 – Giải pháp tổng thể

- Tiêu đề: *Merchant thế hệ mới: thanh toán tại cửa hàng và AI tư vấn du lịch online.*
- Định nghĩa trong một câu: *VDF giúp merchant vừa và nhỏ bán được cho khách quốc tế qua hai kênh: tại cửa hàng, merchant nhận thẻ ngay trên điện thoại bằng Visa Accept tích hợp trong app Tendoo; online, AI tư vấn cho khách điểm du lịch, điểm ăn chơi, mua sắm và khách sạn.*
- **Hai kênh, hai thẻ lớn đặt cạnh nhau** (đánh số 1 và 2, không vẽ mũi tên nối giữa hai thẻ):

| | **1. Offline: thanh toán tại cửa hàng** | **2. Online: AI tư vấn du lịch** |
| --- | --- | --- |
| **Merchant** | Merchant vừa và nhỏ | Merchant vừa và nhỏ (điểm ăn chơi, mua sắm)<br>Riêng booking online: thêm các chuỗi nhà hàng, khách sạn lớn |
| **Khách hàng** | Khách quốc tế mua tại cửa hàng | Khách quốc tế và khách Việt dùng thẻ thanh toán quốc tế |
| **Giải pháp** | Visa Accept tích hợp trong app Tendoo, merchant nhận thẻ ngay trên điện thoại:<br>• **Chạm thẻ (Tap to Phone):** cách nhận tiền chính tại quầy<br>• **Link thanh toán:** khi khách không chạm được | AI tư vấn điểm du lịch và các điểm ăn chơi, mua sắm vừa và nhỏ<br>Booking online qua tư vấn của AI: đặt phòng khách sạn, đặt bàn nhà hàng |
| **Kết quả cho merchant** | **Nhận được tiền** của khách quốc tế:<br>• Không cần máy POS<br>• Nhận tiền ngay trong app bán hàng Tendoo<br>• Chi phí thấp: phí IRF của Visa miễn phí với giao dịch dưới 200.000đ, 200đ mỗi giao dịch trên 200.000đ | **Có thêm khách** nhờ được AI giới thiệu |
| **Doanh thu của VDF** | Chia phí giao dịch với VTT | Tiền affiliate do merchant trả<br>Một phần phí giao dịch booking online |

- Hai kênh vận hành độc lập.
- > **Cần review (không đưa lên slide):** phần booking online cho các chuỗi nhà hàng, khách sạn lớn (dòng Merchant, cột Online) chưa có vấn đề và cơ hội tương ứng ở slide 7, vì slide 7 chỉ nói merchant vừa và nhỏ.
- **Đưa giải pháp đến merchant** (dải ngang dưới hai thẻ): VTT phát triển merchant cho cả hai kênh: merchant vừa và nhỏ qua tệp hộ kinh doanh Tendoo và đội kênh bán thực địa; các chuỗi nhà hàng, khách sạn lớn cho booking online.
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 8.*

### Slide 9 – Giải pháp chi tiết 1 (Offline): Visa Accept

- Tiêu đề: *Visa Accept: chủ thẻ Visa thành người bán, nhận thẻ ngay trên điện thoại.*
- **Bố cục:** 4 khối theo mục 2 tài liệu Visa (*VDS – Acquiring discussion*, 10/2026, trang 12–22): (1) Visa Accept là gì, (2) Bán hàng thế nào, (3) Hạn mức và phí, (4) Lộ trình nâng gói. Minh họa: các màn hình mẫu của Visa (bán hàng bằng chạm thẻ, bằng link thanh toán), đặt trong giao diện Tendoo. Chú thích nhỏ cuối slide: *Nguồn: Visa, 10/2026.*
- **Khối 1 – Visa Accept là gì:**
    - Biến người dùng thẻ Visa ghi nợ, trả trước thành người bán: ai cũng nhận được thẻ.
    - Đăng ký nhanh. Trong giải pháp của VDF, Visa Accept tích hợp trong app Tendoo.
    - Nhận thẻ bằng điện thoại có NFC, không cần máy POS.
    - Tiền về gần như tức thì.
- **Khối 2 – Bán hàng thế nào:**
    - **Chạm thẻ (Tap to Phone):** khách chạm thẻ hoặc ví vào điện thoại của cửa hàng.
    - **Link thanh toán:** khi khách không chạm được, merchant gửi link để khách trả bằng thẻ; giao dịch qua link được bảo vệ bằng 3-D Secure.
    - Merchant theo dõi doanh số, lịch sử và chi tiết từng giao dịch; có chức năng hoàn tiền và báo cáo đối soát.
- **Khối 3 – Hạn mức và phí:**

| Hạn mức mỗi tháng | Số giao dịch mỗi tháng | Mỗi giao dịch |
| --- | --- | --- |
| 100 triệu đồng (4.000 USD) | 2.000 | 8 triệu đồng (300 USD) |

| Phí mạng lưới | Giao dịch dưới 200.000đ | Giao dịch từ 200.000đ |
| --- | --- | --- |
| IRF | Miễn phí | 200đ |
| Phí acquirer | Miễn phí | 0,002 USD |

- **Khối 4 – Lộ trình nâng gói của Visa** (vẽ 3 bậc):
    - **Visa Accept:** MDR gần như bằng 0, trong hạn mức ở khối 3.
    - **Gói SMB:** MDR dưới 1%; khoảng 180 triệu đồng (7.000 USD) mỗi tháng, không giới hạn số giao dịch và giá trị mỗi giao dịch.
    - **Nhận thẻ đầy đủ:** biểu phí chuẩn, không giới hạn, dùng nhiều loại thiết bị.
- Kết luận của slide (1 dòng): **Merchant vừa và nhỏ bắt đầu nhận thẻ với chi phí gần như bằng 0, rồi lớn lên theo lộ trình của Visa.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 9.*

### Slide 10 – Demo giải pháp Visa Accept

- Slide nhúng nguyên file demo `demo-visa-accept/index.html` (không có tiêu đề, demo phủ kín slide). Người trình bấm vào demo để thao tác; phím mũi tên khi đó điều khiển demo.
- Màn hình đi theo luồng Visa Accept trong mục 2 tài liệu Visa (trang 14–18, 20, 22), đặt trong app Tendoo. Cửa hàng mẫu: Lan's House, bán trà và quà lưu niệm ở Hội An.
- Năm kịch bản:
    1. **Đăng ký:** mở Visa Accept trong Tendoo, chọn thẻ Visa nhận tiền, đặt tên người bán (hiện trên sao kê của khách), đồng ý điều khoản và hạn mức.
    2. **Chạm thẻ:** tạo đơn từ hàng có sẵn trong Tendoo, du khách Pháp chạm thẻ Visa, thanh toán thành công, giao dịch vào bảng điều khiển và sổ bán hàng.
    3. **Link thanh toán:** du khách Hàn Quốc không chạm được thẻ; chủ tiệm gửi link qua tin nhắn; khách mở trang yêu cầu thanh toán, nhập thẻ, xác thực 3-D Secure; điện thoại chủ tiệm báo đã nhận tiền.
    4. **Theo dõi và hoàn tiền:** lịch sử giao dịch, chi tiết giao dịch, hoàn tiền về thẻ của khách, báo cáo doanh số và đối soát.
    5. **Nâng gói:** chạm hạn mức tháng, được mời lên gói SMB hoặc ở lại Visa Accept; lộ trình 3 bậc của Visa.
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 10.*

### Slide 11 – Giải pháp chi tiết 2 (Online): AI tư vấn du lịch và booking online

- Tiêu đề: *Online: AI tư vấn du lịch giới thiệu merchant vừa và nhỏ đến khách, và cho khách đặt chỗ ngay.*
- **Bố cục:** trên cùng là khách hàng và kênh khách gặp AI; bên trái là 2 việc AI làm cho khách (tư vấn, booking online); bên phải là merchant tham gia và kết quả cho merchant; dải dưới cùng là phần của VDF và VTT.
- **Khách hàng:** khách quốc tế và khách Việt dùng thẻ thanh toán quốc tế.
- **Khách gặp AI qua kênh Viettel:** link mở AI trong tin nhắn chào mừng khi khách roaming vào Việt Nam, trên SIM/eSIM du lịch Viettel và tại quầy bán SIM ở sân bay. AI là web app, khách bấm link là dùng ngay, không cần cài app.
    - Sau pilot: mở thêm cổng du lịch của tỉnh và Tammi.
- **AI làm 2 việc cho khách:**
    - **Tư vấn:** gợi ý điểm du lịch và các điểm ăn chơi, mua sắm vừa và nhỏ.
    - **Booking online:** từ tư vấn của AI, khách đặt phòng khách sạn, đặt bàn nhà hàng.
- **Merchant tham gia:**

| | **Tư vấn** | **Booking online** |
| --- | --- | --- |
| **Merchant** | Merchant vừa và nhỏ: điểm ăn chơi, mua sắm | Khách sạn, nhà hàng vừa và nhỏ; thêm các chuỗi nhà hàng, khách sạn lớn |
| **Kết quả cho merchant** | Có thêm khách nhờ được AI giới thiệu | Có thêm lượt đặt phòng, đặt bàn qua AI |
| **Doanh thu của VDF** | Tiền affiliate do merchant trả | Một phần phí giao dịch booking online |

- **Dải dưới cùng:**
    - **Đưa đến merchant:** VTT phát triển merchant: merchant vừa và nhỏ qua tệp hộ kinh doanh Tendoo và đội kênh bán thực địa; các chuỗi nhà hàng, khách sạn lớn cho booking online.
    - Chính sách affiliate và booking online thống nhất sau khi triển khai.
- Kết luận của slide (1 dòng): **AI đưa khách đến merchant vừa và nhỏ và cho khách đặt chỗ ngay; merchant có thêm khách, VDF có doanh thu từ affiliate và phí booking.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 11.*

### Slide 12 – Demo giải pháp AI tư vấn du lịch và booking online

- Slide nhúng file demo của kênh online tại `demo-ai-online/index.html`, làm sau demo Visa Accept. Demo chạy theo hành trình của một khách, gồm 5 kịch bản: hạ cánh và mở AI (dòng 1–2 trong bảng dưới), hỏi tư vấn, đặt bàn, đặt phòng, kết quả.
- **Nhân vật:** Minji, 28 tuổi, nhân viên văn phòng ở Seoul, đi Đà Nẵng 5 ngày. Minji đã đặt khách sạn ở Đà Nẵng, chưa biết ăn gì, chơi gì, và muốn ghé Hội An 1 đêm.
- **Hành trình:**

| # | Khoảnh khắc | Minji làm gì | AI làm gì |
| --- | --- | --- | --- |
| 1 | **Hạ cánh** ở sân bay Đà Nẵng | Bật điện thoại, nhận tin nhắn chào mừng roaming của Viettel, trong tin có link "Hỏi AI về Đà Nẵng" | |
| 2 | **Mở AI** khi đang chờ hành lý | Bấm link, web app mở ngay, không cần cài app, không cần đăng nhập | Chào Minji, hỏi Minji muốn đi đâu, thích ăn gì |
| 3 | **Hỏi tư vấn** | Hỏi bằng tiếng Hàn: "Tối nay tôi muốn ăn hải sản gần biển Mỹ Khê, mai đi đâu?" | Trả lời bằng tiếng Hàn. Gợi ý 3 quán hải sản vừa và nhỏ gần biển, kèm giờ mở cửa và giá tham khảo; gợi ý lịch trình ngày mai: Ngũ Hành Sơn và một quán cà phê nhỏ trên đường đi |
| 4 | **Đặt bàn** | Chọn 1 quán, đặt bàn 19h cho 2 người, điền thông tin liên hệ và đặt cọc bằng thẻ quốc tế | Gửi lượt đặt cho quán; quán xác nhận qua app Tendoo; AI báo lại Minji |
| 5 | **Đặt phòng** | "Tôi muốn ở Hội An 1 đêm, khách sạn nhỏ gần phố cổ." Chọn khách sạn, điền thông tin và trả trước bằng thẻ quốc tế | Gợi ý vài khách sạn vừa và nhỏ; xác nhận đặt phòng cho Minji |
| 6 | **Kết quả** | Ra khỏi sân bay đã có chỗ ăn tối và chỗ ở Hội An | Quán và khách sạn có thêm khách nhờ AI giới thiệu |

- **Quy tắc thể hiện trong demo:**
    - AI trả lời bằng thứ tiếng khách dùng để hỏi.
    - Hỏi tư vấn không cần đăng nhập; chỉ khi chốt đặt chỗ, thanh toán khách mới điền thông tin.
    - Khách có thể trả trước bằng thẻ quốc tế; đặt bàn có thể trả trước hoặc đặt cọc.
    - Merchant xác nhận lượt đặt qua app Tendoo.
- **Câu chốt khi demo:** *Minji không phải cài app, không phải tự tìm. Từ lúc hạ cánh đến lúc ra khỏi sân bay, Minji đã đặt xong chỗ ăn và chỗ ở tại các merchant vừa và nhỏ.*
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 12.*

## Phần 3 – Mô hình hợp tác và lộ trình triển khai

### Slide 13 – Phân vai VTT và VDF

- Tiêu đề: *VDF cung cấp giải pháp, VTT phát triển merchant và đưa khách đến AI.*
- **Bố cục:** bảng 2 cột theo 2 kênh ở slide 8 (Offline, Online), 2 dòng (VDF, VTT). Dưới bảng là dòng đối tác bên ngoài.

| Bên | **1. Offline: Visa Accept** | **2. Online: AI tư vấn du lịch và booking online** |
| --- | --- | --- |
| **VDF** | Cung cấp Visa Accept trong app Tendoo; **làm việc với Visa**, gồm cả nâng merchant lên các gói cao hơn của Visa (SMB, nhận thẻ đầy đủ)<br>**Xử lý dòng tiền:** vận hành, đối soát, kiểm soát rủi ro | Xây dựng và vận hành AI tư vấn du lịch và booking online (web app)<br>**Xử lý dòng tiền** của booking online: khách trả trước, đặt cọc bằng thẻ quốc tế |
| **VTT** | **Phát triển merchant** qua tệp hộ kinh doanh Tendoo và đội kênh bán thực địa<br>Tích hợp Visa Accept vào app Tendoo | **Phát triển merchant:** merchant vừa và nhỏ qua tệp hộ kinh doanh Tendoo và đội kênh bán thực địa; các chuỗi nhà hàng, khách sạn lớn cho booking online<br>**Đưa khách đến AI** qua kênh Viettel: tin nhắn chào mừng roaming, SIM/eSIM du lịch, quầy SIM sân bay |

- **Đối tác bên ngoài:** Visa (sản phẩm Visa Accept, mạng lưới thẻ, công cụ chống gian lận).
- Kết luận của slide (1 dòng): **VDF lo giải pháp, việc với Visa và dòng tiền; VTT lo merchant và đưa khách đến AI.**
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 13.*

### Slide 14 – Nguyên tắc hợp tác kinh doanh VTT – VDF

- *Để trống. Bộ phận kinh doanh bổ sung sau.*
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 14.*

### Slide 15 – Lộ trình triển khai

- Tiêu đề: *Pilot kênh offline từ Q1/2027, kênh online từ Q2/2027.*

- Vẽ thành bảng timeline: hàng là các mảng việc, cột là các phase theo thời gian.

| Mảng việc | Phase 0 – Chuẩn bị<br>*(Q4/2026)* | Phase 1 – Pilot<br>*(Q1–Q2/2027)* | Phase 2 – Mở rộng<br>*(Q3–Q4/2027)* |
| --- | --- | --- | --- |
| **1. Offline: Visa Accept** | Chốt hợp tác Visa Accept với Visa; thiết kế tích hợp vào Tendoo | **Q1/2027:** mở Visa Accept trong Tendoo (chạm thẻ, link thanh toán) cho nhóm cửa hàng pilot | Nhân rộng; merchant chạm hạn mức nâng lên gói SMB, nhận thẻ đầy đủ theo lộ trình của Visa |
| **2. Online: AI tư vấn và booking** | Thiết kế AI tư vấn du lịch và booking online (web app); thống nhất với VTT về kênh tin nhắn roaming, SIM/eSIM du lịch, quầy SIM sân bay | **Q2/2027:** pilot AI tư vấn và booking online qua kênh Viettel | Nhân rộng; mở thêm cổng du lịch của tỉnh và Tammi |
| **Merchant và kênh bán** | Làm việc với VTT, chốt phạm vi và đầu mối | VTT phát triển merchant pilot tại một nhóm điểm đông khách quốc tế (Hội An, Đà Nẵng, Phú Quốc): kênh offline từ Q1, kênh online từ Q2 | Nhân rộng ra các điểm du lịch qua đội kênh bán VTT, tiến tới phủ các merchant Tendoo phục vụ khách quốc tế |
| **Phụ thuộc** | Đồng thuận của VTT; Visa | VDF, VTT (Tendoo, kênh bán, kênh tin nhắn roaming); Visa | Visa; cổng du lịch tỉnh; Tammi |

- Hai kênh độc lập: kênh online triển khai sau kênh offline một quý, nhưng không có bước nào của kênh này phụ thuộc kênh kia.
- Chính sách phí cho merchant (offline), chính sách affiliate và booking online thống nhất sau khi triển khai; không đặt vào phase nào trên slide.
- Trên slide chỉ giữ bảng lộ trình và dòng kết luận **KPI chính** theo từng kênh:
    - **Offline:** GMV của cửa hàng qua Visa Accept; số cửa hàng phát sinh giao dịch.
    - **Online:** số lượt đặt phòng, đặt bàn qua AI; GMV booking online.
- > **Cần review (không đưa lên slide):**
    > - KPI hai kênh là đề xuất, chờ xác nhận.
    > - Địa bàn pilot kênh online: đang ghi chung với kênh offline (Hội An, Đà Nẵng, Phú Quốc). Demo kênh online đặt ở Đà Nẵng, Hội An.
- *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Slide 15.*

## Phụ lục

- **Rủi ro chi tiết và hướng xử lý:**

| Rủi ro | Hướng xử lý |
| --- | --- |
| Merchant vẫn không dùng thật | Chỉ tiêu kênh bán theo cửa hàng có giao dịch; pilot đo GMV và tỉ lệ còn giao dịch sau 30 ngày |
| VPBank, Sacombank, VIB đã có Visa Accept | Tập trung hộ kinh doanh của Tendoo; khác biệt bằng kênh bán thực địa và thanh toán nằm ngay trong Tendoo |
| Merchant chưa có thẻ Visa để nhận tiền | Đội kênh bán hướng dẫn mở thẻ tại ngân hàng; xem xét hợp tác ngân hàng phát hành để mở thẻ nhanh |
| Chạm thẻ chỉ chạy trên Android | Cửa hàng dùng iPhone nhận tiền qua link |
| Chưa nhận ví nước ngoài (Alipay, WeChat Pay) | Pilot ưu tiên điểm nhiều khách dùng thẻ; QR cho ví nước ngoài chưa nằm trong lộ trình hiện tại |
| Hạn mức Visa Accept thấp với cửa hàng lớn | VDF nâng merchant lên gói SMB, nhận thẻ đầy đủ khi chạm hạn mức |
| Doanh thu giai đoạn đầu thấp vì phí gần như bằng 0 | Đặt mục tiêu Phase 1 là có merchant hoạt động; theo dõi tỉ lệ nâng gói |
| Gian lận thẻ | Kiểm soát tần suất và hạn mức của Visa Accept; xác thực 3-D Secure cho giao dịch qua link; cân nhắc công cụ chống gian lận của Visa khi lên gói đầy đủ |
| Phối hợp nhiều đơn vị | VDF làm đầu mối làm việc với VTT và Visa |
| Pháp lý AI: Luật Trí tuệ nhân tạo 134/2025 | AI tư vấn luôn gắn nhãn "Trợ lý AI" và nút "Gặp người thật" |
| Dữ liệu cá nhân: Nghị định 13/2023 | Chỉ dùng dữ liệu khi người dùng đồng ý; hỏi tư vấn không cần đăng nhập, khách chỉ điền thông tin khi chốt đặt chỗ, thanh toán; dữ liệu lưu tại Việt Nam |
| AI tư vấn sai | AI chỉ gợi ý theo dữ liệu của merchant tham gia; lượt đặt do merchant xác nhận qua Tendoo; khiếu nại, hoàn tiền luôn chuyển người thật |

- **Mô hình doanh thu:** bổ sung sau. Các dòng thu đã chốt (slide 8):

| Kênh | Dòng thu của VDF |
| --- | --- |
| Offline: Visa Accept | Chia phí giao dịch với VTT |
| Online: AI tư vấn du lịch và booking online | Tiền affiliate do merchant trả; một phần phí giao dịch booking online |

    - Mức phí cho merchant, tỉ lệ chia phí với VTT, chính sách affiliate và booking online thống nhất sau khi triển khai.

- **Vì sao chọn giải pháp này – kênh offline** (dùng khi được hỏi):
    - **So sánh nhanh với 3 nhóm giải pháp ở slide 5:**

    | Tiêu chí | QR quốc tế | App Việt Nam + liên kết thẻ | Tap to Phone của ngân hàng | **VDF: Visa Accept trong Tendoo** |
    | --- | --- | --- | --- | --- |
    | Khách nước nào cũng trả được | Không (6 nước) | Có | Có | **Có** |
    | Khách không phải cài thêm app | Có | Không | Có | **Có** |
    | Phí với merchant gần như bằng 0 | Tùy đơn vị cung cấp | Tùy đơn vị cung cấp | Chỉ Visa Accept | **Có** |
    | Gắn với bán hàng, tự ghi sổ | Không | Không | Không | **Có** |
    | Đến tận hộ kinh doanh qua đội kênh bán | Không | Không | Không | **Có** |

    - Thông điệp: *ngân hàng đã có Visa Accept, nhưng chỉ là nút nhận tiền trong app ngân hàng, chờ khách hàng tự bật. VDF đưa Visa Accept vào phần mềm bán hàng của hộ kinh doanh, đến tận cửa hàng qua đội kênh bán VTT.*
    - *Ghi chú cho người trình: xem file `ghi-chu-nguoi-trinh-merchant-ai-studio.md`, mục Phụ lục – Vì sao chọn giải pháp này.*

- **Bảng đối thủ chi tiết:**

| Đối thủ | Giải pháp cho khách quốc tế | Hạn chế |
| --- | --- | --- |
| **VPBank, Sacombank, VIB** – Visa Accept | Đã ra mắt Visa Accept trong app ngân hàng (VPBank TapLink, VIB BizPay…): chủ thẻ Visa thành người bán, nhận thẻ bằng điện thoại, không cần thiết bị | Chỉ là tính năng nhận tiền trong app ngân hàng, chờ khách hàng tự bật; không gắn với quản lý bán hàng; ngân hàng không có đội phát triển merchant thực địa |
| **VNPAY** – QR | Khách Trung Quốc, Hàn Quốc, Thái Lan, Lào, Campuchia, Singapore quét VNPAY-QR bằng app nước mình (WeChat Pay, Alipay, UnionPay, Toss Pay…). Đã có tại chuỗi Thế Giới Di Động, Điện Máy Xanh, TopZone (từ 9/2026) | Chỉ khách từ các nước đã kết nối; tập trung chuỗi lớn |
| **VNPAY** – app cho du khách | Hợp tác Mastercard: khách quốc tế tải app VNPAY, liên kết thẻ rồi quét QR thanh toán *(cần nguồn xác nhận)* | Khách phải tải thêm app, đăng ký, liên kết thẻ trong chuyến đi ngắn |
| **VNPAY** – SoftPOS | Biến điện thoại Android thành máy nhận thẻ không tiếp xúc (Visa, Apple Pay, Google Pay, Samsung Pay), đạt chuẩn PCI CPoC | Là app thanh toán riêng, không gắn với quản lý bán hàng của hộ kinh doanh |
| **Ngân hàng** (VCB Tap to Phone…) | Cửa hàng nhận thẻ không tiếp xúc trên điện thoại Android | Chủ tiệm dùng thêm một app riêng; chưa có phương án khi khách không chạm được |
| **MoMo** | Tập trung chiều ra (người Việt dùng MoMo quét Alipay+ ở nước ngoài), làm du lịch cùng Saigontourist | Chưa phục vụ du khách trả tiền tại VN |
| **Phần mềm bán hàng** (KiotViet, Sapo, MISA) | Quản lý bán hàng, có kết nối máy POS hoặc QR nội địa | Chưa có giải pháp riêng cho khách quốc tế |

- **Bảng so sánh đầy đủ:**

| Tiêu chí | Máy POS ngân hàng | SoftPOS của ngân hàng, VNPAY | Visa Accept trong app ngân hàng (VPBank, Sacombank, VIB) | QR xuyên biên giới (VietQR Global, VNPAY-QR) | **VDF: Visa Accept trong Tendoo** |
| --- | --- | --- | --- | --- | --- |
| Khách từ nước nào cũng trả được | Có (thẻ) | Có (thẻ, ví chạm) | Có (thẻ, ví chạm) | Chỉ 6 nước đã kết nối | **Có (thẻ Visa, Mastercard, ví chạm, link)** |
| Khách không phải cài thêm app | Có | Có | Có | Có | **Có** |
| Cửa hàng không cần mua thiết bị | Không | Có | Có | Có | **Có** |
| Phí với cửa hàng | MDR theo hợp đồng | MDR theo hợp đồng | Gần như 0 | Theo đơn vị cung cấp | **Gần như 0, có lộ trình nâng gói** |
| Tiền về | Theo chu kỳ quyết toán | Theo chu kỳ quyết toán | Gần như tức thì | Theo đơn vị cung cấp | **Gần như tức thì** |
| Có phương án khi không chạm được | Quẹt, cắm chip | Không | Có (link) | Không áp dụng | **Có (link)** |
| Thanh toán nằm ngay trong phần mềm bán hàng, tự ghi sổ | Không | Không | Không | Một phần | **Có (trong Tendoo)** |
| Không phải thêm app, công cụ mới | Không (thêm máy) | Không (thêm app) | Không (dùng app ngân hàng) | Không (thêm mã QR, app nhận tiền) | **Có (dùng ngay Tendoo đang có)** |
| Đối soát, chứng từ, hỗ trợ khiếu nại | Có hóa đơn POS | Lịch sử giao dịch | Lịch sử giao dịch, hoàn tiền | Lịch sử giao dịch | **Gắn với đơn hàng và hóa đơn điện tử trên Tendoo; hoàn tiền, báo cáo đối soát** |
| Kênh đưa giải pháp đến hộ kinh doanh | Nhân viên ngân hàng | Nhân viên ngân hàng, đại lý | Khách hàng tự bật trong app | Ngân hàng, trung gian | **Tệp hộ kinh doanh Tendoo, đội kênh bán VTT** |

- **NAPAS – VietQR Global:** ví hoặc app ngân hàng nước ngoài kết nối với NAPAS, merchant nhận tiền VND qua mã VietQR. Có hai chiều: chiều vào (du khách trả tiền tại VN) và chiều ra (người Việt trả tiền ở nước ngoài). Đã kết nối 6 nước: Thái Lan, Lào, Campuchia, Trung Quốc, Hàn Quốc, Singapore; đang mở rộng sang Nhật Bản, Ấn Độ, Malaysia. Đối tác chính theo từng thị trường: UnionPay, Alipay, GLN, Liquid Group và các ngân hàng quyết toán.
- Trải nghiệm chi tiết theo demo: chị Lan (Lan's House, trà và quà lưu niệm ở Hội An) với kênh offline; Minji (khách Hàn Quốc ở Đà Nẵng) với kênh online.
- Ví dụ theo ngành hàng: ăn uống, thời trang, quà lưu niệm, mỹ phẩm và nhà thuốc, spa, tạp hóa.
- Kiến trúc và điểm tích hợp: kênh offline (Tendoo – Visa Accept – VDF – Visa); kênh online (web app AI – kênh Viettel – Tendoo để merchant xác nhận lượt đặt – VDF xử lý dòng tiền).
- Giá trị cho từng bên: merchant, khách quốc tế, khách Việt dùng thẻ quốc tế, VTT, VDF.
- Bộ KPI đầy đủ, giả định tài chính.
- Nguồn số liệu:
    - Visa, "VDS – Acquiring discussion", 10/2026 (*Visa Confidential*): Visa Accept, hạn mức, phí, lộ trình nâng gói, triển khai tại VPBank, Sacombank, VIB; Visa QR Connector; Visa Acceptance Platform
    - "Nhu cầu giải pháp thanh toán phục vụ khách du lịch quốc tế tại merchant Việt Nam", khảo sát 132 merchant tại Hà Nội và TP.HCM, 7/2026 *(cần ghi rõ đơn vị thực hiện)*. Lưu ý khi trích dẫn:
        - Mẫu nghiêng về merchant phục vụ nhiều khách quốc tế (78% có trên 50% khách quốc tế; bán lẻ 36%, lưu niệm 30%, nhà hàng 23%), không đại diện cho toàn bộ merchant Tendoo.
        - Kịch bản khảo sát là giải pháp NFC Tag với phí 1–2%, không phải Visa Accept. "Sẵn sàng triển khai" mới là ý định, chưa phải hành vi thật.
        - Một số tỉ lệ trong báo cáo dùng mẫu số không thống nhất (127 và 132). Outline dùng tỉ lệ trên 132 merchant.
    - "Nhu cầu thanh toán của khách quốc tế đến Việt Nam", khảo sát 10 khách quốc tế, 16/10/2026 *(cần ghi rõ đơn vị thực hiện)*. Lưu ý khi trích dẫn:
        - Khảo sát thăm dò, cỡ mẫu nhỏ (10 người; Đông Nam Á 4, châu Âu 2, Trung Quốc, Nhật Bản, Bắc Mỹ, châu Đại Dương mỗi nhóm 1). Không suy rộng theo quốc tịch.
        - Kịch bản khảo sát thu phí 5% của khách, khác với Visa Accept.
    - NQ 198/2025/QH15 (bỏ thuế khoán từ 01/01/2026)
    - [Hỗ trợ hộ kinh doanh chuyển đổi số và kê khai thuế – VnEconomy](https://vneconomy.vn/ho-tro-ho-kinh-doanh-chuyen-doi-so-va-ke-khai-thue.htm)
    - [Kết quả triển khai hóa đơn điện tử – Thời báo Tài chính](https://thoibaotaichinhvietnam.vn/infographics-ket-qua-trien-khai-hoa-don-dien-tu-197840-197840.html)
    - [5 triệu hộ kinh doanh – Báo Chính phủ](https://baochinhphu.vn/them-mot-trieu-doanh-nghiep-tiem-nang-lon-tu-5-trieu-ho-kinh-doanh-102250411152125423.htm)
    - [3,24 triệu hộ, cá nhân kinh doanh; 2,03 triệu có địa điểm cố định, Tổng cục Thuế 8/2024 – Thanh Niên](https://thanhnien.vn/ca-nuoc-co-324-trieu-ho-ca-nhan-kinh-doanh-18524100317255683.htm)
    - [737.159 máy POS cuối 2024, NHNN – VietNamNet](https://vietnamnet.vn/phat-trien-nhieu-phuong-thuc-thanh-toan-moi-tao-thuan-tien-cho-nguoi-dung-2482940.html)
    - [Khảo sát 350 doanh nghiệp nhỏ: 42% nhận thẻ – Visa](https://www.visa.com.vn/en_VN/about-visa/newsroom/press-releases/sixtytwo-percent-of-women-led-smbs-surveyed-in-vietnam-experience-increased-revenue-after-accepting-digital-payments.html)
    - [61 địa điểm quy hoạch khu du lịch quốc gia – VietnamPlus](https://www.vietnamplus.vn/61-dia-diem-tiem-nang-duoc-quy-hoach-phat-trien-thanh-khu-du-lich-quoc-gia-post959354.vnp)
    - [153 di tích quốc gia đặc biệt – Cổng Chính phủ](https://xaydungchinhsach.chinhphu.vn/danh-sach-di-tich-quoc-gia-dac-biet-119260211160043009.htm); [hơn 4.000 di tích quốc gia, 41.000 di tích – Wikipedia](https://vi.wikipedia.org/wiki/Di_t%C3%ADch_Vi%E1%BB%87t_Nam)
    - [Hội An: 236 cơ sở trên 2 tuyến phố, bằng 4% toàn thành phố – Tuổi Trẻ](https://tuoitre.vn/saigontimes/pho-co-hoi-an-buon-ban-bay-gio-10630819.htm); [Phường Hoàn Kiếm 4.310 hộ kinh doanh – Nhân Dân](https://nhandan.vn/dong-hanh-cung-doanh-nghiep-nho-ho-kinh-doanh-trong-chuyen-doi-so-post910634.html)
    - [Chi tiêu 1.200–1.400 USD mỗi chuyến – VietnamPlus](https://en.vietnamplus.vn/vietnams-tourism-industry-shifts-focus-from-visitor-numbers-to-spending-post350579.vnp)
    - [21,2 triệu lượt khách quốc tế 2025 – Báo Chính phủ](https://en.baochinhphu.vn/foreign-arrivals-soar-to-record-high-in-2025-111260106100233228.htm)
    - [Khách quốc tế 9 tháng 2026 tăng 14,5% – Báo Văn hóa](https://baovanhoa.vn/du-lich/khach-quoc-te-den-viet-nam-9-thang-2026-tang-145-271196.html)
    - [Nguồn khách 9 tháng 2026 theo thị trường – VietnamPlus](https://www.vietnamplus.vn/du-lich-viet-don-177-trieu-khach-sau-9-thang-thi-truong-nao-dang-tang-toc-post1139852.vnp); [Mekong ASEAN](https://mekongasean.vn/trung-quoc-han-quoc-dan-dau-nguon-khach-quoc-te-den-viet-nam-trong-9-thang-60416.html)
    - [Chi tiêu bình quân và cơ cấu chi tiêu khách quốc tế 2019, Niên giám thống kê 2022 – VietNamNet](https://vietnamnet.vn/di-du-lich-viet-nam-khach-nuoc-nao-chi-tien-manh-tay-nhat-2167403.html); [CafeBiz](https://cafebiz.vn/den-viet-nam-du-khach-nuoc-nao-manh-tay-chi-tien-nhat-chi-tien-nhieu-nhat-vao-khoan-gi-176230718085444009.chn)
    - [Thu 15,22 tỷ USD từ khách quốc tế 2025, khoảng 718 USD mỗi lượt – Dân trí](https://dantri.com.vn/kinh-doanh/chi-tieu-khach-tay-den-viet-nam-va-nguoi-viet-ra-nuoc-ngoai-nghich-ly-can-loi-giai-20260906232044127.htm)
    - [Cơ cấu thanh toán tại điểm bán Hàn Quốc 2024, Worldpay GPR 2025 – Payments CMI](https://paymentscmi.com/insights/south-korea-2025-payments-ecommerce-trends/)
    - [Thẻ chiếm 71% chi tiêu tại cửa hàng ở Mỹ 2025 – Global Payments](https://investors.globalpayments.com/news-events/press-releases/detail/504/gen-z-driving-the-shift-from-cards-to-digital-wallets-new)
    - [Alipay, WeChat Pay chiếm 87% giá trị tại điểm bán ở Trung Quốc, Worldpay GPR 2026 – Rich Turrin](https://richturrin.substack.com/p/what-asia-knew-first-digital-wallets)
    - [Tiền mặt ở Nhật Bản khoảng 38% chi tiêu tại cửa hàng, Worldpay GPR 2026 – Dwayne Gefferie](https://dwaynegefferie.substack.com/p/three-things-the-worldpays-global)
    - [Thẻ ở Úc, Anh khoảng 67–70% – Payments CMI](https://paymentscmi.com/insights/top-global-payment-methods/)
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
    - Biểu phí Tap to Phone/SoftPOS công khai: VPBank (hiệu lực 01/08/2026), Techcombank (khách đăng ký mới từ 01/03/2025) *(cần bổ sung link)*
    - VNPAY hợp tác Mastercard cho du khách liên kết thẻ trong app VNPAY: *cần bổ sung nguồn*
    - [MoMo và Alipay+ cho người Việt đi nước ngoài – MoMo](https://www.momo.vn/tin-tuc/khuyen-mai/vi-vu-quoc-te-cung-momo-alipay-quet-ma-thanh-toan-8778)
    - Slide 6 (kênh online):
        - [56% khách Mỹ dùng AI cho chuyến đi, The AI Surge – Phocuswright 3/2026](https://www.phocuswright.com/Travel-Research/Research-Updates/2026/The-fastest-shift-in-travel-behavior-just-became-the-default); [Travel Weekly](https://travelweekly.com.au/research-show-majority-of-us-travellers-now-use-ai-for-trips/)
        - [Gen Z 69%, Millennials 64% dùng AI tạo sinh lên kế hoạch, Booking.com 2026 – Statista](https://www.statista.com/chart/amp/36471/gen-z-consults-gen-ai-for-travel-advice/)
        - [81% khách Việt dự định dùng AI, Agoda 2026 Travel Outlook – PR Newswire qua Utusan](https://www.utusan.com.my/pr-newswire-en/2026/03/81-of-vietnamese-travelers-want-to-use-ai-to-plan-their-next-trip-agoda-report-finds/); [VNA](https://vietnamnews.vn/life-style/1766348/vietnamese-tourists-keen-on-ai-for-smarter-travel-experiences.html)
        - [99% khách Việt quan tâm AI, 11% hoàn toàn tin – BBW, dẫn Booking.com](https://bbw.vn/99-nguoi-viet-muon-dung-tri-tue-nhan-tao-trong-du-lich-nhung-chi-11-that-su-tin-tuong-53999.html)
        - [Du lịch trực tuyến Việt Nam khoảng 4 tỷ USD 2025, e-Conomy SEA 2025 – VnEconomy](https://vneconomy.vn/google-nen-kinh-te-so-viet-nam-du-kien-dat-39-ty-usd-vao-nam-2025.htm)
        - [OTA 58,85% lượt đặt phòng 2025, hoa hồng 15–25% – Tạp chí Kinh tế – Tài chính 12/5/2026](https://nghiencuu.tapchikinhtetaichinh.vn/chien-luoc-phan-phoi-kenh-dat-phong-cua-cac-chuoi-khach-san-viet-nam-nghien-cuu-truong-hop-muong-thanh-va-vinpearl-155966.html); [hoa hồng Booking.com tối thiểu 15% – Vietnam Booking](https://www.vietnambooking.com/khach-san/tin-tuc-khach-san/cac-trang-web-ban-phong-khach-san.html)
        - [50,2 triệu thẻ quốc tế, Vụ Thanh toán NHNN quý I/2025 – VietnamFinance](https://vietnamfinance.vn/nguoi-viet-thuc-hien-hon-447-ty-giao-dich-online-trong-quy-i-d127299.html)
        - [81 triệu lượt khách nội địa 6 tháng 2026 – Thương hiệu và Công luận](https://thuonghieucongluan.com.vn/du-lich-viet-nam-but-toc-trong-nua-dau-nam-2026-a324972.html)
        - [Booking.com, Expedia ra app trong ChatGPT 10/2025 – Skift](https://skift.com/2025/10/06/expedia-booking-chatgpt-apps-openai/); [PhocusWire](https://www.phocuswire.com/openai-chatgpt-apps-expedia-booking-tripadvisor)
        - [PasGo hơn 3.000 nhà hàng – App Store](https://apps.apple.com/vn/app/pasgo-%C4%91%E1%BA%B7t-b%C3%A0n-nh%C3%A0-h%C3%A0ng-%C6%B0u-%C4%91%C3%A3i/id896053668?l=vi); [phí đặt bàn theo khách 0,5–3 EUR – resOS](https://resos.com/best-restaurant-booking-system-without-commission-fees/)

## Thông tin còn thiếu

*Chỉ theo dõi trong outline, không đưa lên slide.*

| Ưu tiên | Nội dung | Phục vụ slide |
| --- | --- | --- |
| Cao | Số merchant Tendoo chính xác (tổng, active) | 7, 8, 13 |
| Cao | Doanh thu của VDF theo từng kênh: tỉ lệ chia phí giao dịch với VTT (offline); mức affiliate và phần phí booking VDF được hưởng (online). Bổ sung sau | 8, 11, phụ lục |
| Cao | Cơ chế phí Visa Accept: đã có mức IRF (miễn phí dưới 200.000đ, 200đ trên 200.000đ); còn thiếu phí acquirer do bên nào trả, bên nào nhận; VDF nhận được phần nào; mức phí áp dụng trước 01/02/2027 | 8, 9, phụ lục |
| Trung bình | Trả qua link nhận những loại thẻ nào | 9, 10 |
| Trung bình | Tỉ lệ merchant Tendoo đã có thẻ Visa và đang dùng Android | 9, phụ lục (rủi ro) |
| Trung bình | Kết quả triển khai Visa Accept của VPBank, Sacombank, VIB | 5, phụ lục |
| Trung bình | Nguồn xác nhận hợp tác VNPAY – Mastercard cho du khách | 5, phụ lục |
| Trung bình | Link biểu phí Tap to Phone/SoftPOS của VPBank, Techcombank | 5 |
| Trung bình | Đơn vị thực hiện hai khảo sát | 2, 3 |
| Trung bình | Cách khách quốc tế trả tiền **tại Việt Nam** theo quốc tịch (đã có số liệu thói quen ở nước của khách; số đo tại Việt Nam xin Visa, NAPAS) | 3, 4 |
| Trung bình | Kênh Viettel đưa khách đến AI: khả năng gắn link AI vào tin nhắn chào mừng roaming; số khách quốc tế roaming Viettel, số SIM/eSIM du lịch bán ra | 11, 15 |
| Trung bình | Rủi ro và hướng xử lý riêng cho kênh online (khách hủy hoặc không đến, hoàn tiền trả trước, đặt cọc) | Phụ lục |
| Trung bình | Tỉ lệ merchant vừa và nhỏ quanh điểm du lịch có mặt trên Google Maps, Tripadvisor, OTA và có thông tin tiếng nước ngoài (nhờ đội kênh bán VTT kiểm tra 3–5 điểm) | 6 |
| Trung bình | Cách khách quốc tế tìm quán ăn, điểm mua sắm tại Việt Nam và tỉ lệ dùng AI (hỏi bổ sung trong khảo sát khách) | 6 |
| Thấp | Cách trả tiền phổ biến ở Đài Loan; số so với cùng kỳ của Mỹ, Nhật Bản | 3 |
| Thấp | Đối chiếu số liệu Worldpay của Úc, Anh, Nhật Bản với báo cáo gốc | 3 |
| Thấp | Nguồn gốc số OTA 58,85% và hoa hồng 15–25% (đối chiếu báo cáo ngành hoặc hợp đồng thực tế); bản gốc báo cáo Agoda, Booking.com | 6 |
