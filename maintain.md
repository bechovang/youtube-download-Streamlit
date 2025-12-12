# Maintenance Guide

This document provides guidelines for maintaining and updating the YouTube Downloader Streamlit application.

## Regular Maintenance Tasks

### 1. Update Dependencies

#### Python Packages
Update packages regularly to get bug fixes and security patches:
```bash
pip install --upgrade streamlit yt-dlp ffmpeg-python
pip freeze > requirements.txt
```

#### yt-dlp Updates
yt-dlp is frequently updated to handle YouTube API changes. Update it weekly:
```bash
pip install --upgrade yt-dlp
```

### 2. Monitor for Breaking Changes

- **YouTube API Changes**: YouTube frequently updates their API. Monitor yt-dlp GitHub issues for breaking changes.
- **Streamlit Updates**: Check Streamlit release notes for deprecated features.
- **FFmpeg Updates**: Usually backward compatible, but check release notes.

### 3. Test After Updates

After updating dependencies, test:
- Video download functionality
- Audio extraction functionality
- Error handling
- Cookie-based downloads (if applicable)

## Common Issues and Solutions

### Issue: Downloads Fail After YouTube Update

**Symptoms:**
- All downloads fail with similar errors
- "Video unavailable" errors for valid URLs

**Solution:**
1. Update yt-dlp immediately:
   ```bash
   pip install --upgrade yt-dlp
   ```
2. Check yt-dlp GitHub issues: https://github.com/yt-dlp/yt-dlp/issues
3. If issue persists, wait for yt-dlp update or use cookies.txt

### Issue: FFmpeg Errors

**Symptoms:**
- "FFmpeg not found" errors
- Audio conversion fails

**Solution:**
1. Verify FFmpeg installation:
   ```bash
   ffmpeg -version
   ```
2. Reinstall FFmpeg if needed
3. Check PATH environment variable includes FFmpeg

### Issue: Cookie File Expires

**Symptoms:**
- Age-restricted videos fail to download
- "Sign in required" errors

**Solution:**
1. Re-export cookies from browser
2. Replace `cookies.txt` file
3. Ensure cookies are exported while logged into YouTube

### Issue: Rate Limiting / IP Blocking

**Symptoms:**
- Downloads fail after multiple requests
- Connection timeouts

**Solution:**
1. Implement rate limiting in code
2. Add delays between downloads
3. Use proxy rotation (advanced)
4. Consider using cookies.txt

## Code Maintenance

### Adding New Features

1. **New Download Format**
   - Modify `downloader.py` format options
   - Update Streamlit UI in `app.py`
   - Test with various video types

2. **Quality Selection**
   - Add quality selector to UI
   - Update format string dynamically
   - Validate user input

3. **Playlist Support**
   - Set `noplaylist: False` in options
   - Handle multiple files
   - Update UI for progress tracking

### Code Quality

- Run linters regularly:
  ```bash
  pylint downloader.py app.py
  flake8 downloader.py app.py
  ```
- Follow PEP 8 style guide
- Add docstrings to new functions
- Write unit tests for critical functions

## Performance Optimization

### Current Optimizations
- Uses `quiet: True` to reduce logging overhead
- Restricts filenames to ASCII for compatibility
- Overwrites existing files to save space

### Potential Improvements
1. **Caching**: Cache video metadata to avoid redundant API calls
2. **Parallel Downloads**: Implement threading for multiple downloads
3. **Progress Bars**: Add real-time download progress in UI
4. **Queue System**: Implement download queue for batch processing

## Security Considerations

### File Security
- Validate all user inputs (URLs, paths)
- Sanitize filenames (already implemented)
- Limit file size downloads
- Set download directory permissions

### Cookie Security
- Never commit `cookies.txt` to version control
- Rotate cookies regularly
- Use environment variables for sensitive data

### Network Security
- Validate YouTube URLs before processing
- Implement request timeouts
- Handle SSL certificate errors properly

## Backup and Recovery

### Regular Backups
- Backup `requirements.txt` after dependency updates
- Keep version history of `downloader.py` and `app.py`
- Document configuration changes

### Recovery Procedures
1. **Complete Failure**: Restore from git history
2. **Partial Failure**: Check error logs, update dependencies
3. **Data Loss**: Downloads are not critical, can be re-downloaded

## Monitoring

### Logs to Monitor
- Download success/failure rates
- Error message patterns
- User-reported issues
- yt-dlp update notifications

### Metrics to Track
- Average download time
- Success rate percentage
- Most common error types
- Peak usage times

## Version Control

### Git Workflow
1. Create feature branches for new features
2. Test thoroughly before merging
3. Tag releases with version numbers
4. Keep `main` branch stable

