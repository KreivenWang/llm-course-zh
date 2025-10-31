import { formatNumber } from '../utils.js';

let trendChart = null;

// 渲染趋势图
function renderTrendChart(data) {
    const chartDom = document.getElementById('trendChart');
    
    if (trendChart) {
        trendChart.dispose();
    }
    
    trendChart = echarts.init(chartDom);
    
    // 计算新增确诊和现存确诊的最大值，用于设置左侧Y轴范围
    const newConfirmedMax = Math.max(...data.daily_data.new_confirmed);
    const existingConfirmedMax = Math.max(...data.daily_data.existing_confirmed);
    const newExistingMax = Math.max(newConfirmedMax, existingConfirmedMax);
    
    // 计算累计确诊的最大值，用于设置右侧Y轴范围
    const cumulativeMax = Math.max(...data.daily_data.cumulative_confirmed);
    
    // 计算Y轴上限，使其显示为整数
    const newExistingMaxYAxis = Math.ceil(newExistingMax * 1.1 / 10000) * 10000;
    const cumulativeMaxYAxis = Math.ceil(cumulativeMax * 1.1 / 10000) * 10000;

    const option = {
        tooltip: {
            trigger: 'axis',
            backgroundColor: 'rgba(17, 34, 64, 0.8)',
            borderColor: '#64ffda',
            borderWidth: 1,
            textStyle: {
                color: '#e6f1ff'
            }
        },
        legend: {
            data: ['新增确诊', '累计确诊', '现存确诊'],
            textStyle: {
                color: '#e6f1ff'
            },
            top: 10
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.daily_data.dates,
            axisLine: {
                lineStyle: {
                    color: '#8892b0'
                }
            },
            axisLabel: {
                color: '#8892b0',
                rotate: 45,
                // 调整横坐标显示密度，每隔7个显示一个标签
                interval: 6
            }
        },
        yAxis: [
            {
                type: 'value',
                name: '新增/现存确诊',
                nameTextStyle: {
                    color: '#e6f1ff'
                },
                axisLine: {
                    lineStyle: {
                        color: '#8892b0'
                    }
                },
                axisLabel: {
                    color: '#8892b0'
                },
                splitLine: {
                    lineStyle: {
                        color: 'rgba(136, 146, 176, 0.2)'
                    }
                },
                // 设置合适的刻度范围，使新增和现存确诊更清晰可见
                min: 0,
                max: newExistingMaxYAxis
            },
            {
                type: 'value',
                name: '累计确诊',
                nameTextStyle: {
                    color: '#e6f1ff'
                },
                axisLine: {
                    lineStyle: {
                        color: '#8892b0'
                    }
                },
                axisLabel: {
                    color: '#8892b0'
                },
                splitLine: {
                    show: false
                },
                // 设置合适的刻度范围，使累计确诊更清晰可见
                min: 0,
                max: cumulativeMaxYAxis
            }
        ],
        series: [
            {
                name: '新增确诊',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 4,
                lineStyle: {
                    width: 2,
                    color: '#ff6b6b'
                },
                itemStyle: {
                    color: '#ff6b6b'
                },
                areaStyle: {
                    opacity: 0.1,
                    color: '#ff6b6b'
                },
                data: data.daily_data.new_confirmed,
                yAxisIndex: 0  // 使用左侧Y轴
            },
            {
                name: '现存确诊',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 4,
                lineStyle: {
                    width: 2,
                    color: '#ffd166'
                },
                itemStyle: {
                    color: '#ffd166'
                },
                areaStyle: {
                    opacity: 0.1,
                    color: '#ffd166'
                },
                data: data.daily_data.existing_confirmed,
                yAxisIndex: 0  // 使用左侧Y轴
            },
            {
                name: '累计确诊',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 4,
                lineStyle: {
                    width: 2,
                    color: '#4ecdc4'
                },
                itemStyle: {
                    color: '#4ecdc4'
                },
                areaStyle: {
                    opacity: 0.1,
                    color: '#4ecdc4'
                },
                data: data.daily_data.cumulative_confirmed,
                yAxisIndex: 1  // 使用右侧Y轴
            }
        ]
    };
    
    trendChart.setOption(option);
}

// 调整图表大小
function resizeTrendChart() {
    if (trendChart) {
        trendChart.resize();
    }
}

export { renderTrendChart, resizeTrendChart };