from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import json

# Import processing modules
from modules.video_processor import VideoProcessor
from modules.link_parser import LinkParser

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # Get extract type
        extract_type = request.form.get('extract_type', 'text')
        
        # Save file with unique name
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{file_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)
        
        # Process video
        processor = VideoProcessor()
        
        if extract_type == 'text':
            # Extract text from video (OCR + speech-to-text)
            text = processor.extract_text(filepath)
            result = {'text': text, 'type': 'text'}
        
        elif extract_type == 'audio':
            # Extract audio
            audio_path = processor.extract_audio(filepath, file_id)
            audio_url = f'/api/download/{os.path.basename(audio_path)}'
            result = {'audio_url': audio_url, 'type': 'audio'}
        
        elif extract_type == 'video':
            # Just return the uploaded video
            video_url = f'/api/download/{saved_filename}'
            result = {'video_url': video_url, 'type': 'video'}
        
        else:
            return jsonify({'error': '无效的提取类型'}), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/extract-link', methods=['POST'])
def extract_link():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        platform = data.get('platform', 'auto')
        extract_type = data.get('extract_type', 'text')
        
        if not url:
            return jsonify({'error': '链接不能为空'}), 400
        
        # Parse and download video from platform
        parser = LinkParser()
        
        # Detect platform if auto
        if platform == 'auto':
            platform = parser.detect_platform(url)
        
        # Download video
        file_id = str(uuid.uuid4())
        video_path = parser.download_video(url, platform, file_id)
        
        if not video_path:
            return jsonify({'error': '下载视频失败'}), 500
        
        # Process based on extract type
        processor = VideoProcessor()
        
        if extract_type == 'text':
            text = processor.extract_text(video_path)
            result = {'text': text, 'type': 'text'}
        
        elif extract_type == 'audio':
            audio_path = processor.extract_audio(video_path, file_id)
            audio_url = f'/api/download/{os.path.basename(audio_path)}'
            result = {'audio_url': audio_url, 'type': 'audio'}
        
        elif extract_type == 'video':
            video_url = f'/api/download/{os.path.basename(video_path)}'
            result = {'video_url': video_url, 'type': 'video'}
        
        else:
            return jsonify({'error': '无效的提取类型'}), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        # Check in both folders
        if os.path.exists(os.path.join(app.config['DOWNLOAD_FOLDER'], filename)):
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)
        elif os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Server is running'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
