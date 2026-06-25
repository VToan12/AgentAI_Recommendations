import streamlit as st
import pandas as pd
import plotly.express as px

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="AI Agent IT Insights", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS để làm nổi bật các khối Khuyến nghị
st.markdown("""
<style>
    .insight-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4a90e2;}
    .recommendation-box { background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32;}
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .insight-box { background-color: #1e1e1e; border-left: 5px solid #90caf9; color: #fff;}
        .recommendation-box { background-color: #123314; border-left: 5px solid #81c784; color: #fff;}
    }
</style>
""", unsafe_allow_html=True)

st.title("Chiến lược ứng dụng AI Agent trong lĩnh vực CNTT/KHMT")
st.markdown("Báo cáo phân tích chuyên sâu dựa trên dữ liệu đánh giá từ chuyên gia và mong muốn của kỹ sư phần mềm/dữ liệu.")

# --- HÀM TẢI VÀ XỬ LÝ DỮ LIỆU ---
@st.cache_data
def load_data():
    try:
        df_tasks = pd.read_csv(r"D:\coding-viz\AgentAI_Project\data\task_statement_with_metadata.csv")
        df_worker = pd.read_csv(r"D:\coding-viz\AgentAI_Project\data\domain_worker_metadata.csv")
        df_desires = pd.read_csv(r"D:\coding-viz\AgentAI_Project\data\domain_worker_desires.csv")
        df_expert = pd.read_csv(r"D:\coding-viz\AgentAI_Project\data\expert_rated_technological_capability.csv")
        
        # Danh sách từ khóa lọc nhóm ngành IT
        it_keywords = ['Software', 'Computer', 'Data', 'Network', 'Programmer', 'Web', 'Information', 'Developer', 'Architect']
        pattern = '|'.join(it_keywords)
        
        df_it_tasks = df_tasks[df_tasks['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)]
        
        df_merged = pd.merge(
            df_desires[['Task ID', 'Occupation (O*NET-SOC Title)', 'Task', 'Automation Desire Rating', 'Reasons for Automation Desire - Repetitive', 'Reasons for Automation Desire - Human Error', 'Reasons for Human Agency - Quality Oversight', 'Reasons for Human Agency - Control']],
            df_expert[['Task ID', 'Automation Capacity Rating', 'Human Agency Scale Rating']],
            on='Task ID',
            how='inner'
        )
        
        df_it_merged = df_merged[df_merged['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)].drop_duplicates()
        df_it_worker = df_worker[df_worker['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)]
        
        return df_it_tasks, df_it_merged, df_it_worker
    except FileNotFoundError as e:
        st.error(f"Lỗi: Không tìm thấy file dữ liệu. Chi tiết: {e}")
        return None, None, None

df_it_tasks, df_it_merged, df_it_worker = load_data()

if df_it_tasks is not None:
    
    # CHỈ SỬ DỤNG 2 TABS ĐỂ TẬP TRUNG VÀO LUỒNG PHÂN TÍCH
    tab1, tab2 = st.tabs(["Phân tích Insights & Khuyến nghị chi tiết", "Khám phá Dữ liệu Gốc (Raw Data)"])

    # ==========================================
    # TAB 1: PHÂN TÍCH INSIGHTS VÀ KHUYẾN NGHỊ (GỘP CHUNG)
    # ==========================================
    with tab1:
        st.markdown("---")
        
        # ---------------------------------------------------------
        # CHỦ ĐỀ 1: VÙNG CƠ HỘI VÀNG (SWEET SPOT)
        # ---------------------------------------------------------
        st.header("1. Điểm giao thoa: Máy làm tốt & Người muốn giao việc")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            df_scatter = df_it_merged.groupby('Occupation (O*NET-SOC Title)')[['Automation Desire Rating', 'Automation Capacity Rating']].mean().reset_index()
            avg_cap = df_scatter['Automation Capacity Rating'].mean()
            avg_des = df_scatter['Automation Desire Rating'].mean()
            
            fig1 = px.scatter(
                df_scatter, x="Automation Capacity Rating", y="Automation Desire Rating", 
                color="Occupation (O*NET-SOC Title)", size_max=60,
                labels={"Automation Capacity Rating": "Khả năng của AI (Chuyên gia chấm)", "Automation Desire Rating": "Mong muốn tự động hóa (Kỹ sư chấm)"}
            )
            fig1.add_hline(y=avg_des, line_dash="dash", line_color="gray")
            fig1.add_vline(x=avg_cap, line_dash="dash", line_color="gray")
            # Highlight vùng Sweet Spot
            fig1.add_shape(type="rect", x0=avg_cap, y0=avg_des, x1=5, y1=5, fillcolor="rgba(46, 204, 113, 0.2)", line=dict(width=0))
            fig1.add_annotation(x=4.2, y=4.5, text="VÙNG CƠ HỘI VÀNG", showarrow=False, font=dict(size=14, color="green"))
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            sweet_spot_count = df_scatter[(df_scatter['Automation Capacity Rating'] > avg_cap) & (df_scatter['Automation Desire Rating'] > avg_des)].shape[0]
            total_occupations = df_scatter.shape[0]
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Insight: Kỹ sư CNTT rất cởi mở với tự động hóa, nhưng có chọn lọc.</h4>
                <b>Số liệu chứng minh:</b><br>
                Có <b>{sweet_spot_count}/{total_occupations}</b> nhóm công việc IT rơi vào "Vùng cơ hội vàng" (Góc trên cùng bên phải). Đây là khu vực mà cả năng lực của AI (Capacity) và mong muốn của kỹ sư (Desire) đều vượt mức trung bình.<br><br>
                <b>Diễn giải:</b><br>
                Trong ngành IT, những tác vụ mang tính nền tảng, rõ ràng logic (ví dụ: tạo cấu trúc thư mục, viết unit test cơ bản, rà soát syntax) là những thứ máy móc hiện tại làm rất tốt và kỹ sư cũng cực kỳ muốn "khoán" trắng cho máy để rảnh tay làm việc khó hơn (System Architecture).
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
                <h4>Khuyến nghị cho Ứng dụng AI Agent: Xây dựng "Micro-Agents"</h4>
                <ul>
                    <li><b>Đừng xây dựng một "AI Lập trình viên thay thế con người".</b> Hãy xây dựng các tập hợp <b>Micro-Agents</b> chuyên biệt cho từng tác vụ nhỏ.</li>
                    <li><b>Sản phẩm tiêu biểu:</b> Agent tự động phân tích JIRA ticket và tạo sẵn Boilerplate code; Agent tự động viết Test Coverage; Agent quét và định dạng lại cấu trúc Log hệ thống.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("---")
        
        # ---------------------------------------------------------
        # CHỦ ĐỀ 2: ĐỘNG LỰC VÀ RÀO CẢN
        # ---------------------------------------------------------
        st.header("2. Tại sao Kỹ sư IT muốn dùng (hoặc sợ) AI Agent?")
        
        col3, col4 = st.columns([1, 1.2])
        
        with col3:
            reasons_data = {
                "Yếu tố": ["Giảm Lặp lại (Repetitive)", "Giảm Lỗi (Human Error)", "Cần Kiểm soát (Control)", "Giám sát Chất lượng (Oversight)"],
                "Lượt chọn": [
                    df_it_merged['Reasons for Automation Desire - Repetitive'].sum(),
                    df_it_merged['Reasons for Automation Desire - Human Error'].sum(),
                    df_it_merged['Reasons for Human Agency - Control'].sum(),
                    df_it_merged['Reasons for Human Agency - Quality Oversight'].sum()
                ],
                "Phân loại": ["Động lực (Desire)", "Động lực (Desire)", "Rào cản/Yêu cầu (Agency)", "Rào cản/Yêu cầu (Agency)"]
            }
            df_reasons = pd.DataFrame(reasons_data)
            fig2 = px.bar(
                df_reasons, x="Yếu tố", y="Lượt chọn", color="Phân loại",
                color_discrete_map={"Động lực (Desire)": "#3498db", "Rào cản/Yêu cầu (Agency)": "#e74c3c"}
            )
            st.plotly_chart(fig2, use_container_width=True)
            
        with col4:
            rep_count = df_reasons.iloc[0]['Lượt chọn']
            over_count = df_reasons.iloc[3]['Lượt chọn']
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>Insight: Động lực lớn nhất là tránh sự nhàm chán, nhưng rào cản lớn nhất là Nỗi sợ mất kiểm soát chất lượng.</h4>
                <b>Số liệu chứng minh:</b><br>
                Yếu tố <i>"Tránh công việc lặp lại"</i> đạt mức rất cao ({rep_count} lượt chọn). Tuy nhiên, yêu cầu về <i>"Giám sát chất lượng - Quality Oversight"</i> lại cao tương đương, thậm chí áp đảo ({over_count} lượt chọn).<br><br>
                <b>Diễn giải:</b><br>
                Đặc thù ngành KHMT: Một dòng code sai do AI sinh ra nếu bị đẩy thẳng lên hệ thống (Production) có thể gây sập server hoặc rò rỉ dữ liệu, dẫn đến thiệt hại hàng tỷ đồng. Do đó, kỹ sư <b>không tin tưởng giao toàn quyền (Autopilot)</b> cho AI xử lý end-to-end.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
                <h4>Khuyến nghị cho Ứng dụng AI Agent: Mô hình "Human-in-the-loop" (Bắt buộc)</h4>
                <ul>
                    <li><b>Định vị sản phẩm:</b> Thiết kế AI Agent như một "Co-pilot" (Cơ phó) thay vì "Autopilot" (Lái tự động).</li>
                    <li><b>Thiết kế Workflow:</b> 
                        <ul>
                            <li>AI Agent có quyền: Phân tích, lập kế hoạch, viết code, chạy test cục bộ, và <b>tạo Pull Request (PR)</b>.</li>
                            <li>AI Agent KHÔNG có quyền: Tự động Merge code vào nhánh Master, tự động Deploy lên Server, hoặc xóa bảng Dữ liệu.</li>
                        </ul>
                    </li>
                    <li><b>Giao diện (UI/UX):</b> Ứng dụng phải có màn hình <i>"Pending Approval" (Chờ phê duyệt)</i> hiển thị rõ ràng dạng "Diff" (code thêm/bớt) để kỹ sư con người bấm nút "Approve" (Chấp thuận) cuối cùng.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("---")
        
        # ---------------------------------------------------------
        # CHỦ ĐỀ 3: MỨC ĐỘ TRƯỞNG THÀNH TRONG SỬ DỤNG LLM
        # ---------------------------------------------------------
        st.header("3. Hành vi sử dụng LLM hiện tại trong công việc thực tế")
        
        col5, col6 = st.columns([1.2, 1])
        
        with col5:
            llm_usage_cols = [col for col in df_it_worker.columns if 'LLM Usage by Type' in col]
            usage_summary = []
            for col in llm_usage_cols:
                daily_users = df_it_worker[df_it_worker[col] == 'Daily'].shape[0]
                weekly_users = df_it_worker[df_it_worker[col] == 'Weekly'].shape[0]
                task_name = col.split('-')[-1].strip()
                usage_summary.append({
                    "Loại tác vụ": task_name, 
                    "Daily": daily_users, 
                    "Weekly": weekly_users,
                    "Total Active": daily_users + weekly_users
                })
            
            df_usage = pd.DataFrame(usage_summary).sort_values(by="Total Active", ascending=True)
            fig3 = px.bar(
                df_usage, y="Loại tác vụ", x=["Daily", "Weekly"], 
                orientation='h', title="Tần suất sử dụng LLM theo nhóm công việc IT",
                barmode='stack', color_discrete_sequence=['#2ecc71', '#f1c40f']
            )
            st.plotly_chart(fig3, use_container_width=True)
            
        with col6:
            st.markdown(f"""
            <div class="insight-box">
                <h4>Insight: Kỹ sư đang dùng AI như một công cụ truy vấn chiến thuật, chưa phải chiến lược.</h4>
                <b>Số liệu chứng minh:</b><br>
                Mức độ sử dụng "Daily" (Hàng ngày) cao nhất rơi vào các tác vụ mang tính thực thi trực tiếp như <i>Coding</i> và <i>Information Access</i> (Tìm kiếm tài liệu, thư viện). Các tác vụ mang tính vĩ mô như <i>System Design</i> (Thiết kế hệ thống) có mức độ sử dụng thường xuyên thấp hơn hẳn.<br><br>
                <b>Diễn giải:</b><br>
                Kỹ sư đã hình thành thói quen dùng LLM (như ChatGPT, GitHub Copilot) như một sự thay thế cho Google/StackOverflow. Tuy nhiên, họ vẫn chưa tin tưởng khả năng của AI trong việc kiến trúc hệ thống quy mô lớn, do AI thiếu bối cảnh (context) về hạ tầng đặc thù của công ty họ.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="recommendation-box">
                <h4>Khuyến nghị cho Ứng dụng AI Agent: Cấp phát "Ngữ cảnh" (Context-Aware Agents)</h4>
                <ul>
                    <li><b>Vượt ra khỏi Chatbot:</b> Để AI Agent có thể hỗ trợ Thiết kế hệ thống (System Design), Agent phải được cấp quyền truy cập (Read-only) vào kho lưu trữ (Codebase/Repo), tài liệu Confluence, và sơ đồ Cloud AWS/Azure của doanh nghiệp thông qua cơ chế <b>RAG (Retrieval-Augmented Generation)</b>.</li>
                    <li><b>Đề xuất luồng Agent:</b> Xây dựng "Architecture Review Agent" - Kỹ sư upload sơ đồ hệ thống dự kiến, Agent đối chiếu với tài liệu chuẩn (Best Practices) của nội bộ công ty để chỉ ra các lỗ hổng bảo mật hoặc nút thắt cổ chai (bottlenecks) có thể xảy ra.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


    # ==========================================
    # TAB 2: KHÁM PHÁ DỮ LIỆU GỐC
    # ==========================================
    with tab2:
        st.header("Bảng Dữ Liệu Gốc (Đã lọc cho khối ngành IT/CS)")
        st.write("Sử dụng tab này để đối chiếu trực tiếp dữ liệu thô đã dùng cho các phân tích bên trên.")
        
        st.subheader("1. Dữ liệu Đánh giá Tác vụ (Hợp nhất)")
        st.dataframe(df_it_merged)
        
        st.subheader("2. Dữ liệu Thông tin Nhân sự (Worker Metadata)")
        st.dataframe(df_it_worker)