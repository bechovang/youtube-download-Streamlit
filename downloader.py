import yt_dlp
import os
import glob

def download_media(url, output_path, media_type="audio"):
    """
    Hàm tải xuống tối ưu cho Home Server.
    Đã loại bỏ Cookies, sử dụng giả lập Android để chống chặn.
    """
    try:
        # 1. Tạo thư mục nếu chưa có
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 2. Cấu hình cốt lõi (Anti-Block & Safe Filename)
        common_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'restrictfilenames': True,  # Tên file sạch (không dấu)
            'overwrites': True,         # Ghi đè file cũ
            'quiet': True,              # Giảm log rác
            'no_warnings': True,
            
            # --- CÔNG NGHỆ CHỐNG CHẶN (ANTI-BLOCK) ---
            # Giả lập là App Android để YouTube "thả cửa" cho Server tải
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs', 'js'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            }
        }

        # 3. Cấu hình riêng Audio/Video
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
        else:
            # Video: Ưu tiên MP4 1080p -> Merge Video+Audio -> Output MP4
            ydl_opts = {
                **common_opts,
                'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            }

        # 4. Thực thi tải
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Lấy thông tin trước
            try:
                info = ydl.extract_info(url, download=False)
            except Exception as e:
                return False, f"Lỗi lấy thông tin video: {str(e)}"

            # Tải xuống
            ydl.download([url])
            
            # 5. Tìm file kết quả chính xác
            # Lấy tên file gốc (đã được làm sạch bởi restrictfilenames)
            clean_title = ydl.prepare_filename(info)
            base_name = os.path.splitext(os.path.basename(clean_title))[0]
            
            # Tìm tất cả file chứa tên đó trong thư mục output
            search_pattern = os.path.join(output_path, f"*{base_name}*")
            files = glob.glob(search_pattern)
            
            if not files:
                # Fallback: Tìm file mới nhất trong thư mục
                all_files = glob.glob(os.path.join(output_path, "*"))
                if not all_files:
                    return False, "Tải xong nhưng không tìm thấy file."
                latest_file = max(all_files, key=os.path.getctime)
                return True, os.path.basename(latest_file)

            # Lấy file khớp tên và mới nhất
            latest_file = max(files, key=os.path.getctime)
            final_filename = os.path.basename(latest_file)
            
            return True, final_filename

    except Exception as e:
        return False, f"Lỗi hệ thống: {str(e)}"