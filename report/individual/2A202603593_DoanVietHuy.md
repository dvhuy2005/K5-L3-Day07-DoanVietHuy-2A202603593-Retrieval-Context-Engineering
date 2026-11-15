# Báo cáo Lab 7 — Agentic RAG

Học viên: Đoàn Việt Huy · MSSV: 2A202603593 · Lớp: L3A

## 1. Mục tiêu và dữ liệu

Hệ thống dùng kho tri thức NIST AI 600-1 từ [Lab 6](https://github.com/dvhuy2005/K5-L3A-DAY06-DoanVietHuy-2A202603593-DataIngestion) để tìm bằng chứng, đưa đoạn phù hợp vào context và trả lời kèm ID nguồn. Nếu không có đủ bằng chứng, agent phải từ chối trả lời. Bài này tách riêng điểm tìm kiếm, điểm context và chất lượng câu trả lời.

- Nguồn: PDF *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* (NIST AI 600-1, July 2024). Manifest Lab 6 ghi URL chính thức, SHA-256 và quy tắc đếm 45 trang nội dung (trang vật lý 5–49). Tài liệu NIST công khai; kiểm tra quyền riêng của nội dung bên thứ ba trước khi tái sử dụng.
- Chunks: 440 mẩu theo đoạn/câu, export từ collection `lab6_paragraph` của Chroma; ID, nguồn, trang và nhãn phần được giữ nguyên trong `data/nist_chunks.json`.
- Vector store: Chroma cosine tại kho Lab 6; embedding FastEmbed `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, 384 chiều. Query dùng cùng model và cache để không lệch vector.
- Model điều phối: Gemini qua native GenerateContent API, mặc định `gemini-3.5-flash-lite`; tên model, số lượt tìm và context budget có thể đổi bằng CLI. API key chỉ lấy từ biến môi trường.

Benchmark `data/benchmark_day7.json` gồm 24 câu: **dev 15 có bằng chứng + 2 thiếu; test 5 có bằng chứng + 2 thiếu**. 15 câu dev lấy từ Lab 6; 5 câu test cũ Lab 6 đã được xem khi phân tích kết quả nên **không tái sử dụng**. Năm câu test có bằng chứng mới ở trang 21, 23, 24, 36, 48; mỗi trích đoạn được script xác nhận nằm trọn trong một chunk đúng nguồn/trang. Bốn câu thiếu bằng chứng được thiết kế gần chủ đề nhưng yêu cầu thông tin ngoài phạm vi tài liệu; lý do vắng bằng chứng ghi trong benchmark. Đây là nhãn soạn và kiểm tra có hỗ trợ AI; người học cần đọc lại bằng chứng khi nộp.

## 2. Ba phương pháp tìm và cấu hình

1. **Dense:** câu hỏi được embed rồi tìm gần nhất trên Chroma từ Lab 6.
2. **TF-IDF:** so khớp từ trên cùng 440 chunk, chạy offline.
3. **Hybrid RRF:** lấy tối đa 20 ứng viên từ mỗi cách trên, cộng điểm hạng `1/(60 + rank)`, sau đó xếp lại. Không cộng trực tiếp score cosine và TF-IDF vì chúng khác thang đo.

Các phương pháp dùng cùng corpus, câu hỏi và filter `section` chỉ khi filter có trong câu hỏi. `gold`, đáp án chuẩn và trang đúng không được truyền vào retriever hay agent. Hit@1 và Evidence Hit@3 chấm mẩu phải **chứa nguyên văn evidence** ở đúng nguồn/trang. Context Evidence Rate chỉ đếm bằng chứng thật sự có trong context cuối. Mẫu số chỉ gồm câu có đáp án; câu thiếu bằng chứng được đánh giá riêng bằng abstention.

| Cấu hình | Vai trò | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Trung vị tìm + đóng gói |
|---|---|---|---:|---:|---:|---:|
| Dense, k=3, 800 ký tự | Baseline | dev | 2/15 | 3/15 | 3/15 | 17.75 ms |
| TF-IDF, k=3, 800 ký tự | Phương pháp 2 | dev | 1/15 | 2/15 | 1/15 | 0.58 ms |
| RRF, k=3, 800 ký tự | Phương pháp 3 | dev | 1/15 | 3/15 | 1/15 | 19.26 ms |
| RRF, k=5, 1600 ký tự | Cải thiện 1 | dev | 1/15 | 3/15 | 3/15 | 19.28 ms |
| Dense, k=5, 1600 ký tự | Cải thiện 2 | dev | 2/15 | 3/15 | 3/15 | 17.87 ms |
| RRF, k=10, 3000 ký tự | Thử context lớn | dev | 1/15 | 3/15 | 5/15 | 19.70 ms |
| **Dense, k=10, 3000 ký tự** | **Đã chọn** | dev | **2/15** | **3/15** | **5/15** | **17.51 ms** |
| Dense, k=3, 800 ký tự | Baseline | test mới | 1/5 | 3/5 | 2/5 | 18.85 ms |
| **Dense, k=10, 3000 ký tự** | **Đã chọn** | test mới | **1/5** | **3/5** | **3/5** | **18.14 ms** |

Chọn cấu hình trên dev theo Context Evidence Rate, sau đó Evidence Hit@3, Hit@1, thời gian và độ đơn giản. [Bản chốt trước khi chạy test](../../results/config_selection.md) ghi rõ các giả thuyết và lựa chọn. Chi phí API cho retrieval tại máy là 0 USD; thời gian trên là trung vị của một lần chạy, không gồm tải model/index lần đầu. Context lớn hơn giúp đưa thêm một mẩu đúng vào test, nhưng không sửa được thứ hạng top 3.

### Hai lỗi dev đã đọc

- `q02`: trang 10 xuất hiện ở hạng 2 nhưng **chunk được tìm không chứa chính câu evidence**. Nếu chấm theo trang sẽ nhầm thành thành công; nhãn chunk cho thấy không đủ bằng chứng. Thử tăng k và budget vẫn không đưa đúng chunk vào context; cần cải thiện ranking hoặc chọn chunk lân cận.
- `q04`: bằng chứng trang 12 không vào top 5; câu hỏi tiếng Việt và nguồn tiếng Anh làm truy xuất khó. Tăng context không giúp khi ứng viên đúng chưa được tìm. Hướng thử tiếp là dịch/mở rộng query rồi đo riêng trên dev.

Trace, danh sách chunk top-k, context cuối và thời gian từng câu nằm trong `results/dev_*/traces.json` và `results/test_*/traces.json`. Kết quả thấp được giữ nguyên, không đổi benchmark hay chấm lại bằng trang đơn thuần.

Đối chiếu đủ 5 câu test có đáp án theo thang context 0/1/2 trong [phiếu đọc context](../../results/context_review_test.md): baseline có 3/0/2 câu ở mức 0/1/2; cấu hình chọn có 2/0/3. Đây là context của một lượt retrieval, khác với context sau nhiều lượt tìm của agent.

## 3. Agent và đánh giá câu trả lời

`starter/agentic.py` giới hạn số lượt tìm và kiểm tra citation ID phải có trong context. `src/gemini_controller.py` yêu cầu model gọi hàm `search` ở lượt đầu, sau đó model có thể tìm tiếp hoặc trả lời. `src/retrieval.py` nối hàm tìm với dense/TF-IDF/RRF; `src/run_live.py` lưu từng model call, tool call, tham số, kết quả, context cuối, câu trả lời, citation, thời gian, usage và lỗi. Nội dung tài liệu là dữ liệu, không phải chỉ dẫn. ID citation hợp lệ **chưa chứng minh** câu trả lời được hỗ trợ; cần đọc thủ công từng claim.

Lần chạy **agent thật trên dev baseline** đã hoàn tất 17/17 câu: 8 answered, 9 abstain, 0 provider errors, 70 model calls, 30.928 input tokens và 2.416 output tokens theo `usageMetadata`. Hai câu thiếu bằng chứng đều bị từ chối; các câu có đáp án bị từ chối cũng cần tính là lỗi. Đây là số lượng trạng thái, **chưa phải điểm grounded answer**. Phiếu đọc ở `results/agent_dev_baseline/review_sheet.md`.

Lần chạy **agent thật trên dev cấu hình chọn** cũng hoàn tất 17/17 câu: 15 answered (toàn bộ câu có đáp án), 2 abstain (hai câu thiếu bằng chứng), 0 provider errors, 51 model calls, 43.987 input tokens và 2.830 output tokens. Context lớn giúp agent có nhiều bằng chứng để trả lời, đồng thời tăng token đầu vào; các câu answered vẫn cần đọc lại để phát hiện trả lời sai hoặc citation không hỗ trợ. Phiếu đọc ở `results/agent_dev_selected/review_sheet.md`.

Ví dụ lỗi agent `q10`: câu hỏi nhắm tới việc ghi lại nguồn gốc/lịch sử của dữ liệu huấn luyện và dữ liệu tạo ra, nhưng model nêu tài liệu về lịch sử sửa nội dung và thay đổi do bên thứ ba. Hai citation dẫn tới các đoạn thật hỗ trợ từng câu model nói, song câu trả lời lệch trọng tâm so với bằng chứng chuẩn. Cần chấm riêng tính đúng của câu trả lời và tính hỗ trợ của citation; không coi citation đúng ID là đáp án đạt.

**Trạng thái thực nghiệm Gemini:** `gemini-3.8-flash` đã hết thời gian khi tạo nội dung (`HTTP 000`), dù GET danh sách model với key trả 200. Chuyển sang `gemini-3.5-flash-lite`. Lần thử đầu: 5 model calls, 4 lượt tìm, abstain; trace cho thấy lượt tìm thứ hai tìm được định nghĩa trang 10 nhưng context cũ chiếm chỗ. Sau khi ưu tiên kết quả tìm mới, cùng câu hỏi được trả lời đúng “Confabulation” với citation `nist-ai-600-1-p010-para-000-000` sau 3 model calls và 2 lượt tìm. Đây là lỗi được tìm và sửa trên dev trước khi chốt test.

Sau khi chốt cấu hình, agent thật đã chạy trên cả 7 câu test ở baseline và cấu hình chọn. Bảng sau là **nhãn đối chiếu có AI hỗ trợ**, đọc câu trả lời và nguyên văn từng đoạn được trích; người học cần xác nhận nhãn trước khi nộp. Điểm 0/1/2 chỉ tính 5 câu có đáp án, không gộp 2 câu thiếu bằng chứng.

| Chỉ số test | Baseline dense k=3, 800 ký tự | Đã chọn dense k=10, 3000 ký tự |
|---|---:|---:|
| Câu chạy xong / lỗi provider | 7/7 · 0 | 7/7 · 0 |
| Có gọi tool tìm kiếm | 7/7 | 7/7 |
| Số lượt tìm mỗi câu | 1 lượt: 1 câu; 4 lượt: 6 câu | 1 lượt: 2 câu; 2 lượt: 2 câu; 4 lượt: 3 câu |
| Grounded answer 0 / 1 / 2 | 3 / 0 / 2; trung bình 0,8/2 | 2 / 0 / 3; trung bình 1,2/2 |
| Citation có hỗ trợ / tổng citation | 2/2 | 3/3 |
| Câu trả lời có citation / câu được trả lời | 2/2 | 3/3 |
| Từ chối đúng câu thiếu bằng chứng | 2/2 | 2/2 |
| Từ chối sai câu có đáp án | 3/5 | 2/5 |
| Model calls; input / output tokens | 32; 14.964 / 835 | 25; 23.372 / 718 |
| Tổng thời gian theo trace | 211,66 giây | 121,78 giây |

Hai câu `d7-t01` và `d7-t02` được cả hai cấu hình trả lời đúng với trích dẫn trang 21 và 23. `d7-t04` chỉ cấu hình chọn trả lời đúng, trích trang 36. `d7-t03` bị cả hai từ chối dù bằng chứng trang 24 nằm trong context retrieval của cấu hình chọn: đây là lỗi đọc hoặc quyết định trả lời của agent, không đơn thuần là lỗi tìm kiếm. `d7-t05` bị cả hai từ chối; câu MG-3.2-008 trang 48 chưa vào context của hai cấu hình. Hai câu hỏi vượt phạm vi tài liệu (`d7-t06`, `d7-t07`) đều được từ chối. Phiếu đọc và nhãn từng câu nằm trong `results/agent_test_{baseline,selected}/review_sheet.md` và `reviews_ai_assisted.json`; metric tương ứng ở `agent_metrics_ai_assisted.json`. Để chấm chính thức, người học cần đọc và xác nhận nhãn. API không báo giá tiền thực tế, vì vậy `api_cost_usd` được giữ `null`, không suy ra USD từ token.

## 4. Giới hạn và cách tái lập

Chất lượng retrieval bị hạn chế bởi câu hỏi tiếng Việt, tài liệu tiếng Anh, chỉ một tài liệu NIST và kích thước benchmark nhỏ. RRF theo TF-IDF hiện không vượt dense ở Hit@1. Agent đã trả lời đúng 3/5 câu test có bằng chứng ở cấu hình chọn; cần thêm cách truy xuất theo mã hành động để giảm từ chối sai. Test đã được dùng để đánh giá nên mọi cải tiến tiếp theo cần bộ test mới. Cách cài, lệnh export, chạy ba phương pháp, chạy agent và chấm nhãn ở [README](../../README.md). Kiểm thử code bằng `python -X utf8 -m unittest discover -s tests -v`.

Thử thách nâng cao 100 trang không thực hiện; PDF hiện dùng có 45 trang nội dung theo quy tắc manifest.
