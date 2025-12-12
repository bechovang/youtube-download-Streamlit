import streamlit as st
import os
from downloader import download_media

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="YouTube Downloader Pro",
    page_icon="🚀",
    layout="centered"
)

# CSS Tùy chỉnh cho đẹp hơn
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
    .success-box {
        padding: 15px;
        background-color: #D4EDDA;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GIAO DIỆN CHÍNH
st.title("🚀 YouTube Downloader")
st.write("Công cụ tải video/nhạc YouTube cho Home Server")

# Tạo thư mục lưu trữ tạm trên server nếu chưa có
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# KHUNG NHẬP LIỆU
with st.container():
    url = st.text_input("🔗 Dán link YouTube vào đây:", placeholder="https://www.youtube.com/watch?v=...")
    
    col1, col2 = st.columns(2)
    with col1:
        file_type = st.radio("📂 Chọn định dạng:", ["Nhạc (MP3)", "Video (MP4)"])
        # Chuyển đổi lựa chọn sang từ khóa mà downloader.py hiểu
        media_type = "audio" if "Nhạc" in file_type else "video"
    
    with col2:
        st.write("") # Spacer
        st.write("") 
        st.info("💡 Mẹo: Video sẽ được tải ở chất lượng tốt nhất (1080p).")

# 3. XỬ LÝ KHI BẤM NÚT TẢI
if st.button("⚡ BẮT ĐẦU TẢI XUỐNG"):
    if not url:
        st.warning("⚠️ Vui lòng dán đường link vào trước!")
    else:
        # Hiển thị vòng quay đang xử lý
        with st.spinner(f"Server đang tải {file_type}... Vui lòng đợi..."):
            try:
                # Gọi hàm từ file downloader.py
                success, result = download_media(url, DOWNLOAD_FOLDER, media_type)
                
                if success:
                    # Thành công
                    filename = result
                    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                    
                    st.success("✅ Đã xử lý xong!")
                    
                    # Kiểm tra file có tồn tại không trước khi cho tải
                    if os.path.exists(file_path):
                        # Đọc file để tạo nút tải về
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                            
                        # Xác định loại file (MIME type)
                        mime_type = "audio/mpeg" if media_type == "audio" else "video/mp4"
                        
                        st.markdown(f'<div class="success-box">File: <b>{filename}</b> đã sẵn sàng!</div>', unsafe_allow_html=True)
                        
                        # Nút download về máy tính người dùng
                        st.download_button(
                            label=f"⬇️ NHẤN ĐỂ TẢI FILE VỀ MÁY ({file_type})",
                            data=file_data,
                            file_name=filename,
                            mime=mime_type
                        )
                    else:
                        st.error("❌ Lỗi: Không tìm thấy file trên server sau khi tải.")
                else:
                    # Thất bại (Lỗi từ downloader trả về)
                    st.error(f"❌ Lỗi tải xuống: {result}")
                    
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống: {str(e)}")

# Footer
st.markdown("---")
st.caption("Home Server YouTube Downloader | Powered by Streamlit & yt-dlp")