# Thanh toán cho khách quốc tế tại merchant VTT – Outline trình bày giải pháp

Cập nhật: 2026-10-22 · Huyhn8 · v0.6

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

Trình bày với Tổng giám đốc VDF về giải pháp VDF cung cấp hạ tầng thanh toán cho khách quốc tế tại các merchant của VTT, dựa trên Visa Accept.

- **Hình thức:** slide, họp trực tiếp
- **Thời lượng:** khoảng 27 phút, 20 slide chính và phụ lục
- **Đơn vị:** VDF, phối hợp với VTT (Tendoo, Tammi)
- **Bối cảnh:** VDF đã có dự án cung cấp nền tảng thanh toán cho Tammi, nhưng bài toán merchant chưa từng được trình bày với Tổng giám đốc. Tài liệu đề xuất v0.1 mới lưu hành nội bộ, chưa làm việc chính thức với Tendoo và Tammi. Visa đã trình bày Visa Accept cho Viettel (10/2026).
- **Thông điệp chính:** VDF đưa Visa Accept vào app Tendoo để merchant nhận thẻ của khách quốc tế ngay trên điện thoại: khách chạm thẻ, hoặc trả qua link nếu không chạm được. Gần như không mất phí, tiền về gần như tức thì. Kèm theo là trợ lý AI đa ngôn ngữ giúp khách hỏi được, hiểu được rồi mới mua. VTT phát triển merchant. Sau đó nâng merchant lên gói nhận thẻ đầy đủ và mở rộng sang khách Việt trên Tammi.

| Phần | Slide | Thời gian |
| --- | --- | --- |
| Mở đầu | 1 | 0,5 phút |
| 1. Bối cảnh | 2–7 | 7 phút |
| 2. Vấn đề | 8–10 | 5 phút |
| 3. Cơ hội của VDF | 11 | 1,5 phút |
| 4. Giải pháp | 12–17 | 9 phút |
| 5. Mô hình hợp tác và lộ trình triển khai | 18–20 | 4 phút |

**Mạch lập luận:** khách quốc tế tăng nhanh nhưng cửa hàng nhỏ chưa có cách nhận tiền phù hợp → các giải pháp đang có đều còn hạn chế → khảo sát merchant và khách xác nhận các hạn chế đó; Tendoo, Tammi cũng chưa giải quyết được → VDF có cơ hội lấp khoảng trống → giải pháp → VTT và VDF cùng triển khai.

## Mở đầu

### Slide 1 – Trang bìa

- Tên bài (đề xuất): *Giải pháp thanh toán cho khách quốc tế tại merchant Tendoo – Tammi*. Đơn vị trình bày (VDF), ngày trình bày.

## Phần 1 – Bối cảnh (khoảng 7 phút)

### Slide 2 – Thị trường merchant trong nước

- Khoảng **5 triệu hộ kinh doanh**, đóng góp gần 30% GDP.
- Từ 01/01/2026 hộ kinh doanh bỏ thuế khoán, chuyển sang tự kê khai (NQ 198/2025/QH15). Đến 14/5/2026, hơn 308.000 hộ kinh doanh đã đăng ký hóa đơn điện tử từ máy tính tiền, tăng 35% so với cuối 2025 (Bộ Tài chính). Nhu cầu số hóa bán hàng và thanh toán tăng mạnh.
- Livestream chiếm khoảng 20% doanh thu thương mại điện tử (AccessTrade, đầu 2026).
- AI đã thành tính năng phổ biến: các phần mềm bán hàng đều có AI nhập liệu và chatbot. Lợi thế chuyển sang **trợ lý biết hành động**, gắn với kênh bán và dòng tiền thật.
- Kết luận của slide: merchant cần công cụ mang thêm khách và doanh thu, không chỉ công cụ quản lý.

### Slide 3 – Xu hướng khách quốc tế đến Việt Nam

- 9 tháng 2026: **17,7 triệu lượt khách quốc tế, tăng 14,5%**, đạt gần 71% mục tiêu 25 triệu lượt cả năm. Cùng kỳ, du lịch quốc tế toàn cầu (6 tháng đầu năm) chỉ tăng 0,4%.
- Năm 2025: 21,2 triệu lượt khách quốc tế, tổng thu du lịch khoảng 1 triệu tỷ đồng.
- **Khách quốc tế chi tiêu cao, khoảng một phần ba chi cho ăn uống và mua sắm:**
    - Mỗi lượt khách chi khoảng **700–1.150 USD**.
    - **Ăn uống chiếm 21,9%, mua sắm chiếm 12,4%**, cộng lại khoảng 34% tổng chi (Tổng cục Thống kê). Đây là chi tiêu tại quán ăn, quán cà phê, cửa hàng nhỏ.
    - Ước tính sơ bộ: khoảng **5–8 tỷ USD mỗi năm** khách quốc tế chi cho ăn uống và mua sắm.
- **Phần lớn khách quốc tế quen trả bằng thẻ:** ở Hàn Quốc, Mỹ, Úc, Anh, thẻ chiếm khoảng 2/3 chi tiêu tại cửa hàng. Riêng khách Trung Quốc chủ yếu dùng Alipay, WeChat Pay (Worldpay Global Payments Report 2025, 2026).
- **Vì sao tập trung phân khúc này:**
    - Tệp khách lớn, tăng nhanh, chi tiêu cao, nhưng chưa được phục vụ tốt ở cửa hàng nhỏ.
    - Phục vụ được nhóm khách này là tạo ra doanh thu mới cho cửa hàng (bán được cho khách trước đây bỏ đi), chứ không chỉ chuyển giao dịch từ tiền mặt sang thẻ.
- *Ghi chú cho người trình, không đưa lên slide:*
    - *1.150 USD là điều tra chi tiêu của Tổng cục Thống kê năm 2019 (bản mới nhất có cơ cấu theo khoản). 718 USD là tổng thu từ khách quốc tế 2025 (15,22 tỷ USD) chia cho 21,2 triệu lượt. Hai số khác nhau do khác cách tính.*
    - *Cách tính 5–8 tỷ USD: 21,2 triệu lượt × 718–1.150 USD × 34%.*
    - *Số liệu chi tiết về cách trả tiền tại cửa hàng ở nước của khách: Hàn Quốc (2024) thẻ 68% (tín dụng 54%, ghi nợ 14%), ví 20%, tiền mặt 7%; Mỹ (2025) thẻ 71%; Úc, Anh thẻ khoảng 67–70%; Nhật Bản (2025) tiền mặt còn khoảng 38%; Trung Quốc (2025) Alipay, WeChat Pay chiếm 87%.*
    - *Đây là thói quen ở nước của khách, không phải số đo tại Việt Nam. Chưa có số liệu công khai về cách khách quốc tế trả tiền tại Việt Nam theo quốc tịch; nên xin từ Visa hoặc NAPAS. Số của Úc, Anh, Nhật Bản lấy qua nguồn thứ cấp, cần đối chiếu báo cáo gốc Worldpay.*

### Slide 4 – Khách quốc tế đang trả tiền thế nào tại Việt Nam

- **Ba cách khách đang trả tiền:**
    - **Tiền mặt, đổi ngoại tệ:** bất tiện, rủi ro, khách thường mang ít.
    - **Thẻ quốc tế qua máy POS:** chủ yếu ở khách sạn, trung tâm thương mại, chuỗi lớn. Cửa hàng nhỏ ít có máy và ngại phí.
    - **Quét QR quốc tế** (khách quét mã bằng ví hoặc app ngân hàng nước mình): đang mở rộng nhưng chỉ dùng được với các nước đã kết nối và mới phủ ít điểm.
- **Số liệu chính:**
    - Chỉ khoảng 6% trong hơn 2,5 triệu điểm chấp nhận thanh toán nhận QR quốc tế (NHNN, 25/9/2026).
    - Nhu cầu là có thật: giao dịch VietQR Global của khách Thái Lan, Lào, Campuchia 8 tháng 2026 tăng khoảng 8 lần so với 2025. Giao dịch của khách Trung Quốc tăng khoảng 3 lần (NAPAS).
    - Cửa hàng đặc sản, quán ăn ở địa phương còn vướng rào cản thiết bị và chi phí (VCCI).
