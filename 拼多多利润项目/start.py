#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润分析系统 - 启动器
一键启动图形界面版本
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查依赖包"""
    required_packages = {
        'tkinter': 'tkinter',
        'matplotlib': 'matplotlib',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(pip_name)
            print(f"❌ {package} (缺失)")
    
    if missing_packages:
        print(f"\n需要安装以下包: {', '.join(missing_packages)}")
        print("正在自动安装...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} 安装完成")
            except subprocess.CalledProcessError:
                print(f"❌ {package} 安装失败")
                return False
    
    return True

def main():
    """主函数"""
    print("拼多多利润分析系统")
    print("=" * 30)
    print("正在检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ 需要Python 3.6+版本")
        input("按回车键退出...")
        return
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖包安装失败")
        input("按回车键退出...")
        return
    
    print("\n✅ 环境检查完成，正在启动GUI界面...")
    
    try:
        # 导入并启动GUI
        from gui_app import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n尝试使用命令行版本...")
        try:
            from main import main as cli_main
            cli_main()
        except Exception as e2:
            print(f"❌ 命令行版本也启动失败: {e2}")
            input("按回车键退出...")

if __name__ == "__main__":
    main()