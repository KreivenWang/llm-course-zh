# 香港疫情数据可视化项目总结报告

## 项目概述

本项目旨在分析香港各区疫情数据，并通过多种可视化方式展示疫情发展趋势。项目包含数据处理、静态图表生成以及交互式可视化大屏。

## 项目结构优化

经过整理和优化，项目现在具有清晰的目录结构：

```
.
├── config/                 # 配置文件目录
├── docs/                   # 文档和输出图表目录
├── src/                    # 源代码目录
│   ├── app/                # Flask应用主文件
│   ├── data/               # 数据处理模块
│   ├── utils/              # 工具脚本
│   └── visualization/      # 高级可视化模块
├── static/                 # 静态资源目录
├── templates/              # HTML模板目录
├── tests/                  # 测试文件目录
├── requirements.txt        # Python依赖包列表
├── run_project.py          # 项目启动脚本
└── README.md               # 项目说明文件
```

## 主要功能模块

### 1. 数据处理模块 (src/data)
- `read_excel_data.py`: 读取并展示原始疫情数据
- `calculate_confirmed_cases.py`: 计算并生成疫情趋势数据
- `香港各区疫情数据_20250322.xlsx`: 原始数据文件

### 2. 可视化模块 (src/visualization)
- `advanced_visualization.py`: 生成多种类型的疫情数据图表
  - 每日新增确诊趋势图（含7日移动平均线）
  - 累计确诊趋势图
  - 每日新增与累计确诊对比图
  - 各区累计确诊对比柱状图

### 3. Web应用模块 (src/app)
- `app.py`: 基于Flask和ECharts构建的交互式疫情数据可视化大屏
- 实时展示关键疫情指标
- 包含趋势图和区域分布图

### 4. 工具脚本 (src/utils)
- `run_analysis.bat`: Windows批处理运行脚本
- `run_analysis.ps1`: PowerShell运行脚本

### 5. 静态资源 (static)
- `css/style.css`: 大屏样式文件
- `js/dashboard.js`: 大屏交互逻辑

### 6. 模板文件 (templates)
- `dashboard.html`: 大屏HTML模板

## 项目特点

1. **模块化设计**: 代码按功能模块组织，便于维护和扩展
2. **清晰的目录结构**: 每个目录都有明确的职责，便于团队协作
3. **配置管理**: 使用YAML格式的配置文件，便于修改项目参数
4. **自动化脚本**: 提供多种运行方式，包括一键启动脚本
5. **测试覆盖**: 包含项目结构测试，确保目录和文件完整性
6. **文档完整**: 提供详细的README和项目总结报告

## 使用方法

### 快速启动
```bash
python run_project.py
```

### 分步执行
```bash
# 只运行数据处理
python run_project.py --process-data

# 只生成可视化图表
python run_project.py --visualize

# 只启动Web应用
python run_project.py --web
```

## 输出结果

### 图表文件 (docs目录)
- `confirmed_cases_trend.png`: 疫情趋势图
- `daily_new_cases_trend.png`: 每日新增确诊趋势图
- `cumulative_cases_trend.png`: 累计确诊趋势图
- `daily_vs_cumulative_trend.png`: 每日新增与累计确诊对比图
- `regional_confirmed_cases.png`: 各区累计确诊对比柱状图

### Web仪表板
访问 `http://localhost:5000` 查看交互式可视化大屏

## 技术栈

- Python 3.x
- Flask: Web应用框架
- Pandas: 数据处理
- OpenPyXL: Excel文件读取
- Matplotlib: 基础图表绘制
- ECharts: 交互式图表展示

## 项目维护

1. **更新数据**: 替换Excel文件并重新运行数据处理脚本
2. **扩展功能**: 在相应模块中添加新功能
3. **修改配置**: 编辑`config/config.yaml`文件
4. **运行测试**: 执行`tests/test_project_structure.py`确保结构完整

## 总结

本项目通过合理的目录结构组织和模块化设计，实现了疫情数据的分析、可视化和交互展示。项目具有良好的可维护性和扩展性，便于后续功能添加和数据更新。