import yt_dlp
import os
import re
import time
import glob

def sanitize_filename(filename):
    """
    Làm sạch tên file để an toàn cho hệ thống file và URL
    """
    # Thay thế các ký tự không an toàn bằng gạch dưới
    s = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Loại bỏ khoảng trắng thừa
    s = s.strip()
    return s

def get_cookies_path():
    """
    Tìm file cookies.txt trong thư mục gốc.
    Cần thiết để tải các video giới hạn độ tuổi hoặc tránh bị YouTube chặn IP Server.
    """
    cookie_file = "cookies.txt"
    if os.path.exists(cookie_file):
        print(f"INFO: Đã tìm thấy file cookies: {cookie_file}")
        return cookie_file
    return None

def download_media(url, output_path, media_type="audio"):
    """
    Hàm tải xuống media tối ưu cho Web Server.
    
    Returns:
        tuple: (success: bool, result: str)
               - Nếu success=True, result là tên file đã tải.
               - Nếu success=False, result là thông báo lỗi.
    """
    try:
        # Tạo thư mục đầu ra nếu chưa có
        os.makedirs(output_path, exist_ok=True)
        
        # Cấu hình chung cho yt-dlp
        cookie_path = get_cookies_path()
        
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'restrictfilenames': True, # Đảm bảo tên file không chứa ký tự lạ (ASCII only)
            'overwrites': True,        # Ghi đè nếu file đã tồn tại
            'cookiefile': cookie_path, # Load cookies nếu có
            'quiet': True,             # Giảm bớt log rác
            'no_warnings': True,
            # Giả lập trình duyệt để tránh bị chặn
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        }

        if media_type == "audio":
            # Cấu hình tải MP3
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            # Cấu hình tải Video (MP4)
            # Ưu tiên 1080p MP4, nếu không có thì lấy best video + best audio merge lại
            ydl_opts = {
                **common_opts,
                'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4', # Bắt buộc đầu ra cuối cùng là mp4
            }

        # Bắt đầu tải
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Lấy thông tin trước để check lỗi
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                error_msg = str(e)
                if "Sign in" in error_msg:
                    return False, "YouTube yêu cầu đăng nhập (Cookies). Server chưa cấu hình cookies."
                if "Video unavailable" i