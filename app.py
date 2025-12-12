import yt_dlp
import os
import glob

def download_media(url, output_path, media_type="audio"):
    """
    Tải xuống media KHÔNG CẦN COOKIES.
    Sử dụng kỹ thuật giả lập Android Client để tránh bị chặn.
    """
    try:
        # Tạo thư mục đầu ra nếu chưa có
        os.makedirs(output_path, exist_ok=True)
        
        # Cấu hình tối ưu để tránh bị chặn (Anti-block)
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'restrictfilenames': True, # Tên file sạch (không ký tự lạ)
            'overwrites': True,        # Ghi đè file cũ
            'quiet': True,             # Ít log hơn
            'no_warnings': True,
            
            # --- QUAN TRỌNG: KỸ THUẬT GIẢ LẬP ĐIỆN THOẠI ---
            # Giúp server tải được mà không cần đăng nhập
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'], # Giả vờ là App Android/iOS
                    'player_skip': ['webpage', 'configs', 'js'], # Bỏ qua check JS
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            }
            # ------------------------------------------------
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
            # Cấu hình tải Video (MP4) - 1080p
            ydl_opts = {
                **common_opts,
                'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            }

        # Bắt đầu quy trình tải
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Lấy thông tin (để chuẩn bị tên file)
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                return False, f"Không thể lấy thông tin video. Lỗi: {str(e)}"

            # 2. Dự đoán tên file sẽ được tạo ra
            filename_template = ydl.prepare_filename(info)
            
            # 3. Tải xuống thật
            ydl.download([url])

            # 4. Tìm file kết quả
            # (Logic tìm file thông minh để tránh lỗi đổi đuôi .webm -> .mp3)
            base_name = os.path.splitext(os.path.basename(filename_template))[0]
            search_pattern = os.path.join(output_path, f"*{base_name}*")
            files = glob.glob(search_pattern)
            
            if not files:
                return False, "Tải xong nhưng không tìm thấy file."

            # Lấy file mới nhất vừa tải xong
            latest_file = max(files, key=os.path.getctime)
            final_filename = os.path.basename(latest_file)
            
            return True, final_filename

    except Exception as e:
        return False, f"Lỗi hệ thống: {str(e)}"