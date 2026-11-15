# Review dev: read the cited chunks before assigning labels

Do not infer citation support from a matching ID alone. Mark each factual claim against the actual chunk text and the full question.

## q01

- Question: Người dùng gặp rủi ro gì khi tin vào thông tin sai mà AI nói rất tự tin?
- Answerable: True
- Status: answered
- Agent answer: Khi tin vào thông tin sai (hay bịa đặt) được hệ thống AI đưa ra một cách rất tự tin, người dùng có nguy cơ hành động theo hoặc quảng bá những thông tin sai lệch đó [nist-ai-600-1-p010-para-001-000]. Trong các ứng dụng thực tế như y tế, điều này có thể dẫn đến việc bác sĩ đưa ra chẩn đoán sai hoặc/và đề xuất các phương pháp điều trị sai (do tóm tắt thông tin bệnh nhân bịa đặt) [nist-ai-600-1-p010-para-001-000].
- Citations: ['nist-ai-600-1-p010-para-001-000']
- Expected answer: Họ có thể tin, làm theo hoặc lan truyền thông tin sai, dẫn tới quyết định sai.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 10, 'evidence': 'Risks from confabulations may arise when users believe false content – often due to the confident nature of the response – leading users to act upon or promote the false information.'}]
- Final context IDs: ['nist-ai-600-1-p010-para-001-000', 'nist-ai-600-1-p015-para-001-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q02

- Question: NIST gọi hiện tượng AI tự tin tạo ra nội dung sai là gì?
- Answerable: True
- Status: answered
- Agent answer: NIST gọi hiện tượng AI tự tin tạo ra nội dung sai là **Confabulation** (sự bịa đặt/tạo thông tin sai lệch một cách tự tin) [nist-ai-600-1-p010-para-000-000].
- Citations: ['nist-ai-600-1-p010-para-000-000']
- Expected answer: Confabulation.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 10, 'evidence': 'refers to a phenomenon in which GAI systems generate and confidently present erroneous or false content in response to prompts.'}]
- Final context IDs: ['nist-ai-600-1-p005-para-004-000', 'nist-ai-600-1-p010-para-000-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q03

- Question: Vì sao chặn các yêu cầu có nội dung nguy hiểm vẫn có thể chưa đủ?
- Answerable: True
- Status: answered
- Agent answer: Chặn các yêu cầu có nội dung nguy hiểm vẫn có thể chưa đủ vì phương pháp này có thể vẫn tạo ra các khuyến nghị có hại khi phản hồi lại những câu lệnh (prompts) mới, ít rõ ràng hơn [nist-ai-600-1-p011-para-001-000]. Hơn nữa, người dùng có thể cố ý tạo ra các câu lệnh như vậy thông qua kỹ thuật "jailbreaking" (thao túng câu lệnh) nhằm lẩn tránh các cơ chế kiểm soát đầu ra [nist-ai-600-1-p011-para-001-000].
- Citations: ['nist-ai-600-1-p011-para-001-000']
- Expected answer: AI vẫn có thể đưa ra gợi ý có hại khi gặp yêu cầu mới hoặc diễn đạt ít rõ ràng hơn.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 11, 'evidence': 'Many current systems restrict model outputs to limit certain content or in response to certain prompts, but this approach may still produce harmful recommendations in response to other less-explicit, novel prompts (also relevant to CBRN Information or Capabilities, Data Privacy, Information Security, and Obscene, Degrading and/or Abusive Content).'}]
- Final context IDs: ['nist-ai-600-1-p011-para-001-000', 'nist-ai-600-1-p040-para-000-004']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q04

- Question: Những hoạt động nào của AI tạo sinh có thể gây tác động lớn tới năng lượng và môi trường?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Huấn luyện, duy trì và vận hành mô hình.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 12, 'evidence': 'Training, maintaining, and operating (running inference on) GAI systems are resource-intensive activities, with potentially large energy and environmental footprints.'}]
- Final context IDs: ['nist-ai-600-1-p041-para-001-003', 'nist-ai-600-1-p012-para-001-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q05

- Question: Theo NIST, lạm dụng dữ liệu tổng hợp khi huấn luyện có thể gây ra hiện tượng gì?
- Answerable: True
- Status: answered
- Agent answer: Theo NIST, việc lạm dụng dữ liệu tổng hợp (synthetic data) trong quá trình huấn luyện có thể gây ra hiện tượng **"sụp đổ mô hình" (model collapse)** [nist-ai-600-1-p013-para-001-000]. Hiện tượng này xảy ra khi việc huấn luyện mô hình quá phụ thuộc vào dữ liệu tổng hợp, dẫn đến việc các điểm dữ liệu biến mất khỏi phân phối đầu ra của mô hình mới, đồng thời đe dọa đến độ bền vững tổng thể của mô hình và tạo ra các đầu ra đồng nhất hơn (homogenized outputs) [nist-ai-600-1-p013-para-001-000].
- Citations: ['nist-ai-600-1-p013-para-001-000']
- Expected answer: Model collapse: một số điểm dữ liệu biến mất khỏi phân bố đầu ra của mô hình mới.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 13, 'evidence': 'Model collapse can occur when model training over-relies on synthetic data, resulting in data points disappearing from the distribution of the new model’s outputs.'}]
- Final context IDs: ['nist-ai-600-1-p013-para-001-000', 'nist-ai-600-1-p026-para-000-004']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q06

