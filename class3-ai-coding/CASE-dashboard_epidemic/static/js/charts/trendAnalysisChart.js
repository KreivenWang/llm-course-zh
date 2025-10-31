import { formatNumber } from '../utils.js';

let trendAnalysisChart = null;

// 渲染趋势分析图
function renderTrendAnalysisChart(data) {
    const chartDom = document.getElementById('trendAnalysisChart');
    
    if (trendAnalysisChart) {
        trendAnalysisChart.dispose();
    }
    
    trendAnalysisChart = echarts.init(chartDom);
    
    // 计算7日移动平均
    const dates = data.daily_data.dates;
    const newConfirmed = data.daily_data.new_confirmed;
    const movingAverage7 = [];
    
    for (let i = 0; i < newConfirmed.length; i++) {
        if (i < 6) {
            movingAverage7.push(null); // 前6天无法计算7日平均
        } else {
            const sum = newConfirmed.slice(i - 6, i + 1).reduce((a, b) => a + b, 0);
            movingAverage7.push(Math.round(sum / 7));
        }
    }
    
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
            data: ['每日新增', '7日移动平均'],
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
            data: dates,
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
        yAxis: {
            type: 'value',
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
            }
        },
        series: [
            {
                name: '每日新增',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 3,
                lineStyle: {
                    width: 1,
                    color: '#ff6b6b'
                },
                itemStyle: {
                    color: '#ff6b6b'
                },
                areaStyle: {
                    opacity: 0.1,
                    color: '#ff6b6b'
                },
                data: newConfirmed
            },
            {
                name: '7日移动平均',
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 4,
                lineStyle: {
                    width: 3,
                    color: '#4ecdc4'
                },
                itemStyle: {
                    color: '#4ecdc4'
                },
                data: movingAverage7
            }
        ]
    };
    
    trendAnalysisChart.setOption(option);
}

// 调整图表大小
function resizeTrendAnalysisChart() {
    if (trendAnalysisChart) {
        trendAnalysisChart.resize();
    }
}

export { renderTrendAnalysisChart, resizeTrendAnalysisChart };