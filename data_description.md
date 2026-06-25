# BÁO CÁO MÔ TẢ CHI TIẾT THUỘC TÍNH BỘ DỮ LIỆU (DATA DICTIONARY)

Bộ dữ liệu này phục vụ nghiên cứu chuyên sâu về mối quan hệ giữa công việc của con người (theo chuẩn O*NET), khả năng tự động hóa của công nghệ/AI, và thái độ/nguyện vọng thực tế của người lao động.

---

## 1.File: `task_statement_with_metadata.csv`
*Bộ dữ liệu lưu trữ danh mục tác vụ cụ thể cho từng ngành nghề dựa trên hệ thống phân loại nghề nghiệp chuẩn O*NET-SOC, kèm các thông tin thị trường lao động.*

| Tên Cột | Định Dạng Dữ Liệu | Ý Nghĩa / Giải Thích Chi Tiết |
| :--- | :---: | :--- |
| `O*NET-SOC Code` | Mã văn bản (String) | Mã định danh nghề nghiệp chuẩn theo Hệ thống Phân loại Nghề nghiệp của Mỹ. |
| `Occupation (O*NET-SOC Title)` | Văn bản (String) | Tên gọi chuẩn tiếng Anh của ngành/nghề nghiệp (*Ví dụ: Air Traffic Controllers*). |
| `Task ID` | Số nguyên (Integer) | **Mã số định danh duy nhất** cho từng tác vụ công việc (Khóa chính liên kết). |
| `Task` | Văn bản (String) | Mô tả chi tiết bằng văn bản về nội dung thực hiện của tác vụ đó. |
| `Task Type` | Phân loại (Category) | Loại tác vụ: `Core` (tác vụ cốt lõi) hoặc `Supplemental` (tác vụ bổ trợ). |
| `Date` | Ngày tháng (Date) | Thời gian hệ thống O*NET cập nhật dữ liệu cho tác vụ này. |
| `Category` | Phân loại (Category) | Phân nhóm danh mục của tác vụ. |
| `Frequency` | Số thực (Float) | Điểm số đánh giá **tần suất** thực hiện tác vụ này trong thực tế. |
| `Importance` | Số thực (Float) | Điểm số đánh giá **mức độ quan trọng** của tác vụ đối với sự thành công của nghề. |
| `Relevance` | Số thực (Float) | Điểm số đánh giá **tính liên quan** hoặc mức độ phổ biến của tác vụ trong ngành. |
| `Occupation Mean Annual Wage` | Số thực (Float) | Mức lương trung bình hằng năm của ngành nghề này (Đơn vị: USD). |
| `Occupation Employment` | Số thực (Float) | Tổng số lượng nhân sự đang hoạt động trong ngành này trên thị trường lao động. |
| `Skill (O*NET Work Activity)` | Danh sách (List) | Nhóm hoạt động công việc hoặc kỹ năng cốt lõi lớn nhất bao hàm tác vụ này. |
| `Skill ID (...)` | Danh sách (List) | Mã định danh của nhóm hoạt động công việc/kỹ năng đó theo chuẩn O*NET. |

---

## 2.File: `expert_rated_technological_capability.csv`
*Chứa điểm số đánh giá chuyên sâu từ các chuyên gia công nghệ/AI đối với từng tác vụ nhằm xác định khả năng tự động hóa của máy móc hiện tại.*

### Cấu trúc thuộc tính dữ liệu:

* **Nhóm định danh và liên kết:**
    * `Task ID`: Mã định danh của tác vụ (Dùng để khớp dữ liệu sang file Task Statement).
    * `Occupation (O*NET-SOC Title)` & `Task`: Tên ngành nghề và mô tả nội dung tác vụ tương ứng.
    * `User ID`: Mã ẩn danh của chuyên gia thực hiện chấm điểm (*Ví dụ: RedTiger, BrownFox*).
    * `Date`: Ngày chuyên gia thực hiện đánh giá.