- Kết luận của slide: **khách có tiền và muốn trả, nhưng cửa hàng nhỏ chưa có cách nhận phù hợp.** Thị trường đã xuất hiện một số giải pháp mới (slide 5–7).

### Slide 5 – Giải pháp hiện có 1: QR thanh toán quốc tế

- **Cách hoạt động:** khách quét mã QR của cửa hàng bằng ví hoặc app ngân hàng nước mình; cửa hàng nhận tiền VND.
- **Ví dụ:**
    - NAPAS – VietQR Global: đã kết nối 6 nước (Thái Lan, Lào, Campuchia, Trung Quốc, Hàn Quốc, Singapore), đang mở rộng sang Nhật Bản, Ấn Độ, Malaysia.
    - VNPAY-QR: khách quét bằng WeChat Pay, Alipay, UnionPay, Toss Pay…; đã có tại Thế Giới Di Động, Điện Máy Xanh, TopZone (từ 9/2026).
- **Hình minh họa:** hai ảnh đặt cạnh nhau:
    - Khách Hàn Quốc quét VietQR bằng app nước mình, trả thành công.
    - Khách Mỹ hoặc châu Âu đứng trước cùng mã QR nhưng không có app nào quét được, phải chuyển sang tiền mặt.
- **Hạn chế:**
    - Chỉ dùng được với khách từ các nước đã kết nối. Khách châu Âu, Mỹ, Úc, Nhật Bản, Ấn Độ… chưa dùng được.
    - Mới khoảng 6% điểm chấp nhận thanh toán nhận QR quốc tế.
    - VNPAY đi qua chuỗi lớn trước, hộ kinh doanh nhỏ chưa được phủ.

### Slide 6 – Giải pháp hiện có 2: khách tải app Việt Nam, liên kết thẻ

- **Cách hoạt động:** khách quốc tế tải app thanh toán của Việt Nam, đăng ký, liên kết thẻ quốc tế rồi quét QR nội địa của cửa hàng.
- **Ví dụ:** VNPAY hợp tác Mastercard *(cần nguồn xác nhận)*.
- **Hình minh họa:** dãy ảnh chụp màn hình các bước khách phải làm trước lần trả tiền đầu tiên: tải app, đăng ký, xác thực, liên kết thẻ, rồi mới quét QR. Đánh số từng bước để thấy quy trình dài.
- **Hạn chế:**
    - Khách phải tải thêm app, đăng ký và liên kết thẻ chỉ để dùng trong một chuyến đi ngắn.
    - Rào cản lớn nhất nằm ở lần dùng đầu tiên: khách đang đứng ở quầy thường không chịu làm cả quy trình.

### Slide 7 – Giải pháp hiện có 3: Tap to Phone

- **Cách hoạt động:** điện thoại Android của cửa hàng thành máy nhận thẻ; khách chạm thẻ hoặc ví trên điện thoại vào.
- **Ví dụ:**
    - VPBank (TapLink), Sacombank, VIB (BizPay): dùng Visa Accept trong app ngân hàng.
    - VNPAY SoftPOS: app nhận thẻ riêng, đạt chuẩn PCI CPoC.
    - VCB Tap to Phone: tính năng nhận thẻ của Vietcombank.
- **Hình minh họa:** dãy ảnh một lần bán hàng: chủ tiệm mở app ngân hàng, nhập số tiền, khách chạm thẻ, trả thành công. Ảnh cuối: chủ tiệm phải mở sổ hoặc phần mềm bán hàng khác để ghi lại đơn.
- **Hạn chế:**
    - Là app riêng hoặc tính năng trong app ngân hàng, tách khỏi việc bán hàng. Chủ tiệm phải ghi sổ lại bằng tay.
    - Ngân hàng chờ khách hàng tự bật tính năng, không có đội phát triển merchant đến tận cửa hàng.
    - VNPAY SoftPOS, VCB Tap to Phone vẫn thu MDR theo hợp đồng và chưa có cách xử lý khi khách không chạm được.
- **Kết luận chung cho slide 5–7:**
    - **Thị trường không thiếu phương thức thanh toán, mà thiếu một giải pháp đến được hộ kinh doanh nhỏ, gắn với việc bán hàng và chi phí thấp.**
    - Visa Accept đã có ở ba ngân hàng, nên công nghệ không phải là khác biệt. Khác biệt nằm ở tệp merchant, kênh phát triển và việc gắn với bán hàng (slide 16).
- *Lưu ý khi trình bày slide 7: không chê công nghệ chạm thẻ, vì giải pháp của VDF cũng dùng Tap to Phone. Chỉ nói hạn chế về cách đưa đến merchant và việc tách khỏi bán hàng.*

**Ghi chú chung cho slide 5–7:**
- *Hình minh họa nên là ảnh chụp màn hình app thật hoặc ảnh dựng lại theo luồng thật, tập trung vào điểm vướng của khách hoặc chủ tiệm.*
- *Cần nghiên cứu thêm: kết quả triển khai Visa Accept của VPBank, Sacombank, VIB; nguồn xác nhận hợp tác VNPAY – Mastercard.*
- *Bảng đối thủ chi tiết (thêm MoMo, KiotViet, Sapo, MISA) ở phụ lục.*

## Phần 2 – Vấn đề (khoảng 5 phút)

### Slide 8 – Merchant nói gì: khảo sát 132 merchant ở khu du lịch (7/2026)

- **Khách quốc tế là nguồn doanh thu chính:** 78% merchant có trên một nửa khách là khách quốc tế.
- **Insight 1 – Phải chắp vá nhiều cách nhận tiền:** 78% merchant dùng song song tiền mặt, QR và POS; 100% vẫn phải giữ tiền mặt để dự phòng. Có merchant mở cả tài khoản ngân hàng Malaysia để nhận tiền của khách Malaysia. Merchant đã mệt vì phải dùng nhiều công cụ ("nhiều phương tiện quá", "phải thêm hình thức mới").
- **Insight 2 – Phí là rào cản lớn nhất:** 48,5% merchant coi phí POS là rắc rối lớn nhất (3–5% mỗi giao dịch); nhiều nơi phải cộng thêm khoảng 30.000đ mỗi giao dịch vào tiền của khách. 50,8% lo chi phí triển khai giải pháp mới.
- **Insight 3 – Mất doanh thu tại quầy:** 14,4% từng gặp khách không có tiền mặt VND hoặc tiền lẻ; 9,1% không nhận được Apple Pay, Google Pay, ví nước ngoài. Khi không nhận được đúng cách khách muốn trả, giao dịch thường hỏng.
- **Insight 4 – Cần chứng từ, không chỉ nhận được tiền:** 26,5% merchant tự nhắc đến đối soát, hóa đơn hoặc khiếu nại.
- **Merchant sẵn sàng đổi:** 58% chắc chắn hoặc có thể sẽ dùng giải pháp thanh toán mới; chỉ 22% có xu hướng từ chối.
- Kết luận của slide: các hạn chế ở slide 5–7 là có thật. Merchant cần **một giải pháp gộp vào công cụ đang dùng, chi phí thấp, có chứng từ**, không cần thêm một công cụ nữa.

### Slide 9 – Khách quốc tế nói gì: khảo sát khách quốc tế (16/10/2026)

- **Phải mang tiền mặt:** 5/10 khách phải mang tiền mặt cho chi tiêu hằng ngày; 3/10 gặp phụ phí thẻ hoặc yêu cầu chi tối thiểu; 2/10 gặp cửa hàng chỉ nhận QR ngân hàng hoặc ví Việt Nam.
- **Không trả được thì phải xoay xở, có khi bỏ đi:** 8/10 khách từng phải xử lý khi không trả được bằng cách mình muốn: nhờ người khác trả hộ (3/10), đi rút hoặc đổi tiền (2/10), **sang cửa hàng khác (2/10)**.
- **Cần ở đâu nhất:** quán ăn, quán cà phê và điểm tham quan (cùng 7/10).
- **Sẵn sàng dùng:** 7/10 khách chấm khả năng sử dụng giải pháp mới ở mức 4–5/5.
- Kết luận của slide: **merchant mất khách khi không nhận được cách khách muốn trả.** Đây cũng chính là doanh thu mà giải pháp mang lại cho merchant.
- *Ghi chú trên slide: khảo sát thăm dò, cỡ mẫu 10 khách. Dùng làm tín hiệu bổ sung cho khảo sát merchant, chưa đại diện cho toàn bộ khách quốc tế.*
- *Lưu ý cho người trình: kịch bản khảo sát khách là thu phí 5% của khách (6/10 sẵn sàng trả), khác với Visa Accept (gần như không thu phí). Không đưa con số phí 5% lên slide để tránh nhầm lẫn.*

