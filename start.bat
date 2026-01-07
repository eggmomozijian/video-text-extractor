@echo off
chcp 65001 >nul
title 视频文字提取工具

echo ========================================
echo    视频文字提取工具
echo ========================================
echo.
echo 正在启动服务器...
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit
)

REM 检查 Node.js 是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit
)

REM 检查是否已安装依赖
if not exist "node_modules\" (
    echo [提示] 首次运行，正在安装前端依赖...
    call npm install
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit
    )
)

if not exist "venv\" (
    echo [提示] 首次运行，正在创建 Python 虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit
    )
    
    echo [提示] 正在安装后端依赖...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 后端依赖安装失败
        pause
        exit
    )
)

REM 创建必要的文件夹
if not exist "uploads\" mkdir uploads
if not exist "downloads\" mkdir downloads

REM 启动后端服务器
echo [启动] 正在启动后端服务器...
start /B cmd /c "venv\Scripts\activate.bat && python app.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端开发服务器
echo [启动] 正在启动前端服务器...
start /B cmd /c "npm run dev"

REM 等待前端启动
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo    服务启动成功！
echo ========================================
echo.
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:5000
echo.
echo 浏览器将自动打开，如未打开请手动访问:
echo http://localhost:3000
echo.
echo 按 Ctrl+C 或关闭此窗口可停止服务
echo ========================================
echo.

REM 打开浏览器
start http://localhost:3000

REM 保持窗口打开
pause >nul
