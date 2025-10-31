import { formatNumber } from '../utils.js';

let regionalChart = null;

// 渲染区域分布图
function renderRegionalChart(data) {
    const chartDom = document.getElementById('regionalChart');
    
    if (regionalChart) {
        regionalChart.dispose();
    }
    
    regionalChart = echarts.init(chartDom);
    
    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            backgroundColor: 'rgba(17, 34, 64, 0.8)',
            borderColor: '#64ffda',
            borderWidth: 1,
            textStyle: {
                color: '#e6f1ff'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
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
        yAxis: {
            type: 'category',
            data: data.regional_data.regions,
            inverse: true,
            axisLine: {
                lineStyle: {
                    color: '#8892b0'
                }
            },
            axisLabel: {
                color: '#e6f1ff'
            }
        },
        series: [
            {
                name: '累计确诊',
                type: 'bar',
                barWidth: '60%',
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                        { offset: 0, color: '#64ffda' },
                        { offset: 1, color: '#4ecdc4' }
                    ])
                },
                data: data.regional_data.confirmed,
                label: {
                    show: true,
                    position: 'right',
                    color: '#e6f1ff',
                    formatter: function(params) {
                        return formatNumber(params.value);
                    }
                }
            }
        ]
    };
    
    regionalChart.setOption(option);
}

// 调整图表大小
function resizeRegionalChart() {
    if (regionalChart) {
        regionalChart.resize();
    }
}

export { renderRegionalChart, resizeRegionalChart };