- Question: Trong tấn công prompt injection trực tiếp, kẻ tấn công đưa nội dung độc hại vào AI bằng cách nào?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Họ tự tạo và nhập yêu cầu độc hại trực tiếp vào hệ thống AI.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 15, 'evidence': 'In direct prompt injections, attackers might craft malicious prompts and input them directly to a GAI system, with a variety of downstream negative consequences to interconnected systems.'}]
- Final context IDs: ['nist-ai-600-1-p015-para-000-001', 'nist-ai-600-1-p035-para-002-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q07

- Question: Prompt injection gián tiếp đưa chỉ dẫn độc hại tới ứng dụng AI bằng đường nào?
- Answerable: True
- Status: answered
- Agent answer: Theo tài liệu, các cuộc tấn công prompt injection gián tiếp xảy ra khi kẻ tấn công khai thác các ứng dụng tích hợp LLM từ xa (tức là không có giao diện trực tiếp) bằng cách **tiêm các prompt (chỉ dẫn) vào dữ liệu có khả năng được truy xuất** [nist-ai-600-1-p015-para-000-001].
- Citations: ['nist-ai-600-1-p015-para-000-001']
- Expected answer: Kẻ tấn công chèn chỉ dẫn vào dữ liệu mà ứng dụng có thể truy xuất, không cần giao diện trực tiếp.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 15, 'evidence': 'Indirect prompt injection attacks occur when adversaries remotely (i.e., without a direct interface) exploit LLM-integrated applications by injecting prompts into data likely to be retrieved.'}]
- Final context IDs: ['nist-ai-600-1-p015-para-000-001', 'nist-ai-600-1-p005-para-000-000', 'nist-ai-600-1-p019-para-000-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q08

- Question: Vì sao các thành phần AI lấy từ bên thứ ba có thể làm giảm trách nhiệm giải trình?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Chúng có thể được lấy không đúng cách hoặc chưa được thẩm định kỹ.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 16, 'evidence': 'These components might be improperly obtained or not properly vetted, leading to diminished transparency or accountability for downstream users.'}]
- Final context IDs: ['nist-ai-600-1-p009-para-002-001', 'nist-ai-600-1-p045-para-000-005']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q09

- Question: NIST nêu những kiểu tác động nào thuộc rủi ro riêng tư dữ liệu?
- Answerable: True
- Status: answered
- Agent answer: Theo tài liệu NIST AI 600-1, các kiểu tác động (impacts) thuộc rủi ro riêng tư dữ liệu (data privacy) bao gồm:
* Rò rỉ (leakage) [nist-ai-600-1-p008-para-000-002].
* Sử dụng trái phép (unauthorized use) [nist-ai-600-1-p008-para-000-002].
* Tiết lộ (disclosure) [nist-ai-600-1-p008-para-000-002].
* Khôi phục danh tính/giải ẩn danh (de-anonymization) đối với thông tin sinh biền, sức khỏe, vị trí, hoặc thông tin nhận dạng cá nhân khác (PII) hoặc dữ liệu nhạy cảm [nist-ai-600-1-p008-para-000-002].
- Citations: ['nist-ai-600-1-p008-para-000-002']
- Expected answer: Rò rỉ, dùng hoặc tiết lộ trái phép, hoặc tái nhận dạng dữ liệu cá nhân và dữ liệu nhạy cảm.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 8, 'evidence': 'Data Privacy: Impacts due to leakage and unauthorized use, disclosure, or de-anonymization of biometric, health, location, or other personally identifiable information or sensitive data.'}]
- Final context IDs: ['nist-ai-600-1-p008-para-000-002', 'nist-ai-600-1-p007-para-002-002']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q10

- Question: NIST gợi ý tổ chức ghi lại điều gì để tăng minh bạch nội dung AI?
- Answerable: True
- Status: answered
- Agent answer: Dựa trên tài liệu, NIST gợi ý các tổ chức ghi lại các nội dung sau để tăng cường minh bạch và nguồn gốc của nội dung (content provenance):

* Ghi lại mỗi trường hợp nội dung được tạo ra, chỉnh sửa hoặc chia sẻ bằng các giải pháp minh bạch nội dung kỹ thuật số để tạo ra lịch sử chống giả mạo, thúc đẩy tính minh bạch và cho phép truy xuất nguồn gốc [nist-ai-600-1-p038-para-001-003].
* Duy trì hồ sơ về các thay đổi đối với nội dung do bên thứ ba thực hiện, bao gồm các nguồn (sources), dấu thời gian (timestamps) và siêu dữ liệu (metadata) [nist-ai-600-1-p025-para-000-004].
- Citations: ['nist-ai-600-1-p038-para-001-003', 'nist-ai-600-1-p025-para-000-004']
- Expected answer: Nguồn gốc và lịch sử của dữ liệu huấn luyện cũng như dữ liệu được AI tạo ra.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 18, 'evidence': 'GV-1.2-001 Establish transparency policies and processes for documenting the origin and history of training data and generated data for GAI applications to advance digital content transparency, while balancing the proprietary nature of training approaches.'}]
- Final context IDs: ['nist-ai-600-1-p038-para-001-003', 'nist-ai-600-1-p025-para-000-004']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q11

