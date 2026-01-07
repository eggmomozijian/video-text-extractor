import { useState } from 'react'
import { Upload, Link as LinkIcon, FileText, Music, Video, Loader2, CheckCircle, XCircle } from 'lucide-react'
import axios from 'axios'

// API URL - 在生产环境中会使用环境变量
const API_URL = import.meta.env.VITE_API_URL || ''

function App() {
  const [activeTab, setActiveTab] = useState('upload') // 'upload' or 'link'
  const [file, setFile] = useState(null)
  const [url, setUrl] = useState('')
  const [platform, setPlatform] = useState('auto')
  const [extractType, setExtractType] = useState('text') // 'text', 'audio', 'video'
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleUploadSubmit = async () => {
    if (!file) {
      setError('请选择要上传的视频文件')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('extract_type', extractType)

    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || '处理失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const handleLinkSubmit = async () => {
    if (!url.trim()) {
      setError('请输入有效的链接')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/api/extract-link`, {
        url: url.trim(),
        platform,
        extract_type: extractType,
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || '处理失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = (fileUrl, filename) => {
    const link = document.createElement('a')
    link.href = fileUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">视频内容提取工具</h1>
          <p className="text-white/80 text-lg">支持上传视频或解析平台链接，提取文字、音频和视频内容</p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                activeTab === 'upload'
                  ? 'bg-primary text-white border-b-4 border-primary'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Upload className="inline-block mr-2 w-5 h-5" />
              上传视频
            </button>
            <button
              onClick={() => setActiveTab('link')}
              className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                activeTab === 'link'
                  ? 'bg-primary text-white border-b-4 border-primary'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <LinkIcon className="inline-block mr-2 w-5 h-5" />
              解析链接
            </button>
          </div>

          <div className="p-8">
            {/* Extract Type Selection */}
            <div className="mb-8">
              <label className="block text-gray-700 font-semibold mb-3">提取类型</label>
              <div className="grid grid-cols-3 gap-4">
                <button
                  onClick={() => setExtractType('text')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    extractType === 'text'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <FileText className="w-8 h-8 mx-auto mb-2" />
                  <div className="font-semibold">文本提取</div>
                  <div className="text-xs text-gray-500 mt-1">OCR + 语音转文字</div>
                </button>
                <button
                  onClick={() => setExtractType('audio')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    extractType === 'audio'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Music className="w-8 h-8 mx-auto mb-2" />
                  <div className="font-semibold">音频提取</div>
                  <div className="text-xs text-gray-500 mt-1">提取音频文件</div>
                </button>
                <button
                  onClick={() => setExtractType('video')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    extractType === 'video'
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Video className="w-8 h-8 mx-auto mb-2" />
                  <div className="font-semibold">视频下载</div>
                  <div className="text-xs text-gray-500 mt-1">下载原视频</div>
                </button>
              </div>
            </div>

            {/* Upload Tab */}
            {activeTab === 'upload' && (
              <div>
                <label className="block text-gray-700 font-semibold mb-3">选择视频文件</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors">
                  <input
                    type="file"
                    accept="video/*"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <Upload className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-600 mb-2">
                      {file ? file.name : '点击选择视频文件或拖拽到此处'}
                    </p>
                    <p className="text-sm text-gray-400">支持 MP4, AVI, MOV 等格式</p>
                  </label>
                </div>
                <button
                  onClick={handleUploadSubmit}
                  disabled={loading || !file}
                  className="w-full mt-6 bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <>
                      <Loader2 className="inline-block mr-2 w-5 h-5 animate-spin" />
                      处理中...
                    </>
                  ) : (
                    '开始提取'
                  )}
                </button>
              </div>
            )}

            {/* Link Tab */}
            {activeTab === 'link' && (
              <div>
                <label className="block text-gray-700 font-semibold mb-3">视频平台</label>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="auto">自动识别</option>
                  <option value="xiaohongshu">小红书</option>
                  <option value="douyin">抖音</option>
                  <option value="weixin">视频号</option>
                  <option value="bilibili">哔哩哔哩</option>
                </select>

                <label className="block text-gray-700 font-semibold mb-3">分享链接</label>
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="粘贴小红书/抖音/视频号/B站分享链接"
                  className="w-full p-3 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-primary"
                />

                <button
                  onClick={handleLinkSubmit}
                  disabled={loading || !url.trim()}
                  className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary/90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? (
                    <>
                      <Loader2 className="inline-block mr-2 w-5 h-5 animate-spin" />
                      处理中...
                    </>
                  ) : (
                    '开始提取'
                  )}
                </button>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
                <XCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5" />
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {/* Result */}
            {result && (
              <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center mb-4">
                  <CheckCircle className="w-6 h-6 text-green-500 mr-2" />
                  <h3 className="text-lg font-semibold text-green-800">提取成功</h3>
                </div>

                {extractType === 'text' && result.text && (
                  <div className="bg-white p-4 rounded-lg">
                    <h4 className="font-semibold mb-2">提取的文本内容：</h4>
                    <pre className="whitespace-pre-wrap text-gray-700">{result.text}</pre>
                  </div>
                )}

                {extractType === 'audio' && result.audio_url && (
                  <div>
                    <audio controls className="w-full mb-4">
                      <source src={result.audio_url} type="audio/mpeg" />
                    </audio>
                    <button
                      onClick={() => downloadFile(result.audio_url, 'audio.mp3')}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                    >
                      下载音频
                    </button>
                  </div>
                )}

                {extractType === 'video' && result.video_url && (
                  <div>
                    <video controls className="w-full mb-4 rounded-lg">
                      <source src={result.video_url} />
                    </video>
                    <button
                      onClick={() => downloadFile(result.video_url, 'video.mp4')}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                    >
                      下载视频
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-white/70">
          <p>支持小红书、抖音、视频号、哔哩哔哩等平台</p>
        </div>
      </div>
    </div>
  )
}

export default App
