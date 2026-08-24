@echo off
REM Quick Start Script for C-Scavenger
REM 快速启动脚本

echo.
echo ========================================
echo   C-Scavenger - 快速启动
echo ========================================
echo.

REM 检查 Python 是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [×] 未检测到 Python！
    echo.
    echo 解决方案：
    echo 1. 请先安装 Python 3.6 或更高版本
    echo 2. 下载地址: https://www.python.org/downloads/
    echo 3. 安装时请勾选"Add Python to PATH"
    echo.
    echo 或者使用 .exe 版本：
    echo 1. 运行 build.bat 打包成 .exe
    echo 2. 然后双击 dist\C-Scavenger.exe
    echo.
    pause
    exit /b 1
)

echo [√] 检测到 Python
echo.
echo [*] 正在启动 C-Scavenger...
echo.

REM 运行主程序
python main.py

if errorlevel 1 (
    echo.
    echo [×] 程序执行出错！
    echo.
    pause
)
