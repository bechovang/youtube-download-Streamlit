import yt_dlp
import os
import re
import time

def sanitize_filename(filename):
    """Loại bỏ ký tự không hợp lệ khỏi tên file"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_media(url, output_path, media_type="audio"):
    """
    Tải xuống media từ YouTube với xử lý lỗi tốt nhất
    
    Args:
        url (str): YouTube URL
        output_path (str): Đường dẫn lưu file
        media_type (str): "audio" hoặc "video"
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_path, exist_ok=True)
        
        # Lưu danh sách file CŨ trước khi tải
        old_files = set(os.listdir(output_path))
        
        # Cấu hình chung
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            
            # Cấu hình Android Client (đã test OK)
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'retries': 3,
            'fragment_retries': 3,
        }

        if media_type == "audio":
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:  # video
            ydl_opts = {
                **common_opts,
                'format': 'best[height<=1080]/best',
                'merge_output_format': 'mp4',
            }
        
        # Thực hiện tải xuống
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Lấy thông tin video
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get('title', 'Unknown'))
            
            # Tải xuống
            ydl.download([url])
            
            # Tìm file MỚI bằng cách so sánh với danh sách cũ
            time.sleep(1)  # Đợi file system cập nhật
            new_files = set(os.listdir(output_path))
            downloaded = new_files - old_files
            
            # Lọc chỉ file media
            media_files = [f for f in downloaded if f.endswith(('.mp3', '.mp4', '.webm', '.m4a'))]
            
            if media_files:
                return True, media_files[0]
            else:
                # Fallback: Tìm file chứa tên video
                for f in new_files:
                    if title.lower() in f.lower() and f.endswith(('.mp3', '.mp4', '.webm', '.m4a')):
                        return True, f
                
                return True, f"Đã tải xong '{title}' (kiểm tra thư mục Downloads)"
                
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        
        # Xử lý lỗi cụ thể
        if "HTTP Error 403" in error_msg or "Sign in" in error_msg:
            return False, "⚠️ YouTube chặn! Chạy lệnh: pip install --upgrade yt-dlp"
        elif "Private video" in error_msg:
            return False, "❌ Video riêng tư, không thể tải."
        elif "Video unavailable" in error_msg:
            return False, "❌ Video không tồn tại hoặc đã bị xóa."
        else:
            return False, f"❌ Lỗi: {error_msg[:100]}"
            
    except Exception as e:
        return False, f"❌ Lỗi nghiêm trọng: {str(e)[:100]}"