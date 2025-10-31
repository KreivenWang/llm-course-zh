#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask + ECharts 疫情数据可视化大屏
"""

import pandas as pd
from flask import Flask, jsonify, render_template
from datetime import datetime
import os
import json

# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, 
            static_folder=os.path.join(project_root, 'static'),
            template_folder=os.path.join(project_root, 'templates'))


def load_and_process_data():
    """
    加载并处理疫情数据
    
    Returns:
        dict: 处理后的数据
    """
    try:
        # 构建数据文件的完整路径
        data_file_path = os.path.join(project_root, 'src', 'data', '香港各区疫情数据_20250322.xlsx')
        # 读取Excel文件
        df = pd.read_excel(data_file_path)
        
        # 将日期列转换为datetime类型
        df['报告日期'] = pd.to_datetime(df['报告日期'])
        
        # 计算每日统计数据
        daily_stats = df.groupby('报告日期').agg({
            '新增确诊': 'sum',
            '累计确诊': 'last',
            '现存确诊': 'sum',
            '新增康复': 'sum',
            '累计康复': 'last',
            '新增死亡': 'sum',
            '累计死亡': 'last'
        }).reset_index()
        
        daily_stats = daily_stats.sort_values('报告日期')
        daily_stats['累计确诊_计算值'] = daily_stats['新增确诊'].cumsum()
        
        # 获取最新数据
        latest_data = daily_stats.iloc[-1]
        
        # 获取所有区域的累计确诊数据
        latest_date = df['报告日期'].max()
        latest_regional_data = df[df['报告日期'] == latest_date]
        # 按累计确诊数降序排列所有区域
        top_regions = latest_regional_data.sort_values('累计确诊', ascending=False)
        
        # 准备返回数据
        data = {
            'daily_stats': daily_stats,
            'latest_data': latest_data,
            'top_regions': top_regions
        }
        
        return data
    except Exception as e:
        print(f"加载数据时发生错误: {e}")
        return None


@app.route('/')
def index():
    """
    主页路由
    """
    return render_template('dashboard.html')


@app.route('/api/data')
def get_data():
    """
    获取疫情数据API
    """
    data = load_and_process_data()
    
    if data is None:
        return jsonify({'error': '数据加载失败'}), 500
    
    # 准备每日统计数据
    daily_stats = data['daily_stats']
    daily_data = {
        'dates': daily_stats['报告日期'].dt.strftime('%Y-%m-%d').tolist(),
        'new_confirmed': daily_stats['新增确诊'].tolist(),
        'cumulative_confirmed': daily_stats['累计确诊_计算值'].tolist(),
        'existing_confirmed': daily_stats['现存确诊'].tolist(),
        'new_recovered': daily_stats['新增康复'].tolist(),
        'new_deaths': daily_stats['新增死亡'].tolist()
    }
    
    # 准备最新数据
    latest_data = data['latest_data']
    latest_stats = {
        'latest_date': latest_data['报告日期'].strftime('%Y-%m-%d'),
        'new_confirmed': int(latest_data['新增确诊']),
        'cumulative_confirmed': int(latest_data['累计确诊_计算值']),
        'existing_confirmed': int(latest_data['现存确诊']),
        'new_recovered': int(latest_data['新增康复']),
        'cumulative_recovered': int(latest_data['累计康复']),
        'new_deaths': int(latest_data['新增死亡']),
        'cumulative_deaths': int(latest_data['累计死亡'])
    }
    
    # 准备区域数据，只取前10个区域
    top_regions = data['top_regions'].head(10)
    regional_data = {
        'regions': top_regions['地区名称'].tolist(),
        'confirmed': top_regions['累计确诊'].tolist()
    }
    
    return jsonify({
        'daily_data': daily_data,
        'latest_stats': latest_stats,
        'regional_data': regional_data
    })


@app.route('/api/hongkong_geojson')
def get_hongkong_geojson():
    """
    提供香港GeoJSON数据API
    """
    # 使用项目根目录下的map_data路径
    map_data_path = os.path.join(project_root, 'src', 'data', 'map_data', 'hongkong.json')
    if not os.path.exists(map_data_path):
        return jsonify({'error': '香港GeoJSON文件未找到'}), 404
    
    try:
        with open(map_data_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        return jsonify(geojson_data)
    except Exception as e:
        return jsonify({'error': f'读取GeoJSON文件失败: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)