### Slide 10 – Vấn đề nội tại của Tendoo và Tammi

- **Tendoo: có công cụ, chưa có khách**
    - Hơn 200.000 lượt hộ kinh doanh được hỗ trợ chuyển đổi thuế, nhưng phần lớn merchant không hoạt động. Công cụ quản lý chưa tạo thêm khách và thêm doanh thu, nên người bán chưa có lý do gắn bó.
    - **AI của Tendoo đang hướng vào trong:** trợ lý thuế, tạo hàng từ ảnh, lên đơn bằng giọng nói giúp chủ tiệm nhập liệu, chưa giúp bán cho khách. KiotViet, Sapo, MISA cũng có các tính năng này, nên không tạo khác biệt.
    - **Dữ liệu hàng hóa, giá, tồn kho nằm yên trong Tendoo:** chưa đến được khách, chưa có bằng ngôn ngữ của khách, chưa lên kênh bán nào. Khách quốc tế vào cửa hàng không hỏi được, không hiểu được sản phẩm.
    - Merchant không nhận được thẻ quốc tế. Thanh toán đi qua QR ngân hàng, chưa gắn với đơn và sổ sách trên Tendoo.
    - Khi bán online, merchant phụ thuộc nền tảng ngoài (phí cao, thuật toán khó đoán), quá tải khi livestream và thiếu người trực tin nhắn ban đêm.
- **Tammi: có người dùng, chưa có thương mại**
    - Hơn 5 triệu người dùng đã xác thực, chat hằng ngày, nhưng chưa có cửa hàng, livestream hay công cụ cho người bán.
    - AI hiện có (gợi ý dịch vụ, chatbot Tammi AI) chỉ phục vụ dịch vụ Viettel, chưa nối tới cửa hàng nào.
- **Hệ quả của việc hai bên tách rời:** người bán và người mua gặp nhau qua nền tảng ngoài với phí cao, dữ liệu và dòng tiền nằm ngoài hệ sinh thái. Minh họa: sơ đồ "Trước" trong tài liệu đề xuất (mục 2).
- *Ghi chú cho người trình: hai khảo sát chỉ hỏi về thanh toán, chưa có số liệu về rào cản ngôn ngữ tại cửa hàng. Trình bày ý này như một giả thuyết, sẽ kiểm chứng trong pilot bằng lượt quét QR và tỉ lệ đặt hàng sau khi quét (slide 20). Nếu kịp, hỏi bổ sung 1–2 câu về giao tiếp cho merchant và khách quốc tế.*
- *Cần bổ sung: số merchant Tendoo chính xác (tổng, active); MAU Tammi; số đơn và GMV hiện tại trên Tendoo.*
- *Lưu ý: số công bố công khai của Tammi là 5 triệu+ (8/2026); số nội bộ khoảng 10 triệu, nếu dùng thì ghi rõ nguồn và thời điểm. "200.000" là số lượt hộ kinh doanh được hỗ trợ chuyển đổi thuế (Đại biểu Nhân dân, 12/01/2026), không phải số merchant đang dùng Tendoo.*

## Phần 3 – Cơ hội của VDF (khoảng 1,5 phút)

### Slide 11 – Cơ hội của VDF

**1. Thanh toán: merchant muốn nhận, ai có phí thấp sẽ thắng**
- 58% merchant sẵn sàng dùng giải pháp mới; 7/10 khách quốc tế sẵn sàng dùng.
- Kỳ vọng phí 1–2% thì 81,5% merchant sẵn sàng dùng. Visa Accept gần như không thu phí, thấp hơn cả mức này.

**2. AI: trợ lý tư vấn và chốt đơn là xu hướng, nhưng chưa ai gắn với kho, sổ sách và thanh toán**
- **Xu hướng:** AI đang chuyển từ trả lời câu hỏi sang trợ lý biết hành động: tư vấn, chốt đơn, gửi yêu cầu thanh toán. Livestream chiếm khoảng 20% doanh thu thương mại điện tử; người bán quá tải khi live và thiếu người trực tin nhắn ban đêm.
- **Khoảng trống:** AI của các phần mềm bán hàng, kể cả Tendoo, đang hướng vào trong (nhập liệu, thuế). Chatbot bán hàng không có kho và sổ sách. Chưa ai phục vụ khách quốc tế tại quầy.
- **Lợi thế của VDF:** dữ liệu hàng hóa có sẵn trên Tendoo giúp trợ lý tạo được trong vài phút. Trợ lý là cửa vào của giao dịch: mỗi cuộc trò chuyện, dù trên livestream, trong tin nhắn hay tại quầy, đều kết thúc bằng một lần trả tiền qua VDF.

**3. Dài hạn: có sẵn kênh đến merchant và người mua**
- Tệp hộ kinh doanh Tendoo và đội kênh bán thực địa của VTT, không phải chờ merchant tự tìm đến.
- Mở rộng sang khách Việt trên Tammi (hơn 5 triệu người dùng, chưa có thương mại).

- *Ghi chú cho người trình, không đưa lên slide:*
    - *Trong nhóm "chưa chắc chắn", 42,5% chuyển sang sẵn sàng khi được báo một mức phí cụ thể và thấp. Kỳ vọng phí trên 3% thì chỉ 24,3% sẵn sàng.*
    - *Việc khách quốc tế bỏ đi vì không hỏi được nhân viên là giả thuyết, chưa có số liệu khảo sát; pilot đo bằng lượt quét QR và tỉ lệ đặt hàng sau khi quét.*
    - *Tệp hộ kinh doanh Tendoo: hơn 200.000 lượt được hỗ trợ chuyển đổi thuế, không phải số merchant đang dùng.*
    - *Với VTT, quan hệ nâng từ "cung cấp thanh toán cho Tammi" lên "đồng kiến tạo lớp thương mại".*

## Phần 4 – Giải pháp (khoảng 9 phút)

### Slide 12 – Giải pháp tổng thể

- Định nghĩa trong một câu: *VDF đưa Visa Accept vào app Tendoo để merchant nhận thẻ của khách quốc tế ngay trên điện thoại, kèm trợ lý AI tư vấn và chốt đơn: tại cửa hàng bằng ngôn ngữ của khách, online trên livestream và tin nhắn.*
- Minh họa: sơ đồ "Sau" vẽ lại với **thanh toán của VDF ở trung tâm**. Ba lớp:
    1. **Thanh toán VDF:** Visa Accept trong Tendoo, sau đó là gói nhận thẻ đầy đủ và thanh toán nội địa đa nguồn tiền.
    2. **Merchant AI Studio:** trợ lý AI tư vấn và bán hàng, tạo từ dữ liệu cửa hàng có sẵn trên Tendoo.
    3. **Kênh khách hàng:** du khách quốc tế tại cửa hàng (làm ngay); khách online qua website bán hàng và mạng xã hội Tendoo đang kết nối; người dùng Tammi khi Tammi có Shop và Live.
- **Vì sao cần cả thanh toán lẫn AI:** hành trình mua tại quầy gồm *khách vào → hỏi → hiểu → quyết định mua → trả tiền → ghi sổ*.
    - Trợ lý AI giải bước hỏi, hiểu, quyết định. Khách bỏ đi trước khi đến quầy thì nhận được thẻ cũng không có giao dịch.
    - Visa Accept giải bước trả tiền.
    - Tendoo giải bước ghi sổ.
    - Minh họa: một dải hành trình 6 bước, tô màu bước do từng lớp giải quyết.
