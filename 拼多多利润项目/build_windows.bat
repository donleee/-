@echo off
echo ƴ����������ϵͳ - Windows����ű�
echo =====================================

echo ���ڼ��Python����...
python --version
if errorlevel 1 (
    echo ����: δ�ҵ�Python���������Ȱ�װPython 3.8+
    pause
    exit /b 1
)

echo ���ڰ�װ������...
pip install -r requirements.txt

echo ���ڴ��Ӧ�ó���...
pyinstaller --onefile --windowed --name=ƴ����������ϵͳ --add-data=src;src --add-data=config;config --hidden-import=tkinter --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=pandas --hidden-import=openpyxl --hidden-import=json --hidden-import=datetime gui_app.py

echo �����ɣ�
echo ��ִ���ļ�λ��: dist/ƴ����������ϵͳ.exe
pause
