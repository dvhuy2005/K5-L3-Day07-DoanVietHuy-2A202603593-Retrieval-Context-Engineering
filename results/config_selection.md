# Chốt cấu hình trước khi chạy test Lab 7

Ngày chốt: 2026-11-15. Tập test Lab 7 gồm 5 câu có bằng chứng mới (trang 21, 23, 24, 36, 48) và 2 câu thiếu bằng chứng. Năm câu test cũ của Lab 6 không dùng vì đã xem điểm và nhãn của chúng.

Chỉ dùng 15 câu có bằng chứng trên dev để tính retrieval metrics; 2 câu thiếu bằng chứng không nằm trong mẫu số. Quy tắc chọn sau thí nghiệm dev, trước khi chạy test: ưu tiên **Context Evidence Rate**, sau đó Evidence Hit@3, Hit@1, rồi thời gian và độ đơn giản. Đây là lựa chọn theo dev; không tuyên bố quy tắc đã được đặt trước khi xem dev.

| Cấu hình | Vai trò | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Trung vị tìm + đóng gói |
|---|---|---:|---:|---:|---:|
| Dense, top 3, 800 ký tự | Baseline | 2/15 | 3/15 | 3/15 | 17.75 ms |
| TF-IDF, top 3, 800 ký tự | Cách tìm thứ 2 | 1/15 | 2/15 | 1/15 | 0.58 ms |
| RRF(dense + TF-IDF), top 3, 800 ký tự | Cách tìm thứ 3 | 1/15 | 3/15 | 1/15 | 19.26 ms |
| RRF, top 5, 1600 ký tự | Thử cải thiện 1 | 1/15 | 3/15 | 3/15 | 19.28 ms |
| Dense, top 5, 1600 ký tự | Thử cải thiện 2 | 2/15 | 3/15 | 3/15 | 17.87 ms |
| RRF, top 10, 3000 ký tự | Thử tăng context | 1/15 | 3/15 | 5/15 | 19.70 ms |
| **Dense, top 10, 3000 ký tự** | **Đã chọn** | **2/15** | **3/15** | **5/15** | **17.51 ms** |

Giả thuyết của hai cấu hình cải thiện: thêm ứng viên và tăng context giúp giữ thêm bằng chứng; RRF có thể đưa mẩu cùng được hai cách tìm đánh giá cao lên trước. Kết quả: top 5/budget 1600 cải thiện context của RRF từ 1 lên 3, còn dense không đổi; top 10/budget 3000 đưa cả dense lẫn RRF lên 5. Hit@3 không đổi vì nhiều mẩu đúng nằm sau hạng 3.

Hai lỗi dev điển hình:

- `q02`: trang đúng (10) xuất hiện trong top 2, nhưng mẩu đó **không chứa câu bằng chứng đã gắn nhãn**. Chỉ so trang sẽ tạo hit giả; chấm ở mức đoạn văn cho thấy lỗi.
- `q04`: bằng chứng ở trang 12 không vào top 5; câu hỏi tiếng Việt và tài liệu tiếng Anh làm truy xuất ngữ nghĩa khó. Tăng context không khắc phục được nếu đoạn đúng chưa được tìm thấy.

Chỉ số trên đo retrieval/context, không phải độ đúng câu trả lời của Gemini. Kết quả test và đánh giá agent sẽ được ghi riêng sau đây.