- Mục tiêu cốt lõi: **tăng dòng tiền cho merchant Tendoo**. Mỗi lớp đóng góp một phần:
    - Thanh toán giúp **nhận được tiền**.
    - Trợ lý AI giúp **bán được hàng**: tăng tỉ lệ khách mua và giá trị đơn.
    - Kênh khách hàng giúp **có thêm khách**.
- Mọi giao dịch đi qua thanh toán VDF và tự ghi sổ trên Tendoo.

### Slide 13 – Giải pháp chi tiết 1: nhận thẻ của khách quốc tế ngay trên điện thoại

- **Visa Accept, tích hợp sẵn trong app Tendoo:** merchant dùng thẻ Visa đang có để nhận tiền, không cần mở tài khoản doanh nghiệp, không cần máy POS.
- **Hai cách nhận tiền:**
    - **Chạm thẻ (Tap to Phone):** khách chạm thẻ Visa, Mastercard hoặc điện thoại có ví vào điện thoại Android của cửa hàng.
    - **Trả qua link:** khi khách không chạm được hoặc cửa hàng không dùng Android, merchant gửi link thanh toán cho khách (tin nhắn, email) để khách trả bằng thẻ. Tại quầy không đặt sẵn mã trả qua link.
- **Bốn lợi ích cho merchant**, trả lời đúng các insight ở slide 8:
    - **Không cần thiết bị, chỉ cần điện thoại** (insight 1, 2).
    - **Gần như không mất phí** (insight 2). Thấp hơn cả mức 1–2% mà 81,5% merchant sẵn sàng chấp nhận (slide 11), nên dễ thuyết phục hộ kinh doanh bắt đầu nhận thẻ qua VDF.
    - **Tiền về gần như tức thì.**
    - **Giao dịch tự ghi sổ trên Tendoo, có chứng từ để đối soát và xử lý khiếu nại** (insight 4).
- **Lộ trình lớn lên:** khi doanh số vượt hạn mức, merchant được nâng lên gói nhận thẻ đầy đủ.
- Minh họa: 2–3 màn hình mẫu (chạm thẻ, trả qua link) đặt trong giao diện Tendoo.

### Slide 14 – Giải pháp chi tiết 2: trợ lý AI tư vấn khách quốc tế tại cửa hàng

- **Merchant AI Studio trong app Tendoo:** chủ tiệm chọn mẫu trợ lý, AI tự đọc hàng hóa, giá, tồn kho, chính sách cửa hàng từ Tendoo, chủ tiệm duyệt rồi bật.
- **Luồng tại cửa hàng:**
    - Khách quét QR đặt ở bàn, kệ, quầy để mở trang web của trợ lý. Không cần cài app, không cần đăng ký.
    - Khách hỏi bằng tiếng của mình (Trung, Hàn, Anh…). Trợ lý trả lời về sản phẩm, giá, cách dùng theo dữ liệu cửa hàng; giá có quy đổi sang tiền nước khách.
    - Khách đặt hàng trên web. Đơn hiện bằng tiếng Việt trên Tendoo, kèm ghi chú đã dịch (dị ứng, size, gói quà).
    - Khách trả tiền tại quầy bằng cách chạm thẻ (slide 13). Khi khách không chạm được, merchant gửi link thanh toán cho khách. Mã QR tại cửa hàng chỉ để mở trợ lý, không dùng để trả tiền.
- **Bốn lợi ích cho merchant**, trả lời đúng các vấn đề ở slide 10:
    - **Bán được cho khách không nói cùng ngôn ngữ**, nhân viên không cần biết ngoại ngữ.
    - **Dữ liệu sẵn có trên Tendoo thành người tư vấn bán hàng**, không phải nhập lại.
    - **Thiết lập khoảng 10 phút, làm một lần, 4 bước.** Trả lời nỗi lo "chủ quán ko rành công nghệ" mà merchant tự nêu trong khảo sát (câu trả lời tự do).
    - **Đơn và tiền tự vào sổ Tendoo**, có hóa đơn song ngữ cho khách.
- **Chốt an toàn:** chỉ trả lời theo dữ liệu cửa hàng, không biết thì nói không biết; luôn có nhãn "Trợ lý AI" và nút "Gặp người thật"; trợ lý không tự trừ tiền.
- Áp dụng cho mọi ngành hàng: ăn uống, thời trang, quà lưu niệm, mỹ phẩm và nhà thuốc, spa, tạp hóa (ví dụ chi tiết ở phụ lục).
- Minh họa: 3–4 màn hình theo luồng anh Kim Min-jun (đề xuất, mục 6.3): web tiếng Hàn, hỏi đáp, đơn tiếng Việt trên Tendoo, chạm thẻ.

### Slide 15 – Giải pháp chi tiết 3: trợ lý bán hàng online, tư vấn và chốt đơn

- **Bài toán:** khi bán online, merchant quá tải khi livestream, thiếu người trực tin nhắn ban đêm, phụ thuộc nền tảng ngoài (slide 10).
- **Hai trợ lý, cùng một Merchant AI Studio với trợ lý tại cửa hàng:**

| Trợ lý | Bài toán | Trợ lý làm gì | Kết quả cho merchant |
| --- | --- | --- | --- |
| **Livestream** | Vừa giới thiệu, vừa trả lời hàng trăm câu hỏi, vừa ghi đơn: sót đơn, khách bỏ đi | Trả lời comment theo dữ liệu cửa hàng; nhận ra comment muốn mua để tạo đơn nháp; khách chốt là đơn lên tự động | Không sót đơn khi live; báo cáo phiên live, nhắc khách chưa trả |
| **Bán hàng qua tin nhắn** | Không đủ người trực, nhất là buổi tối và ban đêm | Tư vấn theo tồn kho thật, chốt đơn, gửi yêu cầu thanh toán; nhân viên vào ca thì trợ lý lùi lại | Không mất khách ngoài giờ; bản tin buổi sáng, chỉ xử lý các hội thoại được gắn cờ |

- **Kênh triển khai theo hai bước:**
    - **Trước:** các kênh Tendoo đang kết nối (website bán hàng, mạng xã hội). Không phải chờ Tammi.
    - **Sau:** Tammi Shop, Tammi Live và OA cửa hàng, khi Tammi sẵn sàng. Đây là kênh người mua riêng của hệ sinh thái, không mất phí cho nền tảng ngoài.
- Thanh toán đa nguồn tiền của VDF ngay trong cuộc trò chuyện: Viettel Money, tài khoản ngân hàng, thẻ nội địa và quốc tế.
- Đơn, kho, sổ sách tự đồng bộ về Tendoo.
- Minh họa: 2 màn hình theo đề xuất (mục 6.1 và 6.2): comment livestream có trợ lý trả lời và tạo đơn nháp; tin nhắn lúc 23 giờ được chốt đơn.
- *Ghi chú cho người trình: cần kiểm tra với Tendoo khả năng của từng kênh đang kết nối (đọc comment livestream, trả lời tin nhắn tự động, gửi link thanh toán), vì mỗi mạng xã hội có giới hạn API riêng. Trợ lý Tammi OA (đặt món nhóm, tìm hàng nhiều shop) là tính năng cho người dùng Tammi, để ở phụ lục.*

### Slide 16 – Vì sao chọn giải pháp này

- **So sánh nhanh với 3 nhóm giải pháp ở slide 5–7:**

| Tiêu chí | QR quốc tế | App Việt Nam + liên kết thẻ | Tap to Phone của ngân hàng | **VDF trong Tendoo** |
| --- | --- | --- | --- | --- |
| Khách nước nào cũng trả được | Không (6 nước) | Có | Có | **Có** |
| Khách không phải cài thêm app | Có | Không | Có | **Có** |
| Phí với merchant gần như bằng 0 | Tùy đơn vị cung cấp | Tùy đơn vị cung cấp | Chỉ Visa Accept | **Có** |
| Gắn với bán hàng, tự ghi sổ | Không | Không | Không | **Có** |
| Tư vấn khách bằng tiếng nước họ | Không | Không | Không | **Có** |

