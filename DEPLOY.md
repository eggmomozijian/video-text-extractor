# 🚀 Render 部署指南

## 快速部署步骤

### 1️⃣ 准备工作

首先，你需要把代码上传到 GitHub：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 在 GitHub 上创建新仓库，然后关联
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 2️⃣ 注册 Render

1. 访问 https://render.com
2. 点击 "Get Started" 或 "Sign Up"
3. 使用 GitHub 账号登录（推荐）

### 3️⃣ 部署后端

1. 登录 Render 后，点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置如下：
   - **Name**: `video-extractor-api`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn app:app
     ```
   - **Instance Type**: 选择 `Free`

4. 点击 "Advanced" 展开高级设置
5. 添加环境变量（可选）
6. 点击 "Create Web Service"

**重要**：部署后，记下你的后端网址，比如：
```
https://video-extractor-api.onrender.com
```

### 4️⃣ 部署前端

1. 回到 Render Dashboard，点击 "New +" → "Static Site"
2. 连接同一个 GitHub 仓库
3. 配置如下：
   - **Name**: `video-extractor`
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Publish Directory**: `dist`

4. **关键步骤**：在部署前，需要修改前端代码中的 API 地址

### 5️⃣ 更新前端 API 地址

修改 `vite.config.js`，将后端地址改为你的 Render 后端网址：

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://video-extractor-api.onrender.com', // 改成你的后端地址
        changeOrigin: true
      }
    }
  },
  // 添加生产环境配置
  define: {
    'process.env.VITE_API_URL': JSON.stringify('https://video-extractor-api.onrender.com')
  }
})
```

或者在 `src/App.jsx` 中直接使用完整 API 地址：

```javascript
// 修改 axios 请求
const API_URL = 'https://video-extractor-api.onrender.com'

// 在请求中使用
await axios.post(`${API_URL}/api/upload`, formData)
```

### 6️⃣ 部署完成

提交代码更改并推送：
```bash
git add .
git commit -m "Update API URL for production"
git push
```

Render 会自动重新部署。几分钟后，你就可以通过网址访问了：
```
https://video-extractor.onrender.com
```

---

## ⚠️ 注意事项

### 免费套餐限制

Render 免费套餐有以下限制：
- 服务会在 15 分钟不活动后休眠
- 首次访问可能需要等待 30-50 秒唤醒
- 每月 750 小时免费使用时间
- 存储空间有限

### 解决休眠问题

可以使用以下服务保持服务活跃：
- UptimeRobot (https://uptimerobot.com)
- Cron-job.org (https://cron-job.org)

每 10 分钟 ping 一次你的网站即可。

### 大文件处理

如果需要处理超大视频文件，建议：
1. 升级到付费套餐（$7/月起）
2. 或者使用对象存储（如 AWS S3, 腾讯云 COS）

---

## 🎯 更简单的方式：一键部署

如果你觉得上面的步骤还是复杂，可以使用：

### Railway（推荐新手）
1. 访问 https://railway.app
2. 用 GitHub 登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. Railway 会自动检测并部署

### Vercel（仅前端）
```bash
npm install -g vercel
vercel login
vercel
```

---

## 📞 需要帮助？

如果部署遇到问题，检查：
1. GitHub 仓库是否公开
2. requirements.txt 是否正确
3. API 地址是否更新
4. Render 构建日志中的错误信息

祝部署顺利！🎉
