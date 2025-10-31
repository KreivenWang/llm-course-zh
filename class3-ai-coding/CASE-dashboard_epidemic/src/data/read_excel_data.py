#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取香港各区疫情数据Excel文件的前20行数据
"""

import pandas as pd


def read_top_20_rows(file_path):
    """
    读取Excel文件的前20行数据
    
    Args:
        file_path (str): Excel文件路径
    
    Returns:
        DataFrame: 包含前20行数据的DataFrame
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 获取前20行数据
        top_20_rows = df.head(20)
        
        return top_20_rows
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def main():
    """
    主函数
    """
    file_path = "香港各区疫情数据_20250322.xlsx"
    
    print("正在读取Excel文件的前20行数据...")
    data = read_top_20_rows(file_path)
    
    if data is not None:
        print("\n前20行数据:")
        print(data)
        print(f"\n数据形状: {data.shape}")
    else:
        print("读取数据失败")


if __name__ == "__main__":
    main()