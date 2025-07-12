#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润分析系统 - 打包配置文件
支持Windows和Mac系统的可执行文件生成
"""

import sys
import os
from pathlib import Path

# 安装和导入所需的包
try:
    import PyInstaller
except ImportError:
    print("正在安装PyInstaller...")
    os.system(f"{sys.executable} -m pip install pyinstaller")

try:
    import matplotlib
except ImportError:
    print("正在安装matplotlib...")
    os.system(f"{sys.executable} -m pip install matplotlib")

try:
    import pandas
except ImportError:
    print("正在安装pandas...")
    os.system(f"{sys.executable} -m pip install pandas openpyxl")

def create_build_script():
    """创建打包脚本"""
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    
    # PyInstaller配置
    build_command = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # Windows下隐藏命令行窗口
        "--name=拼多多利润分析系统",  # 可执行文件名称
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",  # 图标文件（如果有）
        "--add-data=src;src",  # 包含源代码目录
        "--add-data=config;config",  # 包含配置目录
        "--hidden-import=tkinter",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=json",
        "--hidden-import=datetime",
        "gui_app.py"  # 主程序文件
    ]
    
    # 移除空字符串
    build_command = [cmd for cmd in build_command if cmd]
    
    return " ".join(build_command)

def create_requirements():
    """创建requirements.txt文件"""
    requirements = """
matplotlib>=3.5.0
pandas>=1.3.0
openpyxl>=3.0.9
pyinstaller>=4.8
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements.strip())
    
    print("requirements.txt 已创建")

def create_build_bat():
    """创建Windows批处理文件"""
    bat_content = f"""@echo off
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
{create_build_script()}

echo 打包完成！
echo 可执行文件位置: dist/拼多多利润分析系统.exe
pause
"""
    
    with open("build_windows.bat", "w", encoding="gbk") as f:
        f.write(bat_content)
    
    print("build_windows.bat 已创建")

def create_build_sh():
    """创建Mac/Linux shell脚本"""
    sh_content = f"""#!/bin/bash
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
{create_build_script().replace('pyinstaller', 'python3 -m PyInstaller')}

echo "打包完成！"
echo "可执行文件位置: dist/拼多多利润分析系统"
"""
    
    with open("build_mac.sh", "w", encoding="utf-8") as f:
        f.write(sh_content)
    
    # 给脚本执行权限
    os.chmod("build_mac.sh", 0o755)
    
    print("build_mac.sh 已创建")

def create_setup_py():
    """创建setup.py文件用于打包"""
    setup_content = '''
from setuptools import setup, find_packages

setup(
    name="拼多多利润分析系统",
    version="1.0.0",
    description="专业的拼多多商品利润分析工具",
    author="利润分析系统开发团队",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.9",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'profit-analysis=main:main',
        ],
        'gui_scripts': [
            'profit-analysis-gui=gui_app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
'''
    
    with open("setup.py", "w", encoding="utf-8") as f:
        f.write(setup_content)
    
    print("setup.py 已创建")

def create_readme():
    """创建README文件"""
    readme_content = """# 拼多多利润分析系统

## 功能特点

- 🔢 **单品利润分析**: 详细计算单个商品的利润情况
- 📊 **批量分析**: 支持CSV文件批量分析多个商品
- 📈 **趋势分析**: 可视化不同售价下的利润变化趋势
- 📚 **历史记录**: 完整的历史数据管理和搜索功能
- 📥 **数据导出**: 支持Excel格式的报告导出
- 🖥️ **跨平台**: 支持Windows和Mac系统

## 安装使用

### 方式一：直接运行可执行文件（推荐）

1. 下载对应系统的可执行文件
   - Windows: `拼多多利润分析系统.exe`
   - Mac: `拼多多利润分析系统`

2. 双击运行即可使用

### 方式二：从源码运行

1. 确保已安装Python 3.8+
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行图形界面：
   ```bash
   python gui_app.py
   ```
4. 或运行命令行版本：
   ```bash
   python main.py
   ```

### 方式三：自己打包

1. Windows系统：
   ```cmd
   build_windows.bat
   ```

2. Mac/Linux系统：
   ```bash
   ./build_mac.sh
   ```

## 使用说明

### 单品利润分析
1. 在"单品利润分析"标签页中输入商品信息
2. 点击"计算利润"按钮
3. 查看详细的利润分析报告

### 批量分析
1. 准备CSV文件，包含以下列：
   - model_name: 商品型号
   - price: 商品售价
   - cost: 商品成本
   - other_cost: 其他成本
   - shipping_fee: 运费
   - commission_rate: 平台扣点(%)
   - sales_volume: 销量
   - return_quantity: 退货数量
   - deal_orders: 成交订单数
   - net_deal_orders: 净成交订单数
   - ad_deal_price: 广告出价
   - ad_enabled: 是否启用广告

2. 在"批量分析"标签页选择CSV文件
3. 点击"批量计算"查看结果

### 历史记录管理
- 自动保存每次分析结果
- 支持按型号、利润等条件搜索
- 支持导出历史记录到Excel
- 双击记录查看详情

### 趋势分析
1. 设置价格范围和步长
2. 点击"生成趋势图"
3. 查看利润随价格变化的趋势

## 计算公式

### 基础计算
- **收入** = 分析订单数 × 商品售价
- **商品成本** = 分析订单数 × (商品成本 + 其他成本)
- **运费成本** = 分析订单数 × 运费
- **平台扣点** = 收入 × 平台扣点率
- **广告费用** = 分析订单数 × 每笔广告出价
- **退款广告损失** = 每笔广告出价 × 退款率

### 利润计算
- **总成本** = 商品成本 + 运费成本 + 平台扣点 + 广告费用 + 退款广告损失
- **总利润** = 收入 - 总成本
- **利润率** = (总利润 ÷ 收入) × 100%

### 保本分析
- **保本广告出价** = 售价×(1-扣点率) - 商品成本 - 其他成本 - 运费
- **最高广告投入** = 保本广告出价 × (1 - 退款率)

## 技术支持

如有问题或建议，请联系开发团队。

## 版本信息

当前版本: v1.0.0
更新日期: 2025年7月12日
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md 已创建")

def main():
    """主函数"""
    print("拼多多利润分析系统 - 打包工具")
    print("=" * 40)
    
    # 创建各种配置文件
    create_requirements()
    create_build_bat()
    create_build_sh()
    create_setup_py()
    create_readme()
    
    print("\n所有配置文件已创建完成！")
    print("\n使用方法:")
    print("1. Windows用户: 运行 build_windows.bat")
    print("2. Mac/Linux用户: 运行 ./build_mac.sh")
    print("3. 或者手动运行: python gui_app.py")
    
    # 检查是否可以直接打包
    try:
        import PyInstaller
        print("\n检测到PyInstaller，是否立即开始打包？(y/n)")
        choice = input().lower()
        if choice == 'y':
            print("开始打包...")
            command = create_build_script()
            os.system(command)
            print("打包完成！")
    except ImportError:
        print("\n提示: 请先安装PyInstaller: pip install pyinstaller")

if __name__ == "__main__":
    main()