- Question: NIST gợi ý tổ chức xác định trách nhiệm gì khi theo dõi hệ thống AI định kỳ?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Trách nhiệm rà soát nguồn gốc nội dung và giám sát sự cố theo định kỳ.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 20, 'evidence': 'GV-1.5-001 Define organizational responsibilities for periodic review of content provenance and incident monitoring for GAI systems.'}]
- Final context IDs: ['nist-ai-600-1-p023-para-000-001', 'nist-ai-600-1-p045-para-002-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q12

- Question: Trong phần MAP, NIST gợi ý phối hợp với ai khi xác định bối cảnh sử dụng AI có thể chấp nhận?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Các chuyên gia về văn hóa xã hội và các lĩnh vực liên quan.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 27, 'evidence': 'MP-1.1-002 Determine and document the expected and acceptable GAI system context of use in collaboration with socio-cultural and other domain experts'}]
- Final context IDs: ['nist-ai-600-1-p028-para-001-000', 'nist-ai-600-1-p027-para-001-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q13

- Question: Trong phần MEASURE, NIST gợi ý theo dõi tác động của AI liên tục để kiểm tra điều gì giữa các nhóm người?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Kiểm tra đầu ra AI có công bằng giữa các nhóm dân cư khác nhau hay không.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 33, 'evidence': 'MS-1.1-006 Implement continuous monitoring of GAI system impacts to identify whether GAI outputs are equitable across various sub-populations.'}]
- Final context IDs: ['nist-ai-600-1-p040-para-000-002']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q14

- Question: Trong phần MANAGE, tổ chức có những cách nào để ứng phó với rủi ro AI?
- Answerable: True
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: Giảm thiểu, chuyển giao, tránh hoặc chấp nhận rủi ro.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 44, 'evidence': 'Risk response options can include mitigating, transferring, avoiding, or accepting.'}]
- Final context IDs: ['nist-ai-600-1-p044-para-000-001', 'nist-ai-600-1-p045-para-001-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## q15

- Question: NIST gợi ý chính sách lưu trữ hồ sơ nhằm giữ lại lịch sử của hoạt động nào?
- Answerable: True
- Status: answered
- Agent answer: Theo NIST, chính sách lưu trữ hồ sơ nhằm giữ lại lịch sử của các hoạt động kiểm tra, đánh giá, phê duyệt và xác thực (TEVV - test, evaluation, validation, and verification) và các phương pháp minh bạch nội dung kỹ thuật số đối với GAI (trí tuệ nhân tạo tạo sinh) [nist-ai-600-1-p020-para-000-003].
- Citations: ['nist-ai-600-1-p020-para-000-003']
- Expected answer: Lịch sử kiểm thử, đánh giá, xác nhận, kiểm chứng và phương pháp minh bạch nội dung số.
- Gold evidence: [{'source_id': 'nist-ai-600-1', 'page': 20, 'evidence': 'GV-1.5-003 Maintain a document retention policy to keep history for test, evaluation, validation, and verification (TEVV), and digital content transparency methods for GAI.'}]
- Final context IDs: ['nist-ai-600-1-p020-para-000-003', 'nist-ai-600-1-p005-para-004-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-d16

- Question: NIST AI 600-1 nêu tên bệnh viện nào ở Việt Nam đã triển khai kiểm soát confabulation?
- Answerable: False
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: (abstain)
- Gold evidence: Tài liệu là hồ sơ quản lý rủi ro, không phải danh sách triển khai tại bệnh viện Việt Nam.
- Final context IDs: ['nist-ai-600-1-p046-para-000-000', 'nist-ai-600-1-p045-para-000-000', 'nist-ai-600-1-p048-para-000-000', 'nist-ai-600-1-p008-para-000-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]

## d7-d17

- Question: Theo NIST AI 600-1, lệ phí bắt buộc bằng USD để được chứng nhận tuân thủ là bao nhiêu?
- Answerable: False
- Status: abstain
- Agent answer: Không đủ bằng chứng để trả lời.
- Citations: []
- Expected answer: (abstain)
- Gold evidence: Tài liệu không quy định chương trình chứng nhận hay bảng lệ phí tuân thủ.
- Final context IDs: ['nist-ai-600-1-p037-para-000-005', 'nist-ai-600-1-p044-para-002-000']
- Reviewer notes: [fill]
- Citation support per citation: [fill true/false after reading]
- Answer grade 0/1/2 or abstention correctness: [fill]
