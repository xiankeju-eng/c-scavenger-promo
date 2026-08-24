@echo off
REM C-Scavenger Build Script
REM 将 Python 脚本打包成 .exe 文件

echo.
echo ========================================
echo   C-Scavenger - Build Script
echo ========================================
echo.

REM 检查 PyInstaller 是否已安装
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [*] 未检测到 PyInstaller，正在安装...
    python -m pip install pyinstaller
) else (
    echo [√] PyInstaller 已安装
)

echo.
echo [*] 开始打包...
echo.

REM 删除旧的 build 目录
if exist build (
    echo [*] 删除旧的构建文件...
    rmdir /s /q build
)

if exist dist (
    echo [*] 清理旧的输出文件...
    rmdir /s /q dist
)

echo.

REM 使用 PyInstaller 打包
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "C-Scavenger" ^
    --console ^
    main.py

if errorlevel 1 (
    echo.
    echo [×] 打包失败！
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [√] 打包完成！
echo ========================================
echo.
echo 输出文件位置:
echo   dist\C-Scavenger.exe
echo.
echo 使用方式:
echo   1. 双击 C-Scavenger.exe 运行程序
echo   2. 将 exe 文件复制到 U 盘即可在任何电脑上使用
echo.
pause