### Commit Messages
Use clear, descriptive commit messages:
```
feat: Add quality selector to UI
fix: Resolve FFmpeg path issue on Windows
docs: Update installation instructions
chore: Update yt-dlp to latest version
```

## Testing Checklist

Before deploying updates:
- [ ] Test video download (various resolutions)
- [ ] Test audio extraction
- [ ] Test error handling (invalid URLs, network errors)
- [ ] Test with cookies.txt (if applicable)
- [ ] Test on different operating systems (if possible)
- [ ] Verify UI responsiveness
- [ ] Check file naming and organization
- [ ] Test with age-restricted content (if applicable)

## Resources

- **yt-dlp Documentation**: https://github.com/yt-dlp/yt-dlp
- **Streamlit Documentation**: https://docs.streamlit.io
- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **Issue Tracking**: Monitor yt-dlp GitHub issues for YouTube API changes

---

# Hướng dẫn Bảo trì (Tiếng Việt)

Tài liệu này cung cấp hướng dẫn để bảo trì và cập nhật ứng dụng YouTube Downloader Streamlit.

## Nhiệm vụ Bảo trì Thường xuyên

### 1. Cập nhật Phụ thuộc

#### Gói Python
Cập nhật gói thường xuyên để nhận bản sửa lỗi và bản vá bảo mật:
```bash
pip install --upgrade streamlit yt-dlp ffmpeg-python
pip freeze > requirements.txt
```

#### Cập nhật yt-dlp
yt-dlp được cập nhật thường xuyên để xử lý các thay đổi API YouTube. Cập nhật hàng tuần:
```bash
pip install --upgrade yt-dlp
```

### 2. Theo dõi Thay đổi Phá vỡ

- **Thay đổi API YouTube**: YouTube thường xuyên cập nhật API. Theo dõi các vấn đề GitHub của yt-dlp để biết các thay đổi phá vỡ.
- **Cập nhật Streamlit**: Kiểm tra ghi chú phát hành Streamlit cho các tính năng đã lỗi thời.
- **Cập nhật FFmpeg**: Thường tương thích ngược, nhưng kiểm tra ghi chú phát hành.

### 3. Kiểm thử Sau Khi Cập nhật

Sau khi cập nhật phụ thuộc, kiểm thử:
- Chức năng tải video
- Chức năng trích xuất audio
- Xử lý lỗi
- Tải xuống dựa trên cookies (nếu áp dụng)

## Vấn đề Thường gặp và Giải pháp

### Vấn đề: Tải xuống Thất bại Sau Khi YouTube Cập nhật

**Triệu chứng:**
- Tất cả tải xuống thất bại với lỗi tương tự
- Lỗi "Video không khả dụng" cho URL hợp lệ

**Giải pháp:**
1. Cập nhật yt-dlp ngay lập tức:
   ```bash
   pip install --upgrade yt-dlp
   ```
2. Kiểm tra các vấn đề GitHub của yt-dlp: https://github.com/yt-dlp/yt-dlp/issues
3. Nếu vấn đề vẫn tồn tại, chờ cập nhật yt-dlp hoặc sử dụng cookies.txt

### Vấn đề: Lỗi FFmpeg

**Triệu chứng:**
- Lỗi "Không tìm thấy FFmpeg"
- Chuyển đổi audio thất bại

**Giải pháp:**
1. Xác minh cài đặt FFmpeg:
   ```bash
   ffmpeg -version
   ```
2. Cài đặt lại FFmpeg nếu cần
3. Kiểm tra biến môi trường PATH có bao gồm FFmpeg

### Vấn đề: File Cookie Hết hạn

**Triệu chứng:**
- Video giới hạn độ tuổi không tải được
- Lỗi "Yêu cầu đăng nhập"

**Giải pháp:**
1. Xuất lại cookies từ trình duyệt
2. Thay thế file `cookies.txt`
3. Đảm bảo cookies được xuất khi đã đăng nhập YouTube

### Vấn đề: Giới hạn Tốc độ / Chặn IP

**Triệu chứng:**
- Tải xuống thất bại sau nhiều yêu cầu
- Hết thời gian kết nối

**Giải pháp:**
1. Triển khai giới hạn tốc độ trong mã
2. Thêm độ trễ giữa các tải xuống
3. Sử dụng xoay proxy (nâng cao)
4. Cân nhắc sử dụng cookies.txt

## Bảo trì Mã

### Thêm Tính năng Mới

1. **Định dạng Tải xuống Mới**
   - Sửa đổi tùy chọn định dạng trong `downloader.py`
   - Cập nhật UI Streamlit trong `app.py`
   - Kiểm thử với nhiều loại video

