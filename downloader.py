import yt_dlp
import os
import re
import time
import glob

def sanitize_filename(filename):
    """Loại bỏ ký tự không hợp lệ khỏi tên file"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_media(url, output_path, media_type="audio"):
    """
    Tải xuống media từ YouTube (Sử dụng cấu hình Android Client - Đã test OK trên máy bạn)
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_path, exist_ok=True)
        
        # Cấu hình chung
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,              # Giảm log để Web đỡ rối
            'no_warnings': True,
            
            # --- CẤU HÌNH CỦA BẠN (ANDROID) ---
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'retries': 3,
            'fragment_retries': 3,
            # ----------------------------------
        }

        if media_type == "audio":
            # Cấu hình cho audio
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            print("INFO: Cấu hình tải âm thanh.")
            
        else:  # video
            ydl_opts = {
                **common_opts,
                'format': 'best[height<=1080]/best',
                'merge_output_format': 'mp4',
            }
            print("INFO: Cấu hình tải video.")
        
        # Thực hiện tải xuống
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Lấy thông tin video trước
            try:
                info = ydl.extract_info(url, download=False)
                title = sanitize_filename(info.get('title', 'Unknown'))
            except Exception as e:
                return False, f"Lỗi lấy thông tin: {str(e)}"
            
            # Tải xuống
            ydl.download([url])
            
            # --- LOGIC TÌM FILE THÔNG MINH ---
            # Tìm file vừa được tạo trong 5 phút gần đây (Logic của bạn)
            downloaded_files = []
            current_time = time.time()
            
            for filename in os.listdir(output_path):
                if filename.endswith(('.mp3', '.mp4', '.webm', '.m4a')):
                    file_path = os.path.join(output_path, filename)
                    # Lấy file tạo trong 300s gần đây
                    if os.path.getctime(file_path) > (current_time - 300):
                        downloaded_files.append(filename)
            
            if downloaded_files:
                # Lấy file mới nhất
                latest_file = max(downloaded_files, 
                                key=lambda x: os.path.getctime(os.path.join(output_path, x)))
                return True, latest_file
            else:
                return True, f"Đã tải xong (nhưng không tìm thấy tên file, kiểm tra thư mục downloads)"
                
    except Exception as e:
        error_msg = str(e)
        # Xử lý thông báo lỗi thân thiện hơn
        if "HTTP Error 403" in error_msg:
             return False, "Lỗi 403: YouTube chặn. Hãy thử cập nhật: pip install --upgrade yt-dlp"
        if "Sign in" in error_msg:
            return False, "Video yêu cầu đăng nhập (18+)."
        return False, f"Lỗi tải xuống: {error_msg}"