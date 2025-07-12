@echo off
echo 拼多多利润分析系统 - Windows打包脚本
echo =====================================

echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)

echo 正在安装依赖包...
pip install -r requirements.txt

echo 正在打包应用程序...
pyinstaller --onefile --windowed --name=拼多多利润分析系统 --add-data=src;src --add-data=config;config --hidden-import=tkinter --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=pandas --hidden-import=openpyxl --hidden-import=json --hidden-import=datetime gui_app.py

echo 打包完成！
echo 可执行文件位置: dist/拼多多利润分析系统.exe
pause
