
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