- Thông điệp: *ngân hàng đã có Visa Accept, nhưng chỉ là nút nhận tiền trong app ngân hàng; phần mềm bán hàng và chatbot đã có AI, nhưng chưa ai gắn trợ lý với kho, sổ sách và thanh toán. VDF đưa cả hai vào phần mềm bán hàng của hộ kinh doanh, đến tận cửa hàng qua đội kênh bán.*
- *Ghi chú cho người trình, không đưa lên slide:*
    - *Điểm yếu cần nói thật nếu được hỏi:*
        - *Thanh toán: chưa phục vụ khách chỉ dùng ví nước mình như Alipay, WeChat Pay (phần lớn khách Trung Quốc); chạm thẻ chỉ chạy trên Android; cửa hàng lớn cần lên gói nhận thẻ đầy đủ.*
        - *AI: chưa có số liệu về rào cản ngôn ngữ, pilot sẽ đo; AI có thể trả lời sai, đã có chốt an toàn (chỉ trả lời theo dữ liệu cửa hàng, gặp người thật); kênh Tammi phụ thuộc lộ trình của Tammi, trong lúc chờ thì chạy trên kênh Tendoo đang kết nối.*
    - *Bảng so sánh đầy đủ 11 tiêu chí ở phụ lục. Đánh giá sơ bộ theo thông tin đến 10/2026, cần kiểm tra lại trước khi trình bày.*
    - *Nếu được hỏi về vế "phần mềm bán hàng và chatbot đã có AI" trong thông điệp: mở bảng "So sánh với phần mềm bán hàng và nền tảng thương mại" ở phụ lục. Bảng này cho thấy chỉ Merchant AI Studio có đủ trợ lý tạo đơn, kho và sổ sách, thanh toán trong cùng hệ sinh thái, và phục vụ khách quốc tế tại cửa hàng.*

### Slide 17 – Demo

- Khoảng 2,5–3 phút, hai cảnh:
    - **Tại cửa hàng (khoảng 2 phút):** khách Hàn Quốc vào cửa hàng ở Hội An, quét QR hỏi trợ lý bằng tiếng Hàn, đặt hàng, chạm thẻ vào điện thoại của chủ tiệm, đơn tự ghi sổ trên Tendoo. Thêm tình huống khách không chạm được: chủ tiệm gửi link, khách trả bằng thẻ.
    - **Online (khoảng 30 giây):** 23 giờ, khách nhắn tin cho cửa hàng, trợ lý tư vấn và chốt đơn; hoặc trợ lý trả lời comment và tạo đơn nháp khi livestream. Dùng lại demo có sẵn của tài liệu đề xuất.
- *Kịch bản chi tiết bổ sung sau.*

## Phần 5 – Mô hình hợp tác và lộ trình triển khai (khoảng 4 phút)

### Slide 18 – Phân vai VTT và VDF

| Bên | Vai trò |
| --- | --- |
| **VDF** | Cung cấp **giải pháp và hạ tầng thanh toán merchant quốc tế**: triển khai Visa Accept trong Tendoo, vận hành, đối soát, kiểm soát rủi ro; nâng merchant lên gói nhận thẻ đầy đủ; Merchant AI Studio và các mẫu trợ lý; làm việc với Visa |
| **VTT** (Tendoo, Tammi) | **Phát triển merchant**: tích hợp giải pháp vào app Tendoo, cung cấp dữ liệu hàng hóa và đơn, tuyển và hỗ trợ cửa hàng qua đội kênh bán; Tammi xây lớp thương mại cho người dùng Việt ở các phase sau |

- **Đối tác bên ngoài:** Visa (sản phẩm Visa Accept, mạng lưới thẻ, công cụ chống gian lận).

### Slide 19 – Nguyên tắc hợp tác kinh doanh VTT – VDF

- **Mỗi bên hưởng phần doanh thu tương ứng với phần việc và rủi ro của mình:** VDF gắn với thanh toán và đối soát; VTT gắn với merchant, kênh bán và dữ liệu Tendoo.
- **Tiền của merchant đi qua thanh toán VDF:** VDF là bên quyết toán và đối soát; VTT không giữ tiền của merchant.
- **Chi phí theo phần việc:** mỗi bên chịu chi phí phần mình làm; chi phí phát triển merchant và đội kênh bán được thống nhất khi chốt hợp tác.
- **Cùng có lợi khi merchant lớn lên:** giao dịch qua VDF tự ghi sổ trên Tendoo; merchant nâng gói thì cả hai cùng hưởng.
- *Ghi chú cho người trình, không đưa lên slide:*
    - *Không nêu tỉ lệ chia và số tiền cụ thể khi chưa thống nhất với VTT. Cơ chế phí Visa Accept (IRF, phí acquirer) cần xác nhận với Visa trước khi nêu.*
    - *Mô hình doanh thu chi tiết ở phụ lục, dùng khi được hỏi.*

### Slide 20 – Lộ trình triển khai

- Vẽ thành bảng timeline: hàng là các mảng việc, cột là các phase theo thời gian.

| Mảng việc | Phase 0 – Chuẩn bị<br>*(Q4/2026)* | Phase 1 – Pilot khách quốc tế<br>*(Q1/2027)* | Phase 2 – Mở rộng<br>*(Q3/2027)* | Phase 3 – Hệ sinh thái<br>*(Q4/2027)* |
| --- | --- | --- | --- | --- |
| **Thanh toán** | Chốt hợp tác Visa Accept với Visa; thiết kế tích hợp vào Tendoo | **1a:** mở Visa Accept trong Tendoo (chạm thẻ, trả qua link) | Nâng merchant vượt hạn mức lên gói nhận thẻ đầy đủ; thanh toán đa nguồn tiền trong chat | QR cho khách dùng ví nước mình (Visa QR Connector hoặc VietQR Global); thanh toán cho người Việt ra nước ngoài |
| **Trợ lý AI** | Chốt phạm vi Merchant AI Studio | **1b:** bật trợ lý tư vấn đa ngôn ngữ tại cửa hàng | Trợ lý livestream và tin nhắn trên kênh Tendoo đang kết nối (website, mạng xã hội); lên Tammi Shop, Live, OA cửa hàng khi Tammi sẵn sàng | Tammi OA đầy đủ |
| **Merchant và kênh bán** | Làm việc với VTT, chốt phạm vi và đầu mối | Pilot tại một nhóm cửa hàng đông khách quốc tế (Hội An, Đà Nẵng, Phú Quốc) | Nhân rộng ra các điểm du lịch qua đội kênh bán VTT | Phủ toàn bộ tệp merchant Tendoo |
| **Tammi** | Thống nhất với Tammi về miniapp pilot | **1c:** pilot trợ lý trên miniapp của Tammi cho một nhóm cửa hàng pilot (không cần Tammi Shop, Live) | Tích hợp AI vào OA, xây Shop và Live | Lớp thương mại đầy đủ cho người dùng Việt |
| **Phụ thuộc** | Đồng thuận của VTT; Visa; Tammi (miniapp) | VDF, Visa, Tendoo; Tammi cho miniapp pilot (không cần Shop, Live) | Visa; lộ trình Tammi | Visa, NAPAS, giấy phép |

- **Pilot:** hộ kinh doanh vừa và nhỏ, mọi ngành hàng, ưu tiên quán ăn, quán cà phê và cửa hàng gần điểm tham quan (bối cảnh được 7/10 khách quốc tế chọn). Ưu tiên điểm có nhiều khách dùng thẻ (Hàn Quốc, châu Âu, Mỹ, Úc). Chỉ tiêu kênh bán theo **cửa hàng phát sinh giao dịch**, không theo số tài khoản mở.
- **Pilot miniapp Tammi (bước 1c):** cùng nhóm cửa hàng pilot, trợ lý tư vấn và chốt đơn chạy trong miniapp của Tammi, không cần Tammi Shop hay Live. Mục đích là kiểm chứng người dùng Tammi có hỏi và mua qua trợ lý hay không, trước khi Tammi đầu tư vào Shop và Live.
    - *Ghi chú cho người trình: phạm vi và điều kiện triển khai miniapp phải thống nhất với Tammi trước khi nêu thời điểm. Không nêu cam kết của Tammi trên slide khi chưa có văn bản.*
