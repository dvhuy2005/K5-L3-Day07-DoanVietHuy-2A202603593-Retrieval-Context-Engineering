# Tình trạng bài nộp Lab 7

## Đã có và kiểm tra được

- [x] Kết nối Chroma và embedding của Lab 6; lệnh kiểm tra trả ID, trang và nội dung.
- [x] Export 440 chunk và benchmark 24 câu đúng cơ cấu 17 dev / 7 test.
- [x] Test mới độc lập với 5 câu test đã xem ở Lab 6; evidence của 20 câu có đáp án nằm trọn trong chunk đúng nguồn/trang.
- [x] Ba cách tìm: dense, TF-IDF, hybrid RRF; trace và metrics dev.
- [x] Hai cấu hình thử cải thiện, phân tích ít nhất hai lỗi dev và chốt cấu hình trước test.
- [x] Chạy retrieval baseline và cấu hình chọn trên test; lưu top-k, context, thời gian.
- [x] Code agent Gemini, tool search, citation, abstention, lưu trace/usage/lỗi; 22 kiểm thử offline qua.
- [x] README tái lập, requirements và báo cáo cá nhân trung thực.

## Kết quả model thật

- [x] Chạy một câu thử `src.run_live` trong terminal có `GEMINI_API_KEY`: sau khi sửa context, Gemini trả lời có nguồn trang 10.
- [x] Chạy agent trên dev và baseline/cấu hình chốt trên cùng test: bốn lượt hoàn thành, không có lỗi provider.
- [x] Đối chiếu cả 7 câu test của mỗi cấu hình với chunk nguồn, tạo nhãn có AI hỗ trợ và tổng hợp grounded answer, citation validity, abstention.
- [x] Cập nhật mục Agent của báo cáo bằng số liệu thật.
- [ ] Người học xác nhận nhãn đối chiếu và link repo sau khi push.

Trạng thái hiện tại: `gemini-3.8-flash` tạo nội dung trả `HTTP 000`, nhưng `gemini-3.5-flash-lite` hoàn thành benchmark. Trên test, cấu hình chọn đạt 3/5 câu có bằng chứng và từ chối đúng 2/2 câu thiếu bằng chứng theo nhãn có AI hỗ trợ. API key tạm đã được xóa sau khi chạy. Chi phí tiền thực tế không được provider cung cấp nên để `null`. Repo cá nhân do người học cung cấp: `https://github.com/dvhuy2005/K5-L3-Day07-DoanVietHuy-2A202603593-Retrieval-Context-Engineering`.
