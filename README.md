# Day 7 — Agentic RAG

## Bài thực hành của Đoàn Việt Huy (2A202603593)

Phần đã chạy thật: 440 chunk NIST từ Lab 6; benchmark 24 câu; dense, TF-IDF và hybrid RRF; bảng dev/test và trace retrieval trong `results/`. Agent Gemini đã chạy cả hai cấu hình trên dev và test. Cấu hình chọn trả lời đúng 3/5 câu test có bằng chứng, từ chối đúng 2/2 câu thiếu bằng chứng, theo nhãn đối chiếu có AI hỗ trợ đang chờ người học xác nhận. Xem [báo cáo cá nhân](report/individual/2A202603593_DoanVietHuy.md).

Chạy từ thư mục gốc repo Lab 7 trên Windows PowerShell. Giữ repo [Lab 6 đã hoàn thành](https://github.com/dvhuy2005/K5-L3A-DAY06-DoanVietHuy-2A202603593-DataIngestion) cạnh thư mục `Lab7`, với PDF, manifest, benchmark, Chroma index và FastEmbed cache của lần chạy Lab 6. Nếu chưa có, clone repo Lab 6 và làm theo README của repo đó để tái tạo index. Sử dụng Python 3.11+ với `requirements.txt`; trên máy hiện tại có thể dùng Python của môi trường Lab 6:

```powershell
$py = '..\..\Lab6\K5-L3A-DAY06-DoanVietHuy-2A202603593-DataIngestion\.venv\Scripts\python.exe'
$day6 = '..\..\Lab6\K5-L3A-DAY06-DoanVietHuy-2A202603593-DataIngestion'
& $py -X utf8 -m unittest discover -s tests -v
& $py starter\prepare_day7.py --day6-root $day6
& $py -m src.evaluate_retrieval --day6-root $day6 --split dev --method dense --top-k 3 --budget 800 --output results/dev_dense_k3_b800
& $py -m src.evaluate_retrieval --day6-root $day6 --split dev --method tfidf --top-k 3 --budget 800 --output results/dev_tfidf_k3_b800
& $py -m src.evaluate_retrieval --day6-root $day6 --split dev --method hybrid_rrf --top-k 3 --budget 800 --output results/dev_hybrid_rrf_k3_b800
```

Các cấu hình k/budget khác và phép chọn trước test nằm trong [bản chốt](results/config_selection.md). Test chỉ chạy **sau khi chốt trên dev**. Kết quả test retrieval đã lưu gồm baseline `results/test_dense_k3_b800` và cấu hình chọn `results/test_dense_k10_b3000`.

Để chạy agent thật, đặt `GEMINI_API_KEY` trong terminal của bạn, **không ghi key vào repo hoặc gửi trong chat**. Có thể nhập kín trong PowerShell:

```powershell
$secret = Read-Host 'Gemini API key' -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new('', $secret).Password
Remove-Variable secret
& $py -m src.run_live --day6-root $day6 --question 'NIST gọi hiện tượng AI tự tin tạo nội dung sai là gì?' --model gemini-3.5-flash-lite --output results/agent_smoke
```

Để tái lập kết quả agent đã lưu, chạy trên dev và sau đó baseline/cấu hình chọn trên test:

```powershell
& $py -m src.run_live --day6-root $day6 --split dev --method dense --top-k 3 --budget 800 --output results/agent_dev_baseline
& $py -m src.run_live --day6-root $day6 --split dev --method dense --top-k 10 --budget 3000 --output results/agent_dev_selected
& $py -m src.run_live --day6-root $day6 --split test --method dense --top-k 3 --budget 800 --output results/agent_test_baseline
& $py -m src.run_live --day6-root $day6 --split test --method dense --top-k 10 --budget 3000 --output results/agent_test_selected
```

Mỗi lệnh lưu `traces.json` và `summary.json`. Nếu provider lỗi, chương trình ghi lỗi và dừng sau câu đầu; không gán điểm giả. Đọc bằng chứng, câu trả lời và citation trước khi điền nhãn thủ công theo [BENCHMARK.md](BENCHMARK.md). `starter/agent_metrics.py` chỉ tổng hợp nhãn đã được người học xác nhận, không tự chấm nội dung.

Trace, phiếu đọc và nhãn đối chiếu có AI hỗ trợ của cả hai lượt test đã có trong `results/agent_test_*`. Nhãn này chưa phải đánh giá độc lập của người học. Để xác nhận, đọc từng câu trả lời cùng đoạn nguồn rồi sao chép nhãn sang `reviews.json`; **không chạy metric bằng nhãn trống**:

```powershell
& $py -m src.make_review_sheet --traces results/agent_test_selected/traces.json --split test --output results/agent_test_selected/review_sheet.md
# Đọc review_sheet.md và các chunk được dẫn; sao chép reviews_ai_assisted.json thành reviews.json rồi chỉnh nhãn nếu cần.
& $py starter/agent_metrics.py --cases data/benchmark_day7.json --traces results/agent_test_selected/traces.json --reviews results/agent_test_selected/reviews.json --split test --output results/agent_test_selected/agent_metrics.json
```

**Bài cá nhân · Python 3.11+ · tiếp nối Day 6**

Dùng embedding và vector store từ Day 6 để xây một agent biết tìm bằng chứng, trả lời có nguồn và nhận biết khi không đủ thông tin. Bạn tự chọn kiến trúc, số tool và cách tổ chức retrieval.

> **Tùy chọn:** [Gợi ý dùng AI để lập trình](AGENT_SETUP.md) giúp bạn làm lab; phần này không bắt buộc và không tính điểm.

## Bài cần làm

![Agent tìm tài liệu trong kho Day 6 và trả lời có nguồn](assets/retrieval-pipeline.svg)

1. Kết nối dữ liệu, embedding và vector store Day 6.
2. Xây agent dùng model thật và ít nhất một khả năng truy xuất dữ liệu. Agent có thể dùng nhiều tool và nhiều lượt gọi.
3. Thử **ít nhất 3 phương pháp retrieval khác nhau**, trong đó có dense retrieval dùng vector store Day 6. Tự chọn các phương pháp còn lại; xem [gợi ý](GUIDE.md#2-thử-các-phương-pháp-retrieval).
4. Thử nhiều cấu hình, benchmark, phân tích lỗi và chọn cấu hình tốt trên **dev**; sau đó đánh giá trên **test**.

Benchmark tối thiểu có **24 câu**: dev gồm 15 câu có đáp án và 2 câu thiếu bằng chứng; test gồm 5 câu có đáp án và 2 câu thiếu bằng chứng. Xem [benchmark](BENCHMARK.md) và [rubric](RUBRIC.md).

## Thử thách nâng cao · +15 điểm

Index một tài liệu thực tế từ **100 trang** có bảng, ảnh và biểu đồ; xây agent truy xuất và trả lời các câu hỏi về nội dung đó. Hoàn thành [thử thách nâng cao](ADVANCED.md) và đạt **ít nhất 90% benchmark test** để nhận 15 điểm bonus. Phần cơ bản tối đa 85 điểm; toàn bài tối đa 100 điểm.

## Bắt đầu

Để kiểm tra bước 1 trên máy đã hoàn thành Day 6, chạy bằng môi trường Python của
Day 6 (có sẵn `chromadb` và `fastembed`):

```powershell
& '..\..\Lab6\K5-L3A-DAY06-DoanVietHuy-2A202603593-DataIngestion\.venv\Scripts\python.exe' starter\check_day6_connection.py 'Người dùng gặp rủi ro gì khi tin thông tin sai do AI tạo ra?'
```

Chạy từ thư mục gốc repo Day 7. Lệnh chỉ đọc index, in ra ID, nội dung, trang và nguồn
của ba đoạn gần câu hỏi nhất; đây là kiểm tra kết nối, chưa phải câu trả lời của agent.
Nếu Day 6 nằm ở chỗ khác, truyền thêm `--day6-root <đường-dẫn>`.

1. Đọc [hướng dẫn](GUIDE.md), [rubric](RUBRIC.md) và [quy tắc](RULES.md).
2. Tạo repo cá nhân theo [cách nộp bài](SUBMISSION.md), chuẩn bị đầu ra Day 6 và model hỗ trợ tool calling.
3. Dùng hoặc thay thế [starter](starter/README.md); bạn cần kết nối model và vector store thật.
4. Chạy `python -m unittest discover -s tests -v`. Test mock chỉ kiểm tra code, không phải benchmark agent thật.

![Các bước thử nghiệm trên dev và đánh giá trên test](assets/experiment-loop.svg)

Nộp code, cách chạy, cấu hình, benchmark, trace và [báo cáo](report/individual/MSSV_HoTen.md). Thời gian ở [checkpoints](CHECKPOINTS.md) là gợi ý, có thể điều chỉnh theo lớp và phạm vi thử nghiệm.
