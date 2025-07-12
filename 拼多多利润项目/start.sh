#!/bin/bash

echo "🚀 启动拼多多利润分析系统..."
echo "📦 安装依赖包..."
python3 -m pip install -r requirements.txt

echo "🎯 启动Web应用..."
python3 -m streamlit run main.py 