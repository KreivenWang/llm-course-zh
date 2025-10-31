#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目启动脚本
用于简化项目的启动和运行过程
"""

import os
import sys
import subprocess
import argparse

def run_data_processing():
    """运行数据处理脚本"""
    print("正在运行数据处理脚本...")
    data_dir = os.path.join(os.path.dirname(__file__), 'src', 'data')
    
    # 运行数据读取脚本
    subprocess.run([sys.executable, 'read_excel_data.py'], cwd=data_dir)
    
    # 运行疫情计算脚本
    subprocess.run([sys.executable, 'calculate_confirmed_cases.py'], cwd=data_dir)
    
    print("数据处理完成！")

def run_visualization():
    """运行可视化脚本"""
    print("正在生成可视化图表...")
    viz_dir = os.path.join(os.path.dirname(__file__), 'src', 'visualization')
    
    # 运行高级可视化脚本
    subprocess.run([sys.executable, 'advanced_visualization.py'], cwd=viz_dir)
    
    print("可视化图表生成完成！")

def run_web_app():
    """运行Web应用"""
    print("正在启动Web应用...")
    app_dir = os.path.join(os.path.dirname(__file__), 'src', 'app')
    
    # 运行Flask应用
    subprocess.run([sys.executable, 'app.py'], cwd=app_dir)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='香港疫情数据可视化项目启动脚本')
    parser.add_argument('--process-data', action='store_true', help='运行数据处理')
    parser.add_argument('--visualize', action='store_true', help='生成可视化图表')
    parser.add_argument('--web', action='store_true', help='启动Web应用')
    parser.add_argument('--all', action='store_true', help='运行所有步骤')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，则运行所有步骤
    if not any([args.process_data, args.visualize, args.web, args.all]):
        args.all = True
    
    if args.all or args.process_data:
        run_data_processing()
    
    if args.all or args.visualize:
        run_visualization()
    
    if args.all or args.web:
        run_web_app()

if __name__ == "__main__":
    main()