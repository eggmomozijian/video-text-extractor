import cv2
import os
from PIL import Image
import pytesseract
from moviepy.editor import VideoFileClip
import numpy as np

class VideoProcessor:
    def __init__(self):
        self.download_folder = 'downloads'
        os.makedirs(self.download_folder, exist_ok=True)
    
    def extract_text(self, video_path):
        """
        Extract text from video using OCR and speech recognition
        """
        try:
            # Extract text from video frames (OCR)
            ocr_text = self._extract_text_from_frames(video_path)
            
            # Extract text from audio (Speech-to-Text)
            audio_text = self._extract_text_from_audio(video_path)
            
            # Combine results
            result = ""
            if ocr_text:
                result += "=== 画面文字内容 ===\n" + ocr_text + "\n\n"
            if audio_text:
                result += "=== 语音文字内容 ===\n" + audio_text
            
            if not result:
                result = "未检测到文字内容"
            
            return result.strip()
        
        except Exception as e:
            print(f"Text extraction error: {e}")
            return f"文字提取失败: {str(e)}"
    
    def _extract_text_from_frames(self, video_path, sample_rate=30):
        """
        Extract text from video frames using OCR
        """
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * sample_rate) if fps > 0 else 30
            
            extracted_texts = set()
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Sample frames at intervals
                if frame_count % frame_interval == 0:
                    # Convert to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold to improve OCR accuracy
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Convert to PIL Image
                    pil_img = Image.fromarray(thresh)
                    
                    # Extract text with Chinese support
                    text = pytesseract.image_to_string(pil_img, lang='chi_sim+eng')
                    text = text.strip()
                    
                    if text:
                        extracted_texts.add(text)
                
                frame_count += 1
            
            cap.release()
            
            return "\n".join(extracted_texts) if extracted_texts else ""
        
        except Exception as e:
            print(f"OCR error: {e}")
            return ""
    
    def _extract_text_from_audio(self, video_path):
        """
        Extract text from audio using Whisper (Speech-to-Text)
        """
        try:
            # Note: Whisper requires significant resources
            # For a lightweight version, you might want to use an API
            # Here's a placeholder implementation
            
            import whisper
            
            # Extract audio first
            import tempfile
            temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            audio_path = temp_audio.name
            temp_audio.close()
            
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, logger=None)
            video.close()
            
            # Load Whisper model (use 'base' for faster processing)
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, language='zh')
            
            # Cleanup
            os.unlink(audio_path)
            
            return result['text']
        
        except Exception as e:
            print(f"Speech-to-text error: {e}")
            # Return a message instead of empty string
            return "语音转文字功能需要安装 Whisper 模型（较大），暂时跳过"
    
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