* **Nhóm điểm số đánh giá chuyên môn (Điểm số từ 1 - 5):**
    * `Automation Capacity Rating`: **Khả năng tự động hóa** của công nghệ hiện tại đối với tác vụ (Điểm càng cao nghĩa là máy móc/AI càng dễ làm thay con người).
    * `Physical Action Requirement`: Mức độ yêu cầu về hành động thể chất, khéo léo tay chân để hoàn thành việc.
    * `Involved Uncertainty`: Mức độ bất định, biến động và rủi ro bất ngờ từ môi trường làm việc.
    * `Domain Expertise Requirement`: Mức độ đòi hỏi kiến thức chuyên môn sâu và năng lực tư duy của chuyên gia.
    * `Interpersonal Communication Requirement`: Mức độ yêu cầu tương tác, giao tiếp phức tạp giữa người với người.
    * `Human Agency Scale Rating`: **Mức độ cần thiết phải giữ lại sự kiểm soát của con người** (Con người có cần thiết phải can thiệp/giám sát hay giao phó hoàn toàn cho AI).

---

## 3.File: `domain_worker_metadata.csv`
*Lưu trữ thông tin nền tảng nhân khẩu học và thái độ, hành vi ứng dụng AI tổng quan của những người lao động tham gia khảo sát.*

###Phân nhóm các khối thông tin:

> ### Khối thông tin nhân khẩu học (Demographics)
> * `User ID`: Mã định danh duy nhất của người lao động (Khóa liên kết sang dữ liệu nguyện vọng).
> * `Occupation (O*NET-SOC Title)`: Ngành nghề thực tế hiện tại của người tham gia.
> * `Gender` / `Race` / `Age`: Giới tính, Sắc tộc, và Độ tuổi của người lao động.
> * `Income`: Khoảng thu nhập hằng năm của họ (*Ví dụ: 30K-60K, 86K-165K...*).
> * `Education` / `Experience`: Trình độ học vấn cao nhất và số năm kinh nghiệm trong nghề.
> * `Zip Code` / `Political Affiliation`: Mã bưu chính nơi ở và xu hướng chính trị (Democrat, Republican...).

> ### Khối thông tin thái độ đối với AI (AI Attitudes)
> * `AI Tedious Work Attitude`: Mức độ đồng ý với nhận định: *"AI giúp giảm bớt việc tẻ nhạt"*.
> * `AI Job Importance Attitude`: Đánh giá tầm quan trọng của AI đối với tương lai công việc của họ.
> * `AI Daily Interest Attitude`: Mức độ hứng thú hằng ngày trong việc tìm hiểu, ứng dụng AI.
> * `AI Suffering Attitude`: Mức độ lo lắng về việc AI sẽ gây ảnh hưởng tiêu cực hoặc cướp mất việc làm.

> ### Khối hành vi ứng dụng LLM (LLM Usage Profiles)
> * `LLM Familiarity`: Mức độ quen thuộc với các mô hình ngôn ngữ lớn (ChatGPT, Claude, Gemini...).
> * `LLM Use in Work`: Tần suất ứng dụng thực tế các công cụ LLM vào công việc hiện tại.
> * `LLM Usage by Type - [Tác vụ]`: Tần suất sử dụng LLM (`Daily`, `Weekly`, `Never`...) chia nhỏ theo từng mục đích công việc cụ thể bao gồm:
>     * `Information Access` (Tra cứu thông tin) | `Edit` (Sửa văn bản) | `Idea Generation` (Lên ý tưởng)
>     * `Communication` (Giao tiếp/Viết mail) | `Analysis` (Phân tích) | `Decision` (Hỗ trợ ra quyết định)
>     * `Coding` (Viết code) | `System Design` (Thiết kế hệ thống) | `Data Processing` (Xử lý dữ liệu).
> * `Recruitment Source`: Nguồn thu thập dữ liệu người tham gia (Nền tảng khảo sát *Prolific*).

