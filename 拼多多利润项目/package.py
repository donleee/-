#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润分析系统 - 简化打包脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("正在安装 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 安装完成")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 安装失败")
            return False

def build_executable():
    """构建可执行文件"""
    print("开始打包...")
    
    # 构建命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # 单文件
        "--windowed",  # 无控制台窗口
        "--name=ProfitAnalysis",  # 可执行文件名
        "--add-data=src:src",  # 包含源代码
        "--add-data=config:config",  # 包含配置
        "--hidden-import=tkinter",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "start.py"  # 入口文件
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ 打包成功！")
        
        # 检查生成的文件
        dist_dir = Path("dist")
        if dist_dir.exists():
            files = list(dist_dir.glob("*"))
            print(f"生成的文件: {files}")
            
            # 重命名文件
            if sys.platform == "win32":
                exe_name = "拼多多利润分析系统.exe"
                old_file = dist_dir / "ProfitAnalysis.exe"
            else:
                exe_name = "拼多多利润分析系统"
                old_file = dist_dir / "ProfitAnalysis"
            
            new_file = dist_dir / exe_name
            if old_file.exists():
                shutil.move(str(old_file), str(new_file))
                print(f"✅ 可执行文件已生成: {new_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

def create_portable_package():
    """创建便携版本"""
    print("创建便携版本...")
    
    # 创建便携目录
    portable_dir = Path("拼多多利润分析系统_便携版")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir()
    
    # 复制必要文件
    files_to_copy = [
        "start.py",
        "gui_app.py", 
        "main.py",
        "src/",
        "config/",
        "requirements.txt",
        "README.md"
    ]
    
    for file_path in files_to_copy:
        source = Path(file_path)
        if source.exists():
            if source.is_dir():
                shutil.copytree(source, portable_dir / source.name)
            else:
                shutil.copy2(source, portable_dir / source.name)
    
    # 创建启动脚本
    if sys.platform == "win32":
        # Windows批处理文件
        bat_content = '''@echo off
cd /d "%~dp0"
python start.py
pause'''
        with open(portable_dir / "启动.bat", "w", encoding="gbk") as f:
            f.write(bat_content)
    
    # shell脚本
    sh_content = '''#!/bin/bash
cd "$(dirname "$0")"
python3 start.py'''
    
    sh_file = portable_dir / "启动.sh"
    with open(sh_file, "w", encoding="utf-8") as f:
        f.write(sh_content)
    
    # 给shell脚本执行权限
    if hasattr(os, 'chmod'):
        os.chmod(sh_file, 0o755)
    
    print(f"✅ 便携版本已创建: {portable_dir}")

def main():
    """主函数"""
    print("拼多多利润分析系统 - 打包工具")
    print("=" * 40)
    
    print("选择打包方式:")
    print("1. 生成单个可执行文件 (推荐)")
    print("2. 创建便携版本 (包含源代码)")
    print("3. 两者都生成")
    
    try:
        choice = input("请选择 (1/2/3): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "3"  # 默认选择
    
    success = True
    
    if choice in ["1", "3"]:
        if install_pyinstaller():
            success = build_executable()
        else:
            success = False
    
    if choice in ["2", "3"]:
        create_portable_package()
    
    if success:
        print("\n🎉 打包完成！")
        print("\n使用说明:")
        print("- 可执行文件: 双击 dist/拼多多利润分析系统 运行")
        print("- 便携版本: 进入便携版目录，运行启动脚本")
    else:
        print("\n❌ 打包过程中出现错误")
    
    try:
        input("\n按回车键退出...")
    except (EOFError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    main()