- **KPI chính: GMV của cửa hàng qua Visa Accept.** GMV ở bước 1a là mốc nền, bước 1b đo phần tăng thêm từ các đơn có tương tác với trợ lý.
- **Chỉ số sớm của trợ lý (bước 1b):** lượt quét QR; tỉ lệ đặt hàng sau khi quét; tỉ lệ câu hỏi trợ lý tự xử lý. Đây cũng là cách kiểm chứng giả thuyết khách quốc tế bỏ đi vì không hỏi được (slide 10).
- **Chỉ số theo dõi:** tỉ lệ cửa hàng còn giao dịch sau 30 ngày; số merchant chạm hạn mức và nâng gói.

## Phụ lục

- **Rủi ro chi tiết và hướng xử lý:**

| Rủi ro | Hướng xử lý |
| --- | --- |
| Merchant vẫn không dùng thật | Chỉ tiêu kênh bán theo cửa hàng có giao dịch; pilot đo GMV và tỉ lệ còn giao dịch sau 30 ngày |
| VPBank, Sacombank, VIB đã có Visa Accept | Tập trung hộ kinh doanh của Tendoo; khác biệt bằng kênh bán thực địa, thanh toán nằm trong Tendoo, trợ lý đa ngôn ngữ |
| Merchant chưa có thẻ Visa để nhận tiền | Đội kênh bán hướng dẫn mở thẻ tại ngân hàng; xem xét hợp tác ngân hàng phát hành để mở thẻ nhanh |
| Chạm thẻ chỉ chạy trên Android | Cửa hàng dùng iPhone nhận tiền qua link |
| Chưa nhận ví nước ngoài (Alipay, WeChat Pay) | Pilot ưu tiên điểm nhiều khách dùng thẻ; QR cho ví nước ngoài ở Phase 3 |
| Hạn mức Visa Accept thấp với cửa hàng lớn | Nâng lên gói nhận thẻ đầy đủ khi chạm hạn mức |
| Doanh thu giai đoạn đầu thấp vì phí gần như bằng 0 | Đặt mục tiêu Phase 1 là có merchant hoạt động; theo dõi tỉ lệ nâng gói |
| Gian lận thẻ | Kiểm soát tần suất và hạn mức của Visa Accept; xác thực 3-D Secure cho giao dịch qua link; cân nhắc công cụ chống gian lận của Visa khi lên gói đầy đủ |
| Phụ thuộc lộ trình Tammi (tích hợp AI vào OA, Shop, Live) | Phase 1 chỉ cần miniapp pilot của Tammi, không cần Shop và Live; trợ lý online chạy trước trên kênh Tendoo đang kết nối; Tammi có thể chậm hoặc từ chối miniapp, khi đó pilot vẫn chạy trên kênh Tendoo |
| Tammi chưa hình thành thói quen mua sắm | Kiểm chứng ở Phase 2 trước khi đầu tư lớn |
| Phối hợp nhiều đơn vị | VDF làm đầu mối làm việc với VTT và Visa |
| Pháp lý AI: Luật Trí tuệ nhân tạo 134/2025 | Luôn gắn nhãn "Trợ lý AI" và nút "Gặp người thật" |
| Dữ liệu cá nhân: Nghị định 13/2023 | Chỉ dùng dữ liệu khi người dùng đồng ý; khách quốc tế dùng web không cần đăng ký; dữ liệu lưu tại Việt Nam |
| AI tư vấn sai, giao dịch sai | Chỉ trả lời theo dữ liệu cửa hàng; trợ lý không tự trừ tiền; khiếu nại, hoàn tiền luôn chuyển người thật |

- **Mô hình doanh thu (dùng khi được hỏi, không đưa vào phần chính):** ở giai đoạn Visa Accept, phí gần như bằng 0. Mục tiêu giai đoạn này là có merchant hoạt động thật. Doanh thu đến khi merchant lớn lên và khi mở rộng dịch vụ.

| Dòng thu | Phase |
| --- | --- |
| Phần phí VDF được nhận từ giao dịch Visa Accept *(cần xác nhận với Visa)* | 1 |
| MDR khi merchant nâng lên gói SMB (dưới 1%) và gói nhận thẻ đầy đủ | 2 |
| MDR thanh toán trong chat: Viettel Money, tài khoản ngân hàng, thẻ nội địa | 2 |
| Thanh toán trên Tammi Shop và livestream | 2 |
| Gói dịch vụ AI cho người bán *(cần thống nhất bên nào thu)* | 2 |
| QR cho khách dùng ví nước mình (Visa QR Connector hoặc VietQR Global) | 3 |
| Thanh toán xuyên biên giới cho người Việt ra nước ngoài | 3 |

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

| Tiêu chí | Máy POS ngân hàng | SoftPOS của ngân hàng, VNPAY | Visa Accept trong app ngân hàng (VPBank, Sacombank, VIB) | QR xuyên biên giới (VietQR Global, VNPAY-QR) | **VDF: Visa Accept trong Tendoo + trợ lý AI** |
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
| Tư vấn khách bằng tiếng nước họ | Không | Không | Không | Không | **Có (trợ lý AI)** |
| Kênh đưa giải pháp đến hộ kinh doanh | Nhân viên ngân hàng | Nhân viên ngân hàng, đại lý | Khách hàng tự bật trong app | Ngân hàng, trung gian | **Tệp hộ kinh doanh Tendoo, đội kênh bán VTT** |

- **NAPAS – VietQR Global:** ví hoặc app ngân hàng nước ngoài kết nối với NAPAS, merchant nhận tiền VND qua mã VietQR. Có hai chiều: chiều vào (du khách trả tiền tại VN) và chiều ra (người Việt trả tiền ở nước ngoài). Đã kết nối 6 nước: Thái Lan, Lào, Campuchia, Trung Quốc, Hàn Quốc, Singapore; đang mở rộng sang Nhật Bản, Ấn Độ, Malaysia. Đối tác chính theo từng thị trường: UnionPay, Alipay, GLN, Liquid Group và các ngân hàng quyết toán.
- **Bài học từ thế giới: app chat và thanh toán** *(lưu ý: số liệu chủ yếu do doanh nghiệp công bố, cần kiểm tra lại)*:
    - **WeChat Pay (Trung Quốc):** đưa thanh toán vào app chat (2013), bùng nổ nhờ lì xì điện tử dịp Tết 2014. Người nhận phải liên kết tài khoản để rút tiền, biến thói quen chat thành thói quen thanh toán. Thị phần WeChat Pay tăng gấp đôi sau chiến dịch. Đến 2018, Alipay và WeChat Pay chiếm khoảng 92,7% thanh toán bên thứ ba.
    - **KakaoPay (Hàn Quốc):** thanh toán gắn với KakaoTalk, đạt 5 triệu người dùng trong năm đầu, khoảng 24 triệu MAU cuối 2024, khoảng 650.000 merchant offline. Người dùng cả KakaoTalk Pay và app KakaoPay tạo doanh thu gấp 2,4 lần.
    - **Alipay, WeChat Pay mở cho du khách (Trung Quốc 2023–2025):** cho liên kết thẻ quốc tế, miễn phí giao dịch dưới 200 tệ. Năm 2024, giao dịch của du khách trên Alipay tăng khoảng 10 lần, người dùng hoạt động tăng khoảng 6 lần. Dịp Quốc khánh 2025, chi tiêu của khách quốc tế qua Alipay tăng gần 40%, thanh toán chạm tăng 500%.
    - **Bài học cho Viettel:** thanh toán gắn vào app dùng hằng ngày là con đường nhanh nhất để có người dùng (hướng cho Tammi với người dùng Việt). Khi trả tiền dễ hơn, du khách chi tiêu nhiều hơn ngay. Ở Việt Nam, cái thiếu là phía cửa hàng nhận tiền, và VDF lấp đúng chỗ này.
- **So sánh với phần mềm bán hàng và nền tảng thương mại** (theo tài liệu đề xuất, mục 7):

