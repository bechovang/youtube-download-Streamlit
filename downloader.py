import yt_dlp
import os
import re
import time  # Đưa lên đầu để không bị lỗi
import glob

def sanitize_filename(filename):
    """Loại bỏ ký tự không hợp lệ khỏi tên file"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_media(url, output_path, media_type="audio"):
    """
    Tải xuống media từ YouTube (Phiên bản Anti-Block + Delay)
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_path, exist_ok=True)
        
        # Cấu hình chung (Common Options)
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            
            # --- CẤU HÌNH DELAY (QUAN TRỌNG ĐỂ TRÁNH 403) ---
            'sleep_interval': 3,       # Nghỉ 3 giây trước khi tải
            'max_sleep_interval': 5,   # Nghỉ tối đa 5 giây
            # -----------------------------------------------

            # Bypass YouTube Block (Giả lập Android)
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs', 'js'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'retries': 10,             # Thử lại 10 lần nếu lỗi
            'fragment_retries': 10,
        }

        if media_type == "audio":
            # Cấu hình cho Audio
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
            
        else:  
            # Cấu hình cho Video (1080p)
            ydl_opts = {
                **common_opts,
                'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            }
            print("INFO: Cấu hình tải video.")
        
        # Thực hiện tải xuống
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Lấy thông tin video trước
            try:
                info = ydl.extract_info(url, download=False)
                title = sanitize_filename(info.get('title', 'Unknown'))
                print(f"🎵 Tiêu đề: {title}")
            except Exception as e:
                print(f"⚠️ Không thể lấy thông tin video: {str(e)}")
            
            # Tải xuống
            ydl.download([url])
            
            # --- LOGIC TÌM FILE (Dựa trên thời gian tạo) ---
            # Tìm các file mp3/mp4 vừa được tạo trong 5 phút gần đây
            downloaded_files = []
            current_time = time.time()
            
            for filename in os.listdir(output_path):
                if filename.endswith(('.mp3', '.mp4', '.webm', '.m4a')):
                    file_path = os.path.join(output_path, filename)
                    # Kiểm tra file vừa tạo trong vòng 300 giây (5 phút)
                    if os.path.getctime(file_path) > (current_time - 300):
                        downloaded_files.append(filename)
            
            if downloaded_files:
                # Lấy file mới nhất trong số các file vừa tìm được
                latest_file = max(downloaded_files, 
                                key=lambda x: os.path.getctime(os.path.join(output_path, x)))
                return True, latest_file
            else:
                return True, f"Đã tải xong (nhưng không tìm thấy tên file, hãy kiểm tra thư mục downloads)"
                
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Lỗi: {error_msg}")
        
        if "HTTP Error 403" in error_msg:
             return False, "Lỗi 403: YouTube chặn IP. Hãy thử cập nhật: pip install --upgrade yt-dlp"
        if "Sign in" in error_msg:
            return False, "Video yêu cầu đăng nhập (18+)."
            
        return False, f"Lỗi tải xuống: {error_msg}"