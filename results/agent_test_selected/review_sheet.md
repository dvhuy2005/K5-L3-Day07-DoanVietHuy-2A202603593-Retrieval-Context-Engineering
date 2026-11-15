# Review test: read the cited chunks before assigning labels

Do not infer citation support from a matching ID alone. Mark each factual claim against the actual chunk text and the full question.

## d7-t01

- Question: Theo GV-1.7-001, tổ chức cần chuẩn bị khả năng nào cho hệ thống AI tạo sinh?
- Answerable: True
- Status: answered
- Agent answer: Theo GV-1.7-001, tổ chức cần thiết lập các quy trình (protocols) để đảm bảo rằng các hệ thống AI tạo sinh (GAI systems) có khả năng được vô
 hiệu hóa (deactivated) khi cần thiết [nist-ai-600-1-p021-para-000-001].
- Citations: ['nist-ai-600-1-p021-para-000-001']
- Expected answer: Có quy trình để vô hiệu hóa hệ thống khi cần.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 21, 'evidence': 'GV-1.7-001 Protocols are put in place to ensure GAI systems are able to be deactivated when necessary.'}]
- Final context IDs: ['nist-ai-600-1-p021-para-000-001', 'nist-ai-600-1-p019-para-001-001', 'nist-ai-600-1-p005-para-000-000', 'nist-ai-600-1-p019-para-000-005', 'nist-ai-600-1-p026-para-000-004', 'nist-ai-600-1-p031-para-002-001', 'nist-ai-600-1-p035-para-001-005', 'nist-ai-600-1-p020-para-000-001', 'nist-ai-600-1-p017-para-000-002', 'nist-ai-600-1-p026-para-000-003']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t02

- Question: Chức năng giám sát tổ chức nên bao phủ những giai đoạn nào của vòng đời AI tạo sinh?
- Answerable: True
- Status: answered
- Agent answer: Chức năng giám sát tổ chức nên bao phủ toàn bộ các giai đoạn của vòng đời AI tạo sinh (GAI), bắt đầu từ khâu hình thành vấn đề (problem formulation) và chuỗi cung ứng cho đến khi cho ngừng hoạt động hệ thống (system decommission) [nist-ai-600-1-p023-para-000-001].
- Citations: ['nist-ai-600-1-p023-para-000-001']
- Expected answer: Từ xác định bài toán và chuỗi cung ứng tới khi ngừng hệ thống.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 23, 'evidence': 'across the GAI lifecycle, from problem formulation and supply chains to system decommission.'}]
- Final context IDs: ['nist-ai-600-1-p023-para-000-001', 'nist-ai-600-1-p046-para-002-000', 'nist-ai-600-1-p022-para-000-000', 'nist-ai-600-1-p020-para-001-000', 'nist-ai-600-1-p048-para-001-000', 'nist-ai-600-1-p021-para-000-000', 'nist-ai-600-1-p047-para-001-000', 'nist-ai-600-1-p044-para-001-000', 'nist-ai-600-1-p021-para-000-003', 'nist-ai-600-1-p026-para-000-008', 'nist-ai-600-1-p005-para-001-001']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t03

- Question: GV-5.1-001 yêu cầu phân bổ những gì cho việc tiếp nhận phản hồi và khắc phục?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Thời gian và nguồn lực.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 24, 'evidence': 'GV-5.1-001 Allocate time and resources for outreach, feedback, and recourse processes in GAI system development.'}]
- Final context IDs: ['nist-ai-600-1-p021-para-000-001', 'nist-ai-600-1-p019-para-001-001', 'nist-ai-600-1-p019-para-000-005', 'nist-ai-600-1-p026-para-000-004', 'nist-ai-600-1-p005-para-000-000', 'nist-ai-600-1-p049-para-001-001', 'nist-ai-600-1-p020-para-000-001', 'nist-ai-600-1-p031-para-002-001', 'nist-ai-600-1-p035-para-001-005', 'nist-ai-600-1-p026-para-000-003']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t04