---

## 4. File: `domain_worker_desires.csv`
*Bảng khảo sát chi tiết ghi nhận mong muốn chủ quan của người lao động về việc có muốn tự động hóa tác vụ của họ hay không, kèm theo các lý do phân tích.*

| Nhóm Tính Chất | Tên Cột Dữ Liệu | Giải Thích Ý Nghĩa Thuộc Tính |
| :--- | :--- | :--- |
| **Định danh** | `Task ID`, `User ID`, `Task`, `Date` | Các thông tin cơ bản dùng để liên kết đồng bộ dữ liệu. |
| **Tự đánh giá** | `Self-reported Expertise` | Mức độ tự nhận thức năng lực cá nhân (`Novice`, `Average`, `Expert`). |
| **Chỉ số cốt lõi** | `Automation Desire Rating` | **Mức độ mong muốn tác vụ này được tự động hóa** (Thang điểm từ 1-5). |
| | `Time` | Đánh giá lượng thời gian họ phải tiêu tốn cho tác vụ này. |
| | `Core Skill Rating` | Đánh giá xem tác vụ có thuộc kỹ năng chuyên môn cốt lõi của họ không. |
| | `Job Security Rating` | Đánh giá mức độ đe dọa mất việc nếu tác vụ này bị máy móc thay thế hoàn toàn. |
| | `Enjoyment Rating` | Mức độ yêu thích/niềm vui của người lao động khi tự tay làm việc này. |
| **Lý do muốn giao việc**<br>*(Định dạng True/False)* | `Reasons for Automation Desire - Free Time` | Muốn tự động hóa để giải phóng bản thân, có thêm thời gian rảnh. |
| | `... - Repetitive` | Vì tính chất công việc quá lặp đi lặp lại và nhàm chán. |
| | `... - Human Error` | Vì mong muốn hạn chế các sai sót chủ quan do con người gây ra. |
| | `... - Stress` | Vì tác vụ này tạo áp lực tinh thần hoặc gây stress quá lớn. |
| | `... - Difficulty` | Vì công việc này quá khó đối với năng lực hiện tại của họ. |
| | `... - Scale` | Vì khối lượng hoặc quy mô công việc quá lớn, một người khó gánh vác nổi. |
| **Tự chấm điểm việc** | `Physical Action Requirement`<br>`Interpersonal Communication Requirement`<br>`Involved Uncertainty`<br>`Domain Expertise Requirement`<br>`Human Agency Scale Rating` | Người lao động tự chấm điểm các thuộc tính của tác vụ (Thể chất, Giao tiếp, Biến động, Chuyên môn, Quyền kiểm soát).<br>*(Dùng để đối chiếu trực tiếp với điểm số độc lập của Chuyên gia công nghệ)*. |
| **Lý do giữ quyền làm**<br>*(Định dạng True/False)* | `Reasons for Human Agency - Physical` | Cần giữ con người vì việc này yêu cầu thao tác cơ học, chân tay thực tế. |
| | `... - Control` | Người lao động chủ động muốn giữ quyền kiểm soát, tự quyết công việc. |
| | `... - Domain Knowledge` | Cần kiến thức, trải nghiệm thực tế sâu sắc của con người mà AI khó học. |
| | `... - Empathy` | Yêu cầu sự thấu cảm, kết nối tâm lý mật thiết giữa người với người. |
| | `... - Quality Oversight` | Cần con người kiểm tra, giám sát chất lượng và chịu trách nhiệm đầu ra. |
| | `... - Dynamic` | Môi trường biến động đòi hỏi tư duy linh hoạt, tùy biến của con người. |
| | `... - Ethical` | tác vụ liên quan mật thiết đến các quyết định đạo đức hoặc pháp lý. |
| **Ghi chú tự do** | `Other Reason for Automation Desire`<br>`Other Reason for Human Agency` | Ý kiến viết tay tự do điền thêm của người lao động (nếu có). |