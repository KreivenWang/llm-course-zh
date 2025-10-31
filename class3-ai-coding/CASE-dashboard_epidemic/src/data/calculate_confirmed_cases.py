#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
计算香港各区疫情数据的每日新增与累计确诊数据
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import numpy as np


def load_and_process_data(file_path):
    """
    加载并处理疫情数据
    
    Args:
        file_path (str): Excel文件路径
    
    Returns:
        DataFrame: 处理后的数据
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 将日期列转换为datetime类型
        df['报告日期'] = pd.to_datetime(df['报告日期'])
        
        return df
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        return None


def calculate_daily_and_cumulative(df):
    """
    计算每日新增与累计确诊数据（全港总计）
    
    Args:
        df (DataFrame): 原始数据
    
    Returns:
        DataFrame: 每日新增与累计确诊数据
    """
    try:
        # 按日期分组，计算每日新增确诊和累计确诊（全港总计）
        daily_stats = df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'last'  # 假设每个区域的累计确诊在同一日期是一致的
        }).reset_index()
        
        # 对累计确诊按日期排序
        daily_stats = daily_stats.sort_values('报告日期')
        
        # 重新计算累计确诊（通过每日新增累加）
        daily_stats['累计确诊_计算值'] = daily_stats['新增确诊'].cumsum()
        
        return daily_stats
    except Exception as e:
        print(f"计算数据时发生错误: {e}")
        return None


def display_statistics(daily_stats):
    """
    显示统计数据
    
    Args:
        daily_stats (DataFrame): 每日统计的数据
    """
    print("=" * 50)
    print("香港疫情每日新增与累计确诊数据")
    print("=" * 50)
    
    # 显示前10天的数据
    print("\n前10天数据:")
    print(daily_stats.head(10).to_string(index=False))
    
    # 显示后10天的数据
    print("\n后10天数据:")
    print(daily_stats.tail(10).to_string(index=False))
    
    # 统计信息
    total_days = len(daily_stats)
    total_confirmed = daily_stats['新增确诊'].sum()
    max_daily_new = daily_stats['新增确诊'].max()
    max_daily_date = daily_stats.loc[daily_stats['新增确诊'].idxmax(), '报告日期']
    
    print(f"\n统计信息:")
    print(f"- 总记录天数: {total_days}")
    print(f"- 总确诊病例数: {total_confirmed}")
    print(f"- 单日最高新增: {max_daily_new} (日期: {max_daily_date.strftime('%Y-%m-%d')})")


def plot_trends(daily_stats):
    """
    绘制趋势图
    
    Args:
        daily_stats (DataFrame): 每日统计的数据
    """
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # 绘制每日新增确诊
        color = 'tab:red'
        ax1.set_xlabel('日期')
        ax1.set_ylabel('每日新增确诊', color=color)
        ax1.plot(daily_stats['报告日期'], daily_stats['新增确诊'], color=color, marker='o', markersize=3, linewidth=1, label='每日新增')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # 创建第二个y轴用于累计确诊
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('累计确诊', color=color)
        ax2.plot(daily_stats['报告日期'], daily_stats['累计确诊_计算值'], color=color, marker='s', markersize=3, linewidth=1, label='累计确诊')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # 格式化x轴日期
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        fig.autofmt_xdate()
        
        # 添加标题和网格
        plt.title('香港疫情每日新增与累计确诊趋势')
        ax1.grid(True, alpha=0.3)
        
        # 添加图例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        plt.savefig('confirmed_cases_trend.png', dpi=300, bbox_inches='tight')
        print("\n趋势图已保存为 'confirmed_cases_trend.png'")
        
        # 显示图表
        plt.show()
    except Exception as e:
        print(f"绘制图表时发生错误: {e}")


def main():
    """
    主函数
    """
    file_path = "香港各区疫情数据_20250322.xlsx"
    
    print("正在加载疫情数据...")
    df = load_and_process_data(file_path)
    
    if df is not None:
        print("正在计算每日新增与累计确诊数据...")
        daily_stats = calculate_daily_and_cumulative(df)
        
        if daily_stats is not None:
            display_statistics(daily_stats)
            
            # 绘制趋势图
            print("\n正在生成趋势图...")
            plot_trends(daily_stats)
        else:
            print("计算数据失败")
    else:
        print("加载数据失败")


if __name__ == "__main__":
    main()