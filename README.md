# Chiến lược ứng dụng AI Agent trong lĩnh vực CNTT và KHMT

Đây là dự án phân tích dữ liệu và trực quan hóa bằng Streamlit, nhằm cung cấp góc nhìn chuyên sâu về khả năng ứng dụng AI Agent vào ngành Công nghệ Thông tin (CNTT) và Khoa học Máy tính (KHMT).

## 1. Mục tiêu dự án

Dự án được xây dựng với ba mục tiêu cốt lõi:
* **Đánh giá mức độ sẵn sàng của công nghệ:** Phân tích điểm giao thoa giữa năng lực thực thi của AI (được đánh giá bởi các chuyên gia) và mong muốn tự động hóa của các kỹ sư IT thực tế.
* **Xác định động lực và rào cản:** Tìm hiểu nguyên nhân tại sao nhân sự ngành IT muốn giao việc cho AI (nhằm giảm tải công việc lặp lại) nhưng đồng thời vẫn yêu cầu giữ lại quyền kiểm soát và giám sát chất lượng nghiêm ngặt.
* **Đề xuất chiến lược triển khai thực tiễn:** Từ dữ liệu thu thập được, đưa ra các khuyến nghị thiết kế AI Agent phù hợp cho môi trường doanh nghiệp (ví dụ: xây dựng Micro-Agents, áp dụng mô hình Human-in-the-loop, và sử dụng kỹ thuật RAG để tạo Context-Aware Agents).

## 2. Cấu trúc thư mục

Dự án được tổ chức với cấu trúc tập tin như sau:

```text
agent-ai-recommendations/
│
├── app_ai_agent.py                             # Mã nguồn chính của ứng dụng Streamlit (chứa giao diện và logic phân tích)
├── requirements.txt                            # Danh sách các thư viện Python cần thiết để chạy dự án
├── .gitignore                                  # Khai báo các tập tin/thư mục không cần đẩy lên GitHub (vd: .venv, __pycache__)
├── data_description.md                         # Mô tả ý nghĩa các cột có trong bộ dữ liệu
│
├── task_statement_with_metadata.csv            # Dữ liệu O*NET về danh mục tác vụ theo từng nhóm nghề nghiệp
├── domain_worker_metadata.csv                  # Dữ liệu về hồ sơ kinh nghiệm và tần suất sử dụng LLM của nhân sự IT
├── domain_worker_desires.csv                   # Dữ liệu khảo sát về khao khát tự động hóa và ranh giới kiểm soát của kỹ sư
└── expert_rated_technological_capability.csv   # Dữ liệu chuyên gia đánh giá khả năng thực thi tác vụ của mô hình AI
