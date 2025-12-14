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

st.set_page_config(page_title="Home Server Downloader", page_icon="🎬", layout="wide")

# --- HÀM HỖ TRỢ ---

def create_zip_archive():
    """Nén toàn bộ thư mục downloads thành zip"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f"Batch_Download_{timestamp}.zip"
    zip_path = os.path.join(DOWNLOAD_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
            for file in files:
                if file != zip_filename: # Không nén chính nó
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.basename(file_path))
    return zip_path, zip_filename

def get_file_size(path):
    try:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        return f"{size_mb:.2f} MB"
    except:
        return "0 MB"

# --- GIAO DIỆN CHÍNH ---

st.title("🚀 Home Server Downloader V3.2")

# Tạo 2 Tab chính
tab1, tab2 = st.tabs(["📥 TẢI HÀNG LOẠT", "📂 KHO DỮ LIỆU & QUẢN LÝ"])

# ==========================================
# TAB 1: TẢI HÀNG LOẠT (QUEUE SYSTEM)
# ==========================================
with tab1:
    col_input, col_config = st.columns([2, 1])
    
    with col_input:
        raw_urls = st.text_area("📋 Dán danh sách link (Mỗi link 1 dòng):", height=250, placeholder="https://youtube.com/...\nhttps://youtube.com/...")
    
    with col_config:
        st.write("⚙️ **Cấu hình:**")
        file_type = st.radio("Định dạng:", ["Nhạc (MP3)", "Video (MP4)"])
        media_type = "audio" if "Nhạc" in file_type else "video"
        
        st.info("💡 **Mẹo:**\n- Hệ thống sẽ tự động bỏ qua link lỗi.\n- Tải xong sẽ có thông báo góc màn hình.")

    # Nút điều khiển
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        start_btn = st.button("▶️ BẮT ĐẦU CHẠY HÀNG CHỜ", type="primary", use_container_width=True)
    with col_btn2:
        stop_btn = st.button("🛑 HỦY KHẨN CẤP (PANIC)", type="secondary", use_container_width=True)

    if stop_btn:
        st.session_state.stop_processing = True
        st.error("⚠️ Đã nhận lệnh HỦY! Hệ thống sẽ dừng sau khi xử lý xong file hiện tại.")

    # XỬ LÝ LOGIC TẢI
    if start_btn and raw_urls:
        st.session_state.stop_processing = False
        
        # Lọc link sạch
        url_list = [line.strip() for line in raw_urls.split('\n') if line.strip()]
        total_videos = len(url_list)
        
        if total_videos == 0:
            st.warning("Danh sách link trống!")
        else:
            st.toast(f"🚀 Bắt đầu xử lý {total_videos} video...", icon="⏳")
            progress_bar = st.progress(0)
            status_text = st.empty()
            success_count = 0
            fail_count = 0
            
            # Vòng lặp xử lý từng video
            for i, url in enumerate(url_list):
                # Kiểm tra nút Hủy
                if st.session_state.get('stop_processing', False):
                    st.warning("🛑 Đã dừng quy trình theo yêu cầu!")
                    st.toast("Đã dừng khẩn cấp!", icon="🛑")
                    break
                
                # Hiển thị trạng thái (Status Card)
                with st.status(f"🔄 Đang tải ({i+1}/{total_videos}): {url}", expanded=True) as status:
                    st.write("Dang kết nối server...")
                    try:
                        success, result = download_media(url, DOWNLOAD_FOLDER, media_type)
                        
                        if success:
                            st.write("✅ Tải xong!")
                            status.update(label=f"✅ Xong ({i+1}/{total_videos}): {result}", state="complete", expanded=False)
                            success_count += 1
                        else:
                            st.write(f"❌ Lỗi: {result}")
                            status.update(label=f"❌ Lỗi ({i+1}/{total_videos}): {url}", state="error", expanded=False)
                            fail_count += 1
                    except Exception as e:
                        status.update(label=f"❌ Lỗi hệ thống: {url}", state="error")
                        fail_count += 1
                
                # Cập nhật thanh tiến trình tổng
                progress_bar.progress((i + 1) / total_videos)
                
                # Nghỉ ngơi chống chặn (Anti-block delay)
                if i < total_videos - 1:
                    time.sleep(2) 

            # TỔNG KẾT
            final_msg = f"🎉 HOÀN TẤT! Thành công: {success_count} | Lỗi: {fail_count}"
            st.success(final_msg)
            
            st.balloons()
            st.toast(final_msg, icon="✅")
            
            if success_count > 0:
                st.info("👉 Chuyển sang tab 'KHO DỮ LIỆU' để tải file về máy.")

# ==========================================
# TAB 2: KHO DỮ LIỆU (GALLERY)
# ==========================================
with tab2:
    col_head, col_refresh = st.columns([3, 1])
    with col_head:
        st.header("📂 Quản lý File trên Server")
    with col_refresh:
        if st.button("🔄 Làm mới danh sách", use_container_width=True):
            st.rerun()

    try:
        files = sorted(os.listdir(DOWNLOAD_FOLDER), key=lambda x: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, x)), reverse=True)
        files = [f for f in files if not f.startswith('.')]
    except:
        files = []

    if not files:
        st.info("Chưa có file nào trong kho.")
    else:
        col_zip, col_info = st.columns([1, 3])
        with col_zip:
            if st.button("📦 NÉN ZIP TẤT CẢ & TẢI VỀ", type="primary", use_container_width=True):
                with st.spinner("Đang nén file..."):
                    zip_path, zip_name = create_zip_archive()
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="⬇️ TẢI FILE ZIP NGAY",
                            data=f,
                            file_name=zip_name,
                            mime="application/zip",
                            use_container_width=True
                        )
        with col_info:
            st.success(f"📊 Tổng số file: **{len(files)}**")

        st.divider()

        # Hiển thị danh sách file
        for file in files:
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            # Chia cột: Icon | Tên file | Dung lượng | Nút bấm
            col_icon, col_name, col_size, col_action = st.columns([0.5, 4, 1.5, 2.5])
            
            with col_icon:
                if file.endswith(".mp3"):
                    st.write("🎵")
                elif file.endswith(".mp4"):
                    st.write("🎬")
                elif file.endswith(".zip"):
                    st.write("📦")
                else:
                    st.write("📄")
            
            with col_name:
                st.write(file)
            
            with col_size:
                st.caption(get_file_size(file_path))
            
            with col_action:
                c1, c2 = st.columns(2)
                with c1:
                    try:
                        with open(file_path, "rb") as f:
                            # CẬP NHẬT: Thêm chữ "Tải" vào nút
                            st.download_button("⬇️ Tải", f, file_name=file, key=f"dl_{file}", help="Tải về máy tính")
                    except:
                        st.error("Err")
                with c2:
                    # CẬP NHẬT: Thêm chữ "Xóa" vào nút
                    if st.button("🗑️ Xóa", key=f"del_{file}", help="Xóa khỏi Server"):
                        try:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                st.toast(f"Đã xóa: {file}", icon="🗑️")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.warning("File không tồn tại")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
            
            st.markdown("---")