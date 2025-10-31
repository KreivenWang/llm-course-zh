#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高级疫情数据可视化脚本
提供多种图表类型展示香港疫情数据
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from matplotlib.font_manager import FontProperties


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


def plot_daily_new_cases(daily_stats):
    """
    绘制每日新增确诊折线图
    
    Args:
        daily_stats (DataFrame): 每日统计数据
    """
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # 绘制折线图
    ax.plot(daily_stats['报告日期'], daily_stats['新增确诊'], 
            color='#e74c3c', linewidth=1.5, marker='o', markersize=3)
    
    # 设置标题和标签
    ax.set_title('香港疫情每日新增确诊病例趋势', fontsize=16, pad=20)
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('新增确诊病例数', fontsize=12, color='#e74c3c')
    
    # 格式化x轴日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    # 设置y轴颜色
    ax.tick_params(axis='y', labelcolor='#e74c3c')
    
    # 添加移动平均线
    daily_stats['新增确诊_7日均值'] = daily_stats['新增确诊'].rolling(window=7).mean()
    ax.plot(daily_stats['报告日期'], daily_stats['新增确诊_7日均值'], 
            color='#3498db', linewidth=2, label='7日移动平均')
    
    # 添加图例
    ax.legend(loc='upper left')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('daily_new_cases_trend.png', dpi=300, bbox_inches='tight')
    print("每日新增确诊趋势图已保存为 'daily_new_cases_trend.png'")
    
    # 显示图表
    plt.show()


def plot_cumulative_cases(daily_stats):
    """
    绘制累计确诊折线图
    
    Args:
        daily_stats (DataFrame): 每日统计数据
    """
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # 绘制累计确诊折线图
    ax.plot(daily_stats['报告日期'], daily_stats['累计确诊_计算值'], 
            color='#3498db', linewidth=2, marker='s', markersize=3)
    
    # 设置标题和标签
    ax.set_title('香港疫情累计确诊病例趋势', fontsize=16, pad=20)
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('累计确诊病例数', fontsize=12, color='#3498db')
    
    # 格式化x轴日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    # 设置y轴颜色
    ax.tick_params(axis='y', labelcolor='#3498db')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('cumulative_cases_trend.png', dpi=300, bbox_inches='tight')
    print("累计确诊趋势图已保存为 'cumulative_cases_trend.png'")
    
    # 显示图表
    plt.show()


def plot_daily_vs_cumulative(daily_stats):
    """
    绘制每日新增与累计确诊对比双轴图
    
    Args:
        daily_stats (DataFrame): 每日统计数据
    """
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形
    fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # 绘制每日新增确诊
    color = '#e74c3c'
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('每日新增确诊病例', color=color, fontsize=12)
    ax1.plot(daily_stats['报告日期'], daily_stats['新增确诊'], 
             color=color, linewidth=1, marker='o', markersize=2, alpha=0.7, label='每日新增')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # 创建第二个y轴用于累计确诊
    ax2 = ax1.twinx()
    color = '#3498db'
    ax2.set_ylabel('累计确诊病例', color=color, fontsize=12)
    ax2.plot(daily_stats['报告日期'], daily_stats['累计确诊_计算值'], 
             color=color, linewidth=2, marker='s', markersize=2, label='累计确诊')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # 格式化x轴日期
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    
    # 添加标题和网格
    plt.title('香港疫情每日新增与累计确诊病例对比', fontsize=16, pad=20)
    ax1.grid(True, alpha=0.3)
    
    # 添加图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('daily_vs_cumulative_trend.png', dpi=300, bbox_inches='tight')
    print("每日新增与累计确诊对比图已保存为 'daily_vs_cumulative_trend.png'")
    
    # 显示图表
    plt.show()


def plot_regional_comparison(df):
    """
    绘制各区域累计确诊对比图
    
    Args:
        df (DataFrame): 原始数据
    """
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 获取最新的日期
    latest_date = df['报告日期'].max()
    
    # 筛选最新日期的数据
    latest_data = df[df['报告日期'] == latest_date]
    
    # 按累计确诊数排序，取前10个区域
    top_regions = latest_data.nlargest(10, '累计确诊')
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘制柱状图
    bars = ax.bar(range(len(top_regions)), top_regions['累计确诊'], 
                  color=plt.cm.viridis(np.linspace(0, 1, len(top_regions))))
    
    # 设置标题和标签
    ax.set_title(f'截至{latest_date.strftime("%Y-%m-%d")}香港各区累计确诊病例数TOP10', fontsize=16, pad=20)
    ax.set_xlabel('区域', fontsize=12)
    ax.set_ylabel('累计确诊病例数', fontsize=12)
    
    # 设置x轴标签
    ax.set_xticks(range(len(top_regions)))
    ax.set_xticklabels(top_regions['地区名称'], rotation=45, ha='right')
    
    # 在柱状图上添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('regional_confirmed_cases.png', dpi=300, bbox_inches='tight')
    print("各区累计确诊对比图已保存为 'regional_confirmed_cases.png'")
    
    # 显示图表
    plt.show()


def main():
    """
    主函数
    """
    file_path = "香港各区疫情数据_20250322.xlsx"
    
    print("正在加载疫情数据...")
    df = load_and_process_data(file_path)
    
    if df is not None:
        print("正在处理数据...")
        
        # 计算每日统计数据
        daily_stats = df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'last'
        }).reset_index()
        
        daily_stats = daily_stats.sort_values('报告日期')
        daily_stats['累计确诊_计算值'] = daily_stats['新增确诊'].cumsum()
        
        print("正在生成各种可视化图表...")
        
        # 生成不同的图表
        plot_daily_new_cases(daily_stats)
        plot_cumulative_cases(daily_stats)
        plot_daily_vs_cumulative(daily_stats)
        plot_regional_comparison(df)
        
        print("\n所有图表已生成完成！")
    else:
        print("加载数据失败")


if __name__ == "__main__":
    main()