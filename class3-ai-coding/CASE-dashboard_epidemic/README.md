# 香港疫情数据可视化仪表板

## 项目结构

```
.
├── config/                 # 配置文件目录
│   └── config.yaml         # 项目配置文件
├── docs/                   # 文档和输出图表目录
│   ├── confirmed_cases_trend.png
│   ├── cumulative_cases_trend.png
│   ├── daily_new_cases_trend.png
│   ├── daily_vs_cumulative_trend.png
│   └── regional_confirmed_cases.png
├── src/                    # 源代码目录
│   ├── app/                # Flask应用主文件
│   │   └── app.py
│   ├── data/               # 数据处理模块
│   │   ├── calculate_confirmed_cases.py
│   │   ├── read_excel_data.py
│   │   ├── 香港各区疫情数据_20250322.xlsx
│   │   └── map_data/
│   │       └── hongkong.json
│   ├── utils/              # 工具脚本
│   │   ├── run_analysis.bat
│   │   └── run_analysis.ps1
│   └── visualization/      # 高级可视化模块
│       └── advanced_visualization.py
├── static/                 # 静态资源目录
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
├── templates/              # HTML模板目录
│   └── dashboard.html
├── tests/                  # 测试文件目录
├── requirements.txt        # Python依赖包列表
├── run_project.py          # 项目启动脚本
└── README.md               # 项目说明文件
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

### 方法一：使用项目启动脚本（推荐）
```bash
# 运行所有步骤（数据处理、可视化、启动Web应用）
python run_project.py

# 只运行数据处理
python run_project.py --process-data

# 只生成可视化图表
python run_project.py --visualize

# 只启动Web应用
python run_project.py --web

# 运行所有步骤（与不带参数相同）
python run_project.py --all
```

### 方法二：使用Python直接运行
```bash
cd src/app
python app.py
```

### 方法三：使用批处理脚本运行
```bash
cd src/utils
./run_analysis.bat
```

### 方法四：使用PowerShell脚本运行
```bash
cd src/utils
./run_analysis.ps1
```

## 生成图表

要重新生成图表，请运行：
```bash
cd src/data
python read_excel_data.py
python calculate_confirmed_cases.py
```

或者使用高级可视化脚本：
```bash
cd src/visualization
python advanced_visualization.py
```

## 查看结果

1. Web仪表板：运行应用后访问 http://localhost:5000
2. 图表文件：在docs/目录中查看生成的PNG文件