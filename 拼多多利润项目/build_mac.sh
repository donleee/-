#!/bin/bash
echo "拼多多利润分析系统 - Mac/Linux打包脚本"
echo "========================================"

echo "正在检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到Python环境，请先安装Python 3.8+"
    exit 1
fi

echo "正在安装依赖包..."
pip3 install -r requirements.txt

echo "正在打包应用程序..."
python3 -m PyInstaller --onefile --windowed --name=拼多多利润分析系统 --add-data=src;src --add-data=config;config --hidden-import=tkinter --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=pandas --hidden-import=openpyxl --hidden-import=json --hidden-import=datetime gui_app.py

echo "打包完成！"
echo "可执行文件位置: dist/拼多多利润分析系统"
