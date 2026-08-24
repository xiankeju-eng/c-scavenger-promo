#!/bin/bash
# Quick Start Script for C-Scavenger
# 快速启动脚本

echo ""
echo "========================================"
echo "  C-Scavenger - 快速启动"
echo "========================================"
echo ""

# 检查 Python 是否已安装
if ! command -v python3 &> /dev/null; then
    echo "[×] 未检测到 Python3！"
    echo ""
    echo "解决方案:"
    echo "1. 请先安装 Python 3.6 或更高版本"
    echo "2. Ubuntu/Debian: sudo apt-get install python3"
    echo "3. macOS: brew install python3"
    echo ""
    exit 1
fi

echo "[√] 检测到 Python3"
echo ""
echo "[*] 正在启动 C-Scavenger..."
echo ""

# 运行主程序
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[×] 程序执行出错！"
    echo ""
fi
