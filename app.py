import streamlit as st
import os
import shutil
import time
import zipfile
from datetime import datetime
from downloader import download_media

# --- CẤU HÌNH ---
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

st.set_page_config(
    page_title="Tải Nhạc Cho Mẹ Diệp", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH CHO MOBILE ---
st.markdown("""
    <style>
    /* Font chữ dễ đọc */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Nút bấm to, bo tròn để dễ bấm trên điện thoại */
    .stButton>button {
        height: 3.5rem;
        font-weight: bold;
        border-radius: 12px;
        transition: all 0.3s;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Hiệu ứng khi bấm */
    .stButton>button:active {
        transform: scale(0.98);
    }

    /* Ẩn menu rườm rà của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tùy chỉnh card trạng thái */
    div[data-testid="stStatusWidget"] {
        border-radius: 10px;
        border: 1px solid #eee;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM HỖ TRỢ ---

def create_zip_archive():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"Tong_Hop_Nhac_{timestamp}.zip"
    zip_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
            for file in files:
                if file != zip_filename:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.basename(file_path))
    return zip_path, zip_filename

def get_file_size(path):
    try:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        return f"{size_mb:.1f}MB"
    except:
        return ""

# --- GIAO DIỆN CHÍNH ---

st.title("🎵 Tải Nhạc/Video Youtube")

# Dòng chữ tặng mẹ Diệp nằm ngay dưới tiêu đề, màu hồng đậm
st.markdown("Server tốc độ cao tại nhà • <span style='color:#e91e63; font-weight:bold'>Web giúp mẹ Diệp dễ down nhạc</span>", unsafe_allow_html=True)

st.write("---") # Đường kẻ ngang phân cách

# Tạo 2 Tab
tab1, tab2 = st.tabs(["📥 TẢI VỀ", "📂 KHO NHẠC ĐÃ TẢI"])

# ==========================================
# TAB 1: TẢI HÀNG LOẠT
# ==========================================
with tab1:
    with st.container():
        st.write("👇 **Dán link Youtube vào đây (mỗi dòng 1 link):**")
        raw_urls = st.text_area("", height=150, placeholder="Ví dụ:\nhttps://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=...", label_visibility="collapsed")
    
    st.write("") # Khoảng trống
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        st.write("**Chọn loại:**")
        file_type = st.radio("Loại:", ["Lấy Nhạc (MP3)", "Lấy Hình (MP4)"], label_visibility="collapsed")
        media_type = "audio" if "Nhạc" in file_type else "video"
    
    with col_opt2:
        st.write("**Thao tác:**")
        # Nút to màu hồng/đỏ
        start_btn = st.button("🚀 BẮT ĐẦU TẢI NGAY", type="primary", use_container_width=True)

    # Nút dừng khẩn cấp
    with st.expander("⚠️ Nút dừng khẩn cấp"):
        if st.button("🛑 DỪNG LẠI TẤT CẢ", type="secondary", use_container_width=True):
            st.session_state.stop_processing = True
            st.error("Đã gửi lệnh dừng!")

    # XỬ LÝ LOGIC
    if start_btn and raw_urls:
        st.session_state.stop_processing = False
        url_list = [line.strip() for line in raw_urls.split('\n') if line.strip()]
        total = len(url_list)
        
        if total == 0:
            st.warning("⚠️ Chưa nhập link nào cả!")
        else:
            st.toast(f"Đang xử lý {total} bài...", icon="⏳")
            progress_bar = st.progress(0)
            success_count = 0
            
            for i, url in enumerate(url_list):
                if st.session_state.get('stop_processing', False):
                    break
                
                # Card trạng thái
                with st.status(f"🔄 Bài {i+1}/{total}: Đang tải...", expanded=True) as status:
                    st.caption(f"Link: {url}")
                    try:
                        success, result = download_media(url, DOWNLOAD_FOLDER, media_type)
                        if success:
                            status.update(label=f"✅ Bài {i+1}: Thành công!", state="complete", expanded=False)
                            success_count += 1
                        else:
                            status.update(label=f"❌ Bài {i+1}: Lỗi", state="error", expanded=False)
                            st.error(result)
                    except Exception as e:
                        status.update(label="❌ Lỗi hệ thống", state="error")
                
                progress_bar.progress((i + 1) / total)
                if i < total - 1: time.sleep(1.5)

            if success_count > 0:
                st.balloons()
                st.success(f"🎉 Đã tải xong {success_count} bài!")
                st.info("👉 Mẹ bấm sang tab **'KHO NHẠC ĐÃ TẢI'** để lấy nhạc về máy nhé!")

# ==========================================
# TAB 2: KHO DỮ LIỆU
# ==========================================
with tab2:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Danh sách bài đã tải")
    with c2:
        if st.button("🔄 Cập nhật", use_container_width=True):
            st.rerun()

    try:
        files = sorted(os.listdir(DOWNLOAD_FOLDER), key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
        files = [f for f in files if not f.startswith('.')]
    except:
        files = []

    if not files:
        st.info("Chưa có bài nào. Mẹ quay lại tab 'Tải Về' để tải nhé!")
    else:
        # Nút tải tất cả
        if st.button("📦 TẢI HẾT VỀ MỘT LÚC (ZIP)", type="primary", use_container_width=True):
            with st.spinner("Đang nén file..."):
                zip_path, zip_name = create_zip_archive()
                with open(zip_path, "rb") as f:
                    st.download_button("⬇️ LƯU FILE ZIP VỀ MÁY", f, file_name=zip_name, mime="application/zip", use_container_width=True)
        
        st.write("---")

        # Danh sách file (Layout mobile)
        for file in files:
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            
            with st.container():
                # Dòng 1: Tên file
                icon = "🎵" if file.endswith(".mp3") else "🎬"
                if file.endswith(".zip"): icon = "📦"
                
                st.markdown(f"**{icon} {file}**")
                
                # Dòng 2: Nút bấm
                c_size, c_dl, c_del = st.columns([1.5, 2, 1.5])
                
                with c_size:
                    st.caption(get_file_size(file_path))
                
                with c_dl:
                    try:
                        with open(file_path, "rb") as f:
                            st.download_button("⬇️ Tải", f, file_name=file, key=f"dl_{file}", use_container_width=True)
                    except:
                        st.error("Lỗi")
                
                with c_del:
                    if st.button("Xóa", key=f"del_{file}", use_container_width=True):
                        try:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                st.toast("Đã xóa!", icon="🗑️")
                                time.sleep(0.5)
                                st.rerun()
                        except:
                            pass
                
                st.divider()