| Tiêu chí | **Merchant AI Studio** | Phần mềm bán hàng có AI (KiotViet, Sapo, MISA) | Chatbot bán hàng (Pancake/Botcake) | OA + mini app (Zalo) | Sàn, live (TikTok Shop, Shopee) |
| --- | --- | --- | --- | --- | --- |
| Kênh người mua của riêng hệ sinh thái | **Có** | Chưa thấy | Chưa thấy | Có | Có |
| Quản lý kho, đơn, sổ sách, thuế | **Có** | Có | Một phần | Chưa thấy | Một phần |
| Trợ lý tạo đơn trong chat, livestream | **Có** | Một phần | Có | Một phần | Một phần |
| Thanh toán của chính hệ sinh thái | **Có** | Một phần | Chưa thấy | Có | Có |
| Phục vụ khách quốc tế tại cửa hàng | **Có** | Một phần | Chưa thấy | Chưa thấy | Chưa thấy |

    - *Đánh giá sơ bộ dựa trên thông tin công khai đến 10/2026, cần cập nhật trước khi trình bày.*
- Trải nghiệm chi tiết theo persona: chị Lan (cửa hàng trà ở Hội An), Minh (người dùng Tammi), anh Kim Min-jun và chị Camille Laurent (du khách).
- Ví dụ theo ngành hàng: ăn uống, thời trang, quà lưu niệm, mỹ phẩm và nhà thuốc, spa, tạp hóa.
- Kiến trúc và điểm tích hợp Tendoo – Studio – Tammi – thanh toán VDF – Visa.
- Giá trị cho từng bên: người bán, khách quốc tế, người dùng Tammi, Tendoo, Tammi, VDF.
- Bộ KPI đầy đủ, giả định tài chính.
- Nguồn số liệu:
    - Visa, "VDS – Acquiring discussion", 10/2026 (*Visa Confidential*): Visa Accept, hạn mức, phí, lộ trình nâng gói, triển khai tại VPBank, Sacombank, VIB; Visa QR Connector; Visa Acceptance Platform
    - "Nhu cầu giải pháp thanh toán phục vụ khách du lịch quốc tế tại merchant Việt Nam", khảo sát 132 merchant tại Hà Nội và TP.HCM, 7/2026 *(cần ghi rõ đơn vị thực hiện)*. Lưu ý khi trích dẫn:
        - Mẫu nghiêng về merchant ở khu du lịch (78% có trên 50% khách quốc tế), không đại diện cho toàn bộ merchant Tendoo.
        - Kịch bản khảo sát là giải pháp NFC Tag với phí 1–2%, không phải Visa Accept. "Sẵn sàng triển khai" mới là ý định, chưa phải hành vi thật.
        - Một số tỉ lệ trong báo cáo dùng mẫu số không thống nhất (127 và 132). Outline dùng tỉ lệ trên 132 merchant.
    - "Nhu cầu thanh toán của khách quốc tế đến Việt Nam", khảo sát 10 khách quốc tế, 16/10/2026 *(cần ghi rõ đơn vị thực hiện)*. Lưu ý khi trích dẫn:
        - Khảo sát thăm dò, cỡ mẫu nhỏ (10 người; Đông Nam Á 4, châu Âu 2, Trung Quốc, Nhật Bản, Bắc Mỹ, châu Đại Dương mỗi nhóm 1). Không suy rộng theo quốc tịch.
        - Kịch bản khảo sát thu phí 5% của khách, khác với Visa Accept.
    - NQ 198/2025/QH15 (bỏ thuế khoán từ 01/01/2026)
    - [Hỗ trợ hộ kinh doanh chuyển đổi số và kê khai thuế – VnEconomy](https://vneconomy.vn/ho-tro-ho-kinh-doanh-chuyen-doi-so-va-ke-khai-thue.htm)
    - [Kết quả triển khai hóa đơn điện tử – Thời báo Tài chính](https://thoibaotaichinhvietnam.vn/infographics-ket-qua-trien-khai-hoa-don-dien-tu-197840-197840.html)
    - [Tammi vượt 5 triệu người dùng – VnExpress 19/08/2026](https://vnexpress.net/ung-dung-tammi-nam-trong-top-tai-nhieu-tai-viet-nam-5110618.html)
    - [21,2 triệu lượt khách quốc tế 2025 – Báo Chính phủ](https://en.baochinhphu.vn/foreign-arrivals-soar-to-record-high-in-2025-111260106100233228.htm)
    - [Khách quốc tế 9 tháng 2026 tăng 14,5% – Báo Văn hóa](https://baovanhoa.vn/du-lich/khach-quoc-te-den-viet-nam-9-thang-2026-tang-145-271196.html)
    - [Chi tiêu bình quân và cơ cấu chi tiêu khách quốc tế 2019, Niên giám thống kê 2022 – VietNamNet](https://vietnamnet.vn/di-du-lich-viet-nam-khach-nuoc-nao-chi-tien-manh-tay-nhat-2167403.html); [CafeBiz](https://cafebiz.vn/den-viet-nam-du-khach-nuoc-nao-manh-tay-chi-tien-nhat-chi-tien-nhieu-nhat-vao-khoan-gi-176230718085444009.chn)
    - [Thu 15,22 tỷ USD từ khách quốc tế 2025, khoảng 718 USD mỗi lượt – Dân trí](https://dantri.com.vn/kinh-doanh/chi-tieu-khach-tay-den-viet-nam-va-nguoi-viet-ra-nuoc-ngoai-nghich-ly-can-loi-giai-20260906232044127.htm)
    - [Cơ cấu thanh toán tại điểm bán Hàn Quốc 2024, Worldpay GPR 2025 – Payments CMI](https://paymentscmi.com/insights/south-korea-2025-payments-ecommerce-trends/)
    - [Thẻ chiếm 71% chi tiêu tại cửa hàng ở Mỹ 2025 – Global Payments](https://investors.globalpayments.com/news-events/press-releases/detail/504/gen-z-driving-the-shift-from-cards-to-digital-wallets-new)
    - [Alipay, WeChat Pay chiếm 87% giá trị tại điểm bán ở Trung Quốc, Worldpay GPR 2026 – Rich Turrin](https://richturrin.substack.com/p/what-asia-knew-first-digital-wallets)
    - [Tiền mặt ở Nhật Bản khoảng 38% chi tiêu tại cửa hàng, Worldpay GPR 2026 – Dwayne Gefferie](https://dwaynegefferie.substack.com/p/three-things-the-worldpays-global)
    - [Thẻ ở Úc, Anh khoảng 67–70% – Payments CMI](https://paymentscmi.com/insights/top-global-payment-methods/)
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

## Ghi chú giải pháp Visa Accept (cho người trình, không đưa lên slide)

Mục này giúp người trình dùng từ cho chuẩn và trả lời khi được hỏi sâu.

- **Bản chất:** Visa Accept biến chủ thẻ Visa (ghi nợ, trả trước) thành người bán. Merchant dùng thẻ Visa đang có để nhận tiền. **VDF không phát hành thẻ.** SDK Visa Accept được tích hợp vào app Tendoo.
- **Cách nói chuẩn:**
    - Dùng "nhận thẻ ngay trên điện thoại", "chạm thẻ", "trả qua link".
    - Không nói "VDF phát hành thẻ cho merchant".
    - Không nói "nhận mọi loại thẻ". Hiện tại là thẻ Visa và Mastercard khi chạm; với link thì xác nhận lại loại thẻ được nhận.
    - Không nói "chạy trên mọi điện thoại". Chạm thẻ chỉ chạy trên Android có NFC; iPhone dùng trả qua link.
- **Hai cách nhận tiền:**
    - Chạm thẻ (Tap to Phone, Android): nhận thẻ Visa, Mastercard và ví trên điện thoại.
    - Trả qua link (Pay by Link): khách quét mã QR trên điện thoại cửa hàng hoặc nhận link qua SMS, email, rồi nhập thẻ; có xác thực 3-D Secure.
- **Hạn mức (theo Visa):** khoảng 100 triệu đồng (4.000 USD) và 2.000 giao dịch mỗi tháng; khoảng 8 triệu đồng (300 USD) mỗi giao dịch.
- **Phí (theo Visa):**
    - MDR với merchant gần như bằng 0.
    - Phí mạng lưới đến 31/01/2027: IRF và phí acquirer mỗi loại 10bps, tối đa 250đ mỗi giao dịch.
    - Từ 01/02/2027: giao dịch dưới 200.000đ miễn phí; từ 200.000đ trở lên, IRF 200đ và phí acquirer 0,002 USD.
- **Tiền về:** gần như tức thì, vào thẻ Visa của merchant.
- **Lộ trình nâng gói của Visa:**
    - Merchant chạm hạn mức Visa Accept thì không giao dịch tiếp được trong tháng đó.
    - Merchant được mời nâng lên gói SMB: MDR dưới 1%, khoảng 180 triệu đồng (7.000 USD) mỗi tháng, không giới hạn số giao dịch và giá trị mỗi giao dịch.
    - Sau đó lên gói nhận thẻ đầy đủ theo biểu phí chuẩn, dùng nhiều loại thiết bị.
- **Kiểm soát rủi ro:** theo dõi tần suất giao dịch, giới hạn hạn mức, 3-D Secure cho giao dịch qua link, chức năng hoàn tiền, báo cáo doanh số và đối soát.
- **Đã triển khai tại Việt Nam:** VPBank (TapLink), Sacombank, VIB (BizPay).
- **Sản phẩm Visa khác có thể dùng ở phase sau:**
    - Visa QR Connector: Viettel Money làm cầu nối QR, du khách quét mã bằng ví có thẻ Visa.
    - Visa Acceptance Platform: Pay by Link, Tap to Phone, quản lý token, công cụ chống gian lận Decision Manager.

## Câu hỏi Tổng giám đốc có thể hỏi xoáy

1. **"VPBank, Sacombank, VIB đã có Visa Accept rồi. VDF làm sau thì khác gì?"** Ở ngân hàng, Visa Accept chỉ là một nút trong app, chờ khách hàng tự bật. VDF đưa Visa Accept vào phần mềm bán hàng Tendoo, đến tệp hộ kinh doanh Tendoo qua đội kênh bán thực địa, kèm trợ lý tư vấn đa ngôn ngữ (slide 7, 16).
2. **"Phí gần như bằng 0 thì VDF kiếm tiền ở đâu?"** Phase 1 là giai đoạn có merchant hoạt động thật. Doanh thu đến khi merchant vượt hạn mức và nâng lên gói SMB (MDR dưới 1%), từ thanh toán nội địa và dịch vụ AI ở các phase sau (phụ lục, mô hình doanh thu). Khảo sát cho thấy merchant chấp nhận mức phí 1–2% (81,5% sẵn sàng dùng), nên MDR dưới 1% ở gói SMB là mức merchant chấp nhận được. Cần số theo kịch bản.
3. **"Hạn mức 8 triệu mỗi giao dịch, 100 triệu mỗi tháng có đủ không?"** Đủ cho phần lớn hộ kinh doanh nhỏ phục vụ du khách. Cửa hàng vượt hạn mức được nâng lên gói SMB, và đó cũng là lúc VDF bắt đầu thu MDR.
4. **"NAPAS đã có QR xuyên biên giới, sao VDF lại làm Visa Accept?"** QR chỉ dùng được với khách từ 6 nước đã kết nối. Thẻ Visa và Mastercard thì khách từ nước nào cũng có. QR được xem xét ở Phase 3 (slide 5, 19).
5. **"Khách Trung Quốc chủ yếu dùng Alipay, WeChat Pay. Có phục vụ được không?"** Phase 1 chưa phục vụ khách chỉ dùng ví nước mình. Pilot ưu tiên điểm có nhiều khách dùng thẻ.
6. **"Merchant dùng iPhone thì sao?"** Vẫn nhận được tiền qua link; chạm thẻ cần điện thoại Android.
7. **"Đội kênh bán của VTT chính là kênh đã tạo ra merchant ảo. Lần này khác gì?"** Chỉ tiêu theo cửa hàng phát sinh giao dịch, không theo số tài khoản mở.
8. **"Sao không để Tammi làm app thanh toán cho du khách như Alipay?"** Tammi hiện chỉ phục vụ người dùng Việt. Du khách đã có thẻ và app nước họ, nên phía còn thiếu là cửa hàng nhận tiền. Bài học từ WeChat Pay, KakaoPay được áp dụng cho Tammi với người dùng Việt ở Phase 2 (phụ lục).
9. **"Làm sao biết GMV tăng là nhờ AI chứ không phải nhờ nhận được thẻ?"** Bước 1a là mốc nền, bước 1b đo phần tăng thêm và tách riêng GMV từ đơn có tương tác với trợ lý (slide 20).
10. **"Nếu Tammi chậm xây Shop, Live thì sao?"** Phase 1 vẫn chạy được: pilot miniapp chỉ cần Tammi cho phép trợ lý hoạt động trong miniapp, không cần Shop và Live. Trợ lý livestream và tin nhắn chạy trước trên website bán hàng và mạng xã hội mà Tendoo đang kết nối (slide 15).
11. **"Khảo sát khách chỉ có 10 người, có tin được không?"** Đây là khảo sát thăm dò, chỉ dùng làm tín hiệu bổ sung. Bằng chứng chính là khảo sát 132 merchant. Pilot sẽ đo giao dịch thật thay cho ý định khảo sát.
12. **"Vì sao VDF làm Merchant AI Studio, mà không để Tendoo hay Viettel AI làm?"** Trợ lý là cửa vào của giao dịch: mỗi cuộc trò chuyện kết thúc bằng một đơn và một lần trả tiền. VDF giữ lớp này thì mọi luồng có tiền đều đi qua thanh toán VDF. Tendoo cung cấp dữ liệu và tích hợp vào app (slide 11, 18).
13. **"Có số liệu nào cho thấy khách bỏ đi vì không hỏi được không?"** Chưa có; hai khảo sát hiện tại chỉ hỏi về thanh toán. Đây là giả thuyết, pilot đo bằng lượt quét QR và tỉ lệ đặt hàng sau khi quét. Bước 1a (chỉ thanh toán) là mốc so sánh (slide 20).

## Thông tin còn thiếu

| Ưu tiên | Nội dung | Phục vụ slide |
| --- | --- | --- |
| Cao | Số merchant Tendoo chính xác (tổng, active) | 10, 11 |
| Cao | Cơ chế phí Visa Accept: IRF, phí acquirer do bên nào trả, bên nào nhận; VDF nhận được phần nào | Phụ lục (mô hình doanh thu) |
| Trung bình | Trả qua link nhận những loại thẻ nào | 13, 16 |
| Trung bình | Tỉ lệ merchant Tendoo đã có thẻ Visa và đang dùng Android | 13, 19 |
| Trung bình | Kết quả triển khai Visa Accept của VPBank, Sacombank, VIB | 7, 16 |
| Trung bình | Nguồn xác nhận hợp tác VNPAY – Mastercard cho du khách | 6 |
| Trung bình | Cách khách quốc tế trả tiền **tại Việt Nam** theo quốc tịch (đã có số liệu thói quen ở nước của khách; số đo tại Việt Nam xin Visa, NAPAS) | 3, 16, 19 |
| Thấp | Đối chiếu số liệu Worldpay của Úc, Anh, Nhật Bản với báo cáo gốc | 3 |
| Trung bình | Đơn vị thực hiện hai khảo sát | 8, 9 |
| Thấp | Ước tính doanh thu theo kịch bản; tỉ lệ merchant nâng gói | Phụ lục |
| Thấp | Kiểm tra lại số liệu case thế giới (chủ yếu do doanh nghiệp công bố) | Phụ lục |
| Trung bình | Chụp ảnh minh họa 3 giải pháp hiện có (QR quốc tế, app Việt Nam liên kết thẻ, Tap to Phone) | 5, 6, 7 |
| Thấp | Kịch bản và video demo giải pháp VDF | 17 |
| Trung bình | Số liệu về rào cản ngôn ngữ tại cửa hàng (hỏi bổ sung merchant và khách quốc tế, hoặc nguồn ngoài) | 10, 14 |
