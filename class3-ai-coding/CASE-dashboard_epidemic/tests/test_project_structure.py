#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目结构测试文件
用于验证项目目录结构和关键文件是否存在
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_project_structure():
    """测试项目结构是否完整"""
    # 定义期望存在的目录和文件
    expected_dirs = [
        'config',
        'docs',
        'src',
        'src/app',
        'src/data',
        'src/utils',
        'src/visualization',
        'static',
        'static/css',
        'static/js',
        'templates',
        'tests'
    ]
    
    expected_files = [
        'config/config.yaml',
        'requirements.txt',
        'README.md',
        'src/app/app.py',
        'src/data/read_excel_data.py',
        'src/data/calculate_confirmed_cases.py',
        'src/visualization/advanced_visualization.py',
        'src/utils/run_analysis.bat',
        'src/utils/run_analysis.ps1',
        'static/css/style.css',
        'static/js/dashboard.js',
        'templates/dashboard.html'
    ]
    
    base_path = os.path.join(os.path.dirname(__file__), '..')
    
    # 检查目录是否存在
    for dir_path in expected_dirs:
        full_path = os.path.join(base_path, dir_path)
        assert os.path.exists(full_path) and os.path.isdir(full_path), f"目录 {dir_path} 不存在"
    
    # 检查文件是否存在
    for file_path in expected_files:
        full_path = os.path.join(base_path, file_path)
        assert os.path.exists(full_path) and os.path.isfile(full_path), f"文件 {file_path} 不存在"
    
    print("所有目录和文件结构检查通过！")

if __name__ == "__main__":
    test_project_structure()
    print("项目结构测试完成。")