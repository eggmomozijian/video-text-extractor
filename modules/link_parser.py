import yt_dlp
import os
import re
import requests

class LinkParser:
    def __init__(self):
        self.download_folder = 'downloads'
        os.makedirs(self.download_folder, exist_ok=True)
    
    def detect_platform(self, url):
        """
        Detect platform from URL
        """
        url = url.lower()
        
        if 'xiaohongshu' in url or 'xhslink' in url or 'redbook' in url:
            return 'xiaohongshu'
        elif 'douyin' in url or 'iesdouyin' in url:
            return 'douyin'
        elif 'weixin' in url or 'qq.com' in url and 'channels' in url:
            return 'weixin'
        elif 'bilibili' in url or 'b23.tv' in url:
            return 'bilibili'
        else:
            return 'unknown'
    
    def download_video(self, url, platform, file_id):
        """
        Download video from platform URL
        """
        try:
            output_path = os.path.join(self.download_folder, f"{file_id}_%(title)s.%(ext)s")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
                'quiet': False,
                'no_warnings': False,
            }
            
            # Platform-specific configurations
            if platform == 'bilibili':
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
            elif platform == 'douyin':
                # Douyin might require special headers
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.douyin.com/'
                }
            
            elif platform == 'xiaohongshu':
                # Xiaohongshu might require cookies or special handling
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            
            elif platform == 'weixin':
                # WeChat video channel
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://channels.weixin.qq.com/'
                }
            
            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            return filename
        
        except Exception as e:
            print(f"Download error: {e}")
            raise Exception(f"视频下载失败: {str(e)}")
    
    def extract_share_url(self, text):
        """
        Extract actual URL from share text
        """
        # Pattern for URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        if urls:
            return urls[0]
        
        return text