- Question: Khi rủi ro vượt ngưỡng chấp nhận, MS-2.6-003 yêu cầu làm gì với mô hình đã tinh chỉnh?
- Answerable: True
- Status: answered
- Agent answer: Theo MS-2.6-003, khi rủi ro tiêu cực vượt quá ngưỡng rủi ro của tổ chức, yêu cầu đặt ra là phải đánh giá lại các tính năng an toàn của các mô hình đã được tinh chỉnh (fine-tuned models) [nist-ai-600-1-p036-para-000-003].
- Citations: ['nist-ai-600-1-p036-para-000-003']
- Expected answer: Đánh giá lại các tính năng an toàn của mô hình.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 36, 'evidence': 'MS-2.6-003 Re-evaluate safety features of fine-tuned models when the negative risk exceeds organizational risk tolerance.'}]
- Final context IDs: ['nist-ai-600-1-p036-para-000-003', 'nist-ai-600-1-p034-para-001-002', 'nist-ai-600-1-p046-para-003-004', 'nist-ai-600-1-p027-para-000-003', 'nist-ai-600-1-p032-para-001-005', 'nist-ai-600-1-p044-para-000-001', 'nist-ai-600-1-p033-para-001-003', 'nist-ai-600-1-p048-para-000-003']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t05

- Question: MG-3.2-008 đề xuất dùng cách gì để xem lại nội dung được AI tạo ra khi phù hợp?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Dùng hệ thống kiểm duyệt bởi con người.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 48, 'evidence': 'MG-3.2-008 Use human moderation systems where appropriate to review generated content'}]
- Final context IDs: ['nist-ai-600-1-p046-para-001-000', 'nist-ai-600-1-p049-para-003-001', 'nist-ai-600-1-p046-para-000-002', 'nist-ai-600-1-p049-para-001-001', 'nist-ai-600-1-p046-para-003-004', 'nist-ai-600-1-p045-para-001-001', 'nist-ai-600-1-p048-para-001-002', 'nist-ai-600-1-p047-para-001-001', 'nist-ai-600-1-p023-para-001-002']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t06

- Question: NIST AI 600-1 cho biết tỷ lệ confabulation của Gemini 3.8 Flash vào năm 2026 là bao nhiêu?
- Answerable: False
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: (abstain)
- Gold evidence: Tài liệu xuất bản năm 2024, không thể báo cáo phép đo model ra năm 2026.
- Final context IDs: ['nist-ai-600-1-p005-para-000-000', 'nist-ai-600-1-p023-para-000-000', 'nist-ai-600-1-p019-para-000-000', 'nist-ai-600-1-p026-para-000-000', 'nist-ai-600-1-p033-para-000-000', 'nist-ai-600-1-p045-para-000-000', 'nist-ai-600-1-p025-para-000-000', 'nist-ai-600-1-p035-para-000-000', 'nist-ai-600-1-p041-para-000-000', 'nist-ai-600-1-p043-para-000-000', 'nist-ai-600-1-p049-para-003-001', 'nist-ai-600-1-p047-para-000-001', 'nist-ai-600-1-p048-para-001-006', 'nist-ai-600-1-p049-para-001-001', 'nist-ai-600-1-p044-para-002-002', 'nist-ai-600-1-p035-para-001-003', 'nist-ai-600-1-p048-para-001-004', 'nist-ai-600-1-p014-para-003-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-t07

- Question: NIST AI 600-1 đã chứng nhận sản phẩm AI nào đạt chuẩn vào năm 2026?
- Answerable: False
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: (abstain)
- Gold evidence: Tài liệu là profile rủi ro, không phải danh sách sản phẩm được chứng nhận năm 2026.
- Final context IDs: ['nist-ai-600-1-p035-para-001-000', 'nist-ai-600-1-p005-para-000-001', 'nist-ai-600-1-p039-para-001-001', 'nist-ai-600-1-p029-para-002-000', 'nist-ai-600-1-p029-para-002-003', 'nist-ai-600-1-p043-para-000-001', 'nist-ai-600-1-p033-para-001-001', 'nist-ai-600-1-p034-para-001-003']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]
