# 视频内容提取工具

一个功能强大的视频内容提取网站，支持上传视频和解析主流平台链接，实现文本、音频、视频的智能提取。

## ✨ 功能特性

- 📹 **视频上传**: 支持本地视频文件上传（MP4, AVI, MOV等格式）
- 🔗 **链接解析**: 支持小红书、抖音、视频号、B站分享链接
- 📝 **文本提取**: OCR识别画面文字 + 语音转文字
- 🎵 **音频提取**: 从视频中提取音频文件
- 💾 **视频下载**: 下载原始视频文件

## 🚀 快速开始

### 前置要求

- Node.js 16+
- Python 3.8+
- Tesseract OCR（用于文字识别）

### 安装 Tesseract OCR

**Windows:**
1. 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装后添加到系统环境变量
3. 下载中文语言包（chi_sim.traineddata）到 Tesseract 的 tessdata 目录

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim
```

### 安装依赖

**前端:**
```bash
npm install
```

**后端:**
```bash
pip install -r requirements.txt
```

### 运行项目

**启动后端服务:**
```bash
python app.py
```
后端服务将运行在 http://localhost:5000

**启动前端开发服务器:**
```bash
npm run dev
```
前端将运行在 http://localhost:3000

## 📖 使用说明

### 1. 上传视频

- 点击"上传视频"标签
- 选择提取类型（文本/音频/视频）
- 拖拽或选择视频文件
- 点击"开始提取"按钮

### 2. 解析链接

- 点击"解析链接"标签
- 选择平台（支持自动识别）
- 粘贴分享链接
- 选择提取类型
- 点击"开始提取"按钮

### 支持的平台

- 🔴 **小红书** (xiaohongshu.com)
- 🎵 **抖音** (douyin.com)
- 💬 **视频号** (channels.weixin.qq.com)
- 📺 **哔哩哔哩** (bilibili.com)

## 🛠️ 技术栈

### 前端
- React 18
- Vite
- Tailwind CSS
- Axios
- Lucide Icons

### 后端
- Flask
- OpenCV (视频处理)
- Tesseract OCR (文字识别)
- Whisper (语音转文字)
- MoviePy (音频提取)
- yt-dlp (视频下载)

## 📝 注意事项

1. **Whisper 模型**: 语音转文字功能需要下载 Whisper 模型，首次使用会自动下载，需要较好的网络环境
2. **文件大小**: 默认支持最大 500MB 的视频文件
3. **处理时间**: 根据视频长度和复杂度，处理时间可能从几秒到几分钟不等
4. **平台限制**: 部分平台可能有反爬虫机制，建议使用官方分享链接

## 🔧 配置

可以在 `app.py` 中修改以下配置：

```python
UPLOAD_FOLDER = 'uploads'  # 上传目录
DOWNLOAD_FOLDER = 'downloads'  # 下载目录
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 最大文件大小
```

## 📦 项目结构

```
.
├── src/                    # 前端源代码
│   ├── App.jsx            # 主应用组件
│   ├── main.jsx           # 入口文件
│   └── index.css          # 样式文件
├── modules/                # 后端模块
│   ├── video_processor.py # 视频处理
│   └── link_parser.py     # 链接解析
├── app.py                 # Flask 后端服务
├── package.json           # 前端依赖
├── requirements.txt       # 后端依赖
└── README.md             # 说明文档
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License
