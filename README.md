# YouTube Downloader - Streamlit App

A web-based YouTube video and audio downloader built with Streamlit and yt-dlp. This application allows users to download YouTube videos as MP4 files or extract audio as MP3 files through a simple web interface.

## Features

- 🎥 **Video Download**: Download YouTube videos in MP4 format (up to 1080p)
- 🎵 **Audio Extraction**: Extract audio from YouTube videos as MP3 files (192kbps)
- 🍪 **Cookie Support**: Optional cookie file support for age-restricted or region-locked content
- 🚫 **Anti-Block**: Uses Android/iOS client emulation to avoid blocking
- 📱 **Web Interface**: User-friendly Streamlit web interface
- 🔄 **Auto Overwrite**: Automatically overwrites existing files

## Requirements

### Python Packages
- `streamlit` - Web framework
- `yt-dlp` - YouTube downloader library
- `ffmpeg-python` - Audio/video processing

### System Dependencies
- `ffmpeg` - Required for audio/video conversion

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd youtube-download-Streamlit
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Windows:**
- Download from [FFmpeg official website](https://ffmpeg.org/download.html)
- Add to system PATH or use package manager:
  ```bash
  choco install ffmpeg
  # or
  winget install ffmpeg
  ```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 4. (Optional) Setup Cookies
If you need to download age-restricted or region-locked content:
1. Export cookies from your browser using an extension (e.g., "Get cookies.txt LOCALLY")
2. Save the cookies as `cookies.txt` in the project root directory

## Usage

### Start the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Web Interface
1. Enter a YouTube URL in the input field
2. Select download type (Video or Audio)
3. Click the download button
4. Wait for the download to complete
5. The file will be saved in the `downloads/` directory

### Programmatic Usage
```python
from downloader import download_media

# Download audio
success, result = download_media(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="./downloads",
    media_type="audio"
)

# Download video
success, result = download_media(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="./downloads",
    media_type="video"
)
```

## Project Structure

```
youtube-download-Streamlit/
├── app.py              # Streamlit web application
├── downloader.py        # Core download functionality
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies
├── cookies.txt         # (Optional) Browser cookies file
└── downloads/          # Downloaded files directory
```

## Configuration

### Download Path
By default, files are saved to `./downloads/`. You can modify this in the application code.

### Audio Quality
Default audio quality is 192kbps. To change this, modify the `preferredquality` parameter in `downloader.py`:
```python
'preferredquality': '192',  # Change to '128', '256', '320', etc.
```

### Video Quality
Default maximum video quality is 1080p. To change this, modify the format string in `downloader.py`:
```python
'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
```

## Troubleshooting

### Common Issues

**Error: FFmpeg not found**
- Ensure FFmpeg is installed and added to system PATH
- Restart terminal/IDE after installation

**Error: Video unavailable**
- Video may be private, deleted, or region-locked
- Try using cookies.txt for age-restricted content

**Error: Sign in required**
- Add `cookies.txt` file to project root
- Export cookies from your browser while logged into YouTube

**Download fails silently**
- Check internet connection
- Verify YouTube URL is correct
- Check available disk space

## License

This project is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws when using this tool.

## Disclaimer

This tool is provided as-is. Users are responsible for ensuring their use complies with YouTube's Terms of Service and applicable copyright laws.

---

# YouTube Downloader - Streamlit App (Tiếng Việt)

Ứng dụng web tải video và audio từ YouTube được xây dựng bằng Streamlit và yt-dlp. Ứng dụng này cho phép người dùng tải video YouTube dưới dạng file MP4 hoặc trích xuất audio dưới dạng file MP3 thông qua giao diện web đơn giản.

## Tính năng

- 🎥 **Tải Video**: Tải video YouTube định dạng MP4 (tối đa 1080p)
- 🎵 **Trích xuất Audio**: Trích xuất audio từ video YouTube dưới dạng file MP3 (192kbps)
- 🍪 **Hỗ trợ Cookies**: Tùy chọn sử dụng file cookies cho nội dung giới hạn độ tuổi hoặc khóa vùng
- 🚫 **Chống chặn**: Sử dụng kỹ thuật giả lập client Android/iOS để tránh bị chặn
- 📱 **Giao diện Web**: Giao diện web thân thiện với Streamlit
- 🔄 **Ghi đè tự động**: Tự động ghi đè file đã tồn tại

## Yêu cầu

### Gói Python
- `streamlit` - Framework web
- `yt-dlp` - Thư viện tải YouTube
- `ffmpeg-python` - Xử lý audio/video

### Phụ thuộc hệ thống
- `ffmpeg` - Cần thiết cho việc chuyển đổi audio/video

## Cài đặt

### 1. Clone Repository
```bash
git clone <repository-url>
cd youtube-download-Streamlit
```

### 2. Cài đặt phụ thuộc Python
```bash
pip install -r requirements.txt
```

### 3. Cài đặt FFmpeg

**Windows:**
- Tải từ [trang web chính thức FFmpeg](https://ffmpeg.org/download.html)
- Thêm vào PATH hệ thống hoặc sử dụng package manager:
  ```bash
  choco install ffmpeg
  # hoặc
  winget install ffmpeg
  ```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 4. (Tùy chọn) Thiết lập Cookies
Nếu bạn cần tải nội dung giới hạn độ tuổi hoặc khóa vùng:
1. Xuất cookies từ trình duyệt bằng extension (ví dụ: "Get cookies.txt LOCALLY")
2. Lưu cookies dưới dạng `cookies.txt` trong thư mục gốc của dự án

## Sử dụng

### Khởi động ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở trong trình duyệt mặc định tại `http://localhost:8501`

### Sử dụng giao diện web
1. Nhập URL YouTube vào ô nhập liệu
2. Chọn loại tải xuống (Video hoặc Audio)
3. Nhấn nút tải xuống
4. Chờ quá trình tải hoàn tất
5. File sẽ được lưu trong thư mục `downloads/`

### Sử dụng lập trình
```python
from downloader import download_media

# Tải audio
success, result = download_media(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="./downloads",
    media_type="audio"
)

# Tải video
success, result = download_media(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    output_path="./downloads",
    media_type="video"
)
```

## Cấu trúc dự án

```
youtube-download-Streamlit/
├── app.py              # Ứng dụng web Streamlit
├── downloader.py        # Chức năng tải xuống chính
├── requirements.txt    # Phụ thuộc Python
├── packages.txt        # Phụ thuộc hệ thống
├── cookies.txt         # (Tùy chọn) File cookies trình duyệt
└── downloads/          # Thư mục file đã tải
```

## Cấu hình

### Đường dẫn tải xuống
Mặc định, file được lưu vào `./downloads/`. Bạn có thể thay đổi trong mã ứng dụng.

### Chất lượng Audio
Chất lượng audio mặc định là 192kbps. Để thay đổi, sửa tham số `preferredquality` trong `downloader.py`:
```python
'preferredquality': '192',  # Thay đổi thành '128', '256', '320', v.v.
```

### Chất lượng Video
Chất lượng video tối đa mặc định là 1080p. Để thay đổi, sửa chuỗi format trong `downloader.py`:
```python
'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
```

## Khắc phục sự cố

### Vấn đề thường gặp

**Lỗi: Không tìm thấy FFmpeg**
- Đảm bảo FFmpeg đã được cài đặt và thêm vào PATH hệ thống
- Khởi động lại terminal/IDE sau khi cài đặt

**Lỗi: Video không khả dụng**
- Video có thể là riêng tư, đã bị xóa hoặc khóa vùng
- Thử sử dụng cookies.txt cho nội dung giới hạn độ tuổi

**Lỗi: Yêu cầu đăng nhập**
- Thêm file `cookies.txt` vào thư mục gốc dự án
- Xuất cookies từ trình duyệt khi đã đăng nhập YouTube

**Tải xuống thất bại im lặng**
- Kiểm tra kết nối internet
- Xác minh URL YouTube đúng
- Kiểm tra dung lượng đĩa còn trống

## Giấy phép

Dự án này chỉ dành cho mục đích giáo dục. Vui lòng tuân thủ Điều khoản Dịch vụ của YouTube và luật bản quyền khi sử dụng công cụ này.

## Tuyên bố từ chối trách nhiệm

Công cụ này được cung cấp như hiện tại. Người dùng chịu trách nhiệm đảm bảo việc sử dụng tuân thủ Điều khoản Dịch vụ của YouTube và luật bản quyền hiện hành.

