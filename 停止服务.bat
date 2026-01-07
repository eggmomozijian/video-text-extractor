@echo off
chcp 65001 >nul
title 停止服务

echo 正在停止所有服务...

REM 停止 Python 进程
taskkill /F /IM python.exe >nul 2>&1

REM 停止 Node 进程
taskkill /F /IM node.exe >nul 2>&1

echo 服务已停止！
timeout /t 2 /nobreak >nul
