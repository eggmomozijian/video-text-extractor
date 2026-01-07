# 🚀 Replit 部署指南

## 📋 部署步骤（超简单！）

### 第一步：推送更新到 GitHub

在命令行执行：

```bash
cd "d:/莫孜健全部东西/ai coding/shipintiquwenzi"

git add .

git commit -m "Add Replit configuration"

git push origin main
```

### 第二步：在 Replit 导入项目

1. 访问 **https://replit.com**

2. 点击右上角 **"Sign up"** 或 **"Log in"**
   - 选择 **"Continue with GitHub"**（用 GitHub 账号登录）
   - 授权 Replit 访问

3. 登录后，点击左侧 **"+ Create Repl"**

4. 选择 **"Import from GitHub"**

5. 在 **GitHub URL** 输入框填写：
   ```
   https://github.com/eggmomozijian/video-text-extractor
   ```

6. 点击 **"Import from GitHub"** 按钮

### 第三步：等待自动配置

Replit 会自动：
- ✅ 检测项目类型
- ✅ 安装依赖
- ✅ 配置环境

**不需要任何手动操作！**

### 第四步：运行项目

1. Replit 界面加载完成后，点击顶部的绿色 **"Run"** 按钮

2. 等待 2-3 分钟（首次运行需要安装所有依赖）

3. 看到 "✅ 服务启动成功！" 提示

4. Replit 会自动在右侧显示网页预览

5. 点击顶部的 **"Open in new tab"** 图标，在新标签页打开

### 第五步：分享给朋友！🎉

1. 点击 Replit 顶部的 **"Share"** 按钮

2. 复制 **"Repl URL"** 链接，类似：
   ```
   https://video-text-extractor.eggmomozijian.repl.co
   ```

3. 把这个链接发给朋友，**手机电脑都能直接打开使用！**

---

## 📱 手机使用

直接用手机浏览器打开链接即可：
- ✅ Safari（iOS）
- ✅ Chrome（Android）
- ✅ 微信内置浏览器

**完全不需要安装任何东西！**

---

## 🔧 如果遇到问题

### 问题1：Run 按钮无法点击
**解决**：等待右侧面板加载完成，通常需要 30 秒

### 问题2：提示依赖安装失败
**解决**：
1. 点击左侧 **"Shell"** 标签
2. 输入 `bash start.sh` 手动运行
3. 查看错误信息

### 问题3：页面无法打开
**解决**：
1. 检查右侧 **"Console"** 是否有错误
2. 确保防火墙没有拦截
3. 尝试刷新页面

### 问题4：功能不可用
**说明**：
- OCR 文字识别需要 Tesseract
- 语音转文字功能受限于服务器资源
- 部分功能可能需要时间加载

---

## ⚡ 性能优化

### 保持服务活跃

Replit 免费版会在不活动时休眠，可以使用：

1. **UptimeRobot**（https://uptimerobot.com）
   - 注册账号
   - 添加你的 Replit 网址
   - 设置每 5 分钟 ping 一次

2. **Cron-job.org**（https://cron-job.org）
   - 同样的方法设置定时访问

---

## 💰 费用说明

- ✅ **完全免费**
- ✅ 无需信用卡
- ✅ 每月 100 小时免费运行时间
- ✅ 够个人和朋友使用

如果流量很大，可以升级到 **Replit Hacker Plan**（$7/月）

---

## 🎯 使用限制

Replit 免费版限制：
- 💾 存储空间：500MB
- ⏱️ 运行时间：100 小时/月
- 😴 休眠：30 分钟不活动会休眠
- 🌐 带宽：有限制

**对于个人使用完全够用！**

---

## 📸 截图说明

### 1. 导入界面
![Import from GitHub](填入你的仓库地址)

### 2. 运行界面
![Run 按钮](点击 Run 启动服务)

### 3. 分享界面
![Share 按钮](复制链接分享给朋友)

---

## 🎉 完成！

现在你有了一个：
- ✅ 可以在手机上用的网站
- ✅ 可以分享给朋友的链接
- ✅ 完全免费的在线服务

**享受你的视频文字提取工具吧！** 🚀

---

## 📞 需要帮助？

如果部署遇到问题：
1. 检查 GitHub 仓库是否公开
2. 查看 Replit Console 的错误信息
3. 确认所有配置文件都已推送到 GitHub
4. 在 Replit 社区寻求帮助

---

**祝部署顺利！** 🎊