2. **Lựa chọn Chất lượng**
   - Thêm bộ chọn chất lượng vào UI
   - Cập nhật chuỗi định dạng động
   - Xác thực đầu vào người dùng

3. **Hỗ trợ Playlist**
   - Đặt `noplaylist: False` trong tùy chọn
   - Xử lý nhiều file
   - Cập nhật UI để theo dõi tiến trình

### Chất lượng Mã

- Chạy linter thường xuyên:
  ```bash
  pylint downloader.py app.py
  flake8 downloader.py app.py
  ```
- Tuân theo hướng dẫn phong cách PEP 8
- Thêm docstring cho hàm mới
- Viết unit test cho các hàm quan trọng

## Tối ưu hóa Hiệu suất

### Tối ưu hóa Hiện tại
- Sử dụng `quiet: True` để giảm overhead ghi log
- Giới hạn tên file ở ASCII để tương thích
- Ghi đè file hiện có để tiết kiệm không gian

### Cải thiện Tiềm năng
1. **Bộ nhớ đệm**: Cache metadata video để tránh gọi API dư thừa
2. **Tải xuống Song song**: Triển khai threading cho nhiều tải xuống
3. **Thanh Tiến trình**: Thêm thanh tiến trình tải xuống thời gian thực trong UI
4. **Hệ thống Hàng đợi**: Triển khai hàng đợi tải xuống cho xử lý hàng loạt

## Cân nhắc Bảo mật

### Bảo mật File
- Xác thực tất cả đầu vào người dùng (URL, đường dẫn)
- Làm sạch tên file (đã triển khai)
- Giới hạn kích thước file tải xuống
- Đặt quyền thư mục tải xuống

### Bảo mật Cookie
- Không bao giờ commit `cookies.txt` vào kiểm soát phiên bản
- Xoay cookies thường xuyên
- Sử dụng biến môi trường cho dữ liệu nhạy cảm

### Bảo mật Mạng
- Xác thực URL YouTube trước khi xử lý
- Triển khai timeout yêu cầu
- Xử lý lỗi chứng chỉ SSL đúng cách

## Sao lưu và Khôi phục

### Sao lưu Thường xuyên
- Sao lưu `requirements.txt` sau khi cập nhật phụ thuộc
- Giữ lịch sử phiên bản của `downloader.py` và `app.py`
- Ghi lại các thay đổi cấu hình

### Quy trình Khôi phục
1. **Thất bại Hoàn toàn**: Khôi phục từ lịch sử git
2. **Thất bại Một phần**: Kiểm tra log lỗi, cập nhật phụ thuộc
3. **Mất Dữ liệu**: Tải xuống không quan trọng, có thể tải lại

## Giám sát

### Log cần Theo dõi
- Tỷ lệ thành công/thất bại tải xuống
- Mẫu thông báo lỗi
- Vấn đề người dùng báo cáo
- Thông báo cập nhật yt-dlp

### Số liệu cần Theo dõi
- Thời gian tải xuống trung bình
- Tỷ lệ phần trăm thành công
- Loại lỗi phổ biến nhất
- Thời gian sử dụng cao điểm

## Kiểm soát Phiên bản

### Quy trình Git
1. Tạo nhánh tính năng cho tính năng mới
2. Kiểm thử kỹ lưỡng trước khi hợp nhất
3. Gắn thẻ phát hành với số phiên bản
4. Giữ nhánh `main` ổn định

### Thông điệp Commit
Sử dụng thông điệp commit rõ ràng, mô tả:
```
feat: Thêm bộ chọn chất lượng vào UI
fix: Giải quyết vấn đề đường dẫn FFmpeg trên Windows
docs: Cập nhật hướng dẫn cài đặt
chore: Cập nhật yt-dlp lên phiên bản mới nhất
```

## Danh sách Kiểm tra Kiểm thử

Trước khi triển khai cập nhật:
- [ ] Kiểm thử tải video (nhiều độ phân giải)
- [ ] Kiểm thử trích xuất audio
- [ ] Kiểm thử xử lý lỗi (URL không hợp lệ, lỗi mạng)
- [ ] Kiểm thử với cookies.txt (nếu áp dụng)
- [ ] Kiểm thử trên các hệ điều hành khác nhau (nếu có thể)
- [ ] Xác minh phản hồi UI
- [ ] Kiểm tra đặt tên và tổ chức file
- [ ] Kiểm thử với nội dung giới hạn độ tuổi (nếu áp dụng)

## Tài nguyên

- **Tài liệu yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **Tài liệu Streamlit**: https://docs.streamlit.io
- **Tài liệu FFmpeg**: https://ffmpeg.org/documentation.html
- **Theo dõi Vấn đề**: Theo dõi các vấn đề GitHub của yt-dlp để biết thay đổi API YouTube

