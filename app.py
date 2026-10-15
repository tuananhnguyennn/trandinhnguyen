import pandas as pd
import streamlit as st

# --- 1. Tiêu đề ứng dụng ---
st.title("QUẢN LÝ ĐIỂM THI KHỐI A")
st.markdown("---")

# --- 2. Dữ liệu mẫu (10 học sinh) ---
# Quy tắc tính điểm trung bình: (Toán + Lý + Hóa) / 3
data = {
    "Họ tên": [
        "Lê Trần Nam Anh", "Phạm Hoàng Sơn", "Nguyễn Thu Thủy", "Trần Bá Đạt",
        "Vũ Minh Tuấn", "Đỗ Kim Phượng", "Hoàng Anh Kiệt", "Bùi Ngọc Hân",
        "Ngô Thanh Trúc", "Lý Quốc Bảo"
    ],
    "Toán": [8.5, 9.0, 7.0, 6.5, 9.5, 8.0, 5.0, 4.5, 7.5, 8.5],
    "Lý": [7.5, 8.5, 6.5, 7.0, 9.0, 8.5, 5.5, 5.0, 8.0, 7.5],
    "Hóa": [8.0, 8.0, 7.5, 6.0, 9.5, 7.5, 6.0, 4.0, 7.0, 8.0]
}

df = pd.DataFrame(data)

# Tính điểm Trung bình
df["Điểm trung bình"] = (
    (df["Toán"] + df["Lý"] + df["Hóa"]) / 3
).round(2)

# Xếp loại dựa trên điểm trung bình
def xep_loai(diem):
    if diem >= 8.0:
        return "Giỏi"
    elif diem >= 6.5:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Điểm trung bình"].apply(xep_loai)

# --- 3. Hiển thị bảng điểm ---
st.subheader("📋 Bảng điểm thi thử khối A")
st.dataframe(df, use_container_width=True)

# --- 4. Các thống kê tổng quan ---
st.markdown("---")
st.subheader("📊 Thống kê chung của lớp")

col1, col2, col3 = st.columns(3)

# Điểm trung bình của lớp
dtb_lop = df["Điểm trung bình"].mean().round(2)
col1.metric("Điểm TB cả lớp", dtb_lop)

# Số học sinh Khá/Giỏi (Điểm TB >= 6.5)
so_sv_kha_gioi = len(df[df["Điểm trung bình"] >= 6.5])
col2.metric("Số HS Khá, Giỏi", f"{so_sv_kha_gioi}/10")

# Học sinh thủ khoa và thấp nhất
sv_max = df.loc[df["Điểm trung bình"].idxmax()]
sv_min = df.loc[df["Điểm trung bình"].idxmin()]

col3.metric(
    "Thủ khoa",
    f"{sv_max['Họ tên']} ({sv_max['Điểm trung bình']})"
)

st.info(
    f"🔻 **Học sinh cần cố gắng thêm:** {sv_min['Họ tên']} ({sv_min['Điểm trung bình']} điểm)"
)

# --- 5. Tra cứu điểm từng học sinh (Selectbox) ---
st.markdown("---")
st.subheader("🔍 Tra cứu thông tin học sinh")

selected_student = st.selectbox(
    "Chọn tên học sinh để xem chi tiết:", df["Họ tên"].tolist()
)

# Lọc dữ liệu học sinh được chọn
student_info = df[df["Họ tên"] == selected_student].iloc[0]

# Hiển thị thông tin
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Toán", student_info["Toán"])
c2.metric("Lý", student_info["Lý"])
c3.metric("Hóa", student_info["Hóa"])
c4.metric("Trung bình", student_info["Điểm trung bình"])
c5.metric("Xếp loại", student_info["Xếp loại"])

# --- 6. Biểu đồ cột điểm trung bình ---
st.markdown("---")
st.subheader("📈 Biểu đồ so sánh điểm trung bình")

# Chuẩn bị dữ liệu vẽ biểu đồ
chart_data = df.set_index("Họ tên")[["Điểm trung bình"]]
st.bar_chart(chart_data)

# --- 7. Thông tin footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Hệ thống quản lý điểm thi - Trường THPT Demo"
    "</div>",
    unsafe_allow_html=True,
)