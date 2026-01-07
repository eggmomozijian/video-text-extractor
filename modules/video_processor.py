import os
from PIL import Image
import pytesseract
from moviepy.editor import VideoFileClip

class VideoProcessor:
    def __init__(self):
        self.download_folder = 'downloads'
        os.makedirs(self.download_folder, exist_ok=True)
    
    def extract_text(self, video_path):
        """
        Extract text from video using OCR (simplified version)
        """
        try:
            # Extract text from video frames (OCR)
            ocr_text = self._extract_text_from_frames(video_path)
            
            # Combine results
            result = ""
            if ocr_text:
                result += "=== 画面文字内容 ===\n" + ocr_text + "\n\n"
            
            result += "💡 提示：语音转文字功能需要较大的AI模型，在免费服务器上暂时无法使用。如需此功能，建议在本地运行或升级服务器配置。"
            
            if not result:
                result = "未检测到文字内容"
            
            return result.strip()
        
        except Exception as e:
            print(f"Text extraction error: {e}")
            return f"文字提取失败: {str(e)}"
    
    def _extract_text_from_frames(self, video_path, sample_rate=30):
        """
        Extract text from video frames using OCR (without OpenCV)
        """
        try:
            # Use moviepy to extract frames
            video = VideoFileClip(video_path)
            duration = video.duration
            fps = video.fps
            
            extracted_texts = set()
            
            # Sample frames every sample_rate seconds
            for t in range(0, int(duration), sample_rate):
                frame = video.get_frame(t)
                
                # Convert to PIL Image
                pil_img = Image.fromarray(frame.astype('uint8'), 'RGB')
                
                # Convert to grayscale
                gray_img = pil_img.convert('L')
                
                # Extract text with Chinese support
                text = pytesseract.image_to_string(gray_img, lang='chi_sim+eng')
                text = text.strip()
                
                if text:
                    extracted_texts.add(text)
            
            video.close()
            
            return "\n".join(extracted_texts) if extracted_texts else ""
        
        except Exception as e:
            print(f"OCR error: {e}")
            return "OCR文字识别功能需要服务器安装Tesseract-OCR，当前环境暂不支持"
    
    def _extract_text_from_audio(self, video_path):
        """
        Extract text from audio - disabled in light version
        """
        return ""
    
    def extract_audio(self, video_path, file_id):
        """
        Extract audio from video
        """
        try:
            output_path = os.path.join(self.download_folder, f"{file_id}_audio.mp3")
            
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                raise Exception("视频中没有音频轨道")
            
            audio.write_audiofile(output_path, logger=None)
            video.close()
            
            return output_path
        
        except Exception as e:
            raise Exception(f"音频提取失败: {str(e)}")
    
    def extract_video(self, video_path, file_id):
        """
        Copy video to download folder
        """
        import shutil
        try:
            output_path = os.path.join(self.download_folder, f"{file_id}_video.mp4")
            shutil.copy(video_path, output_path)
            return output_path
        except Exception as e:
            raise Exception(f"视频处理失败: {str(e)}")
