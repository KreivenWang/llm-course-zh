import { formatNumber } from '../utils.js';

let riskWarningChart = null;

// 渲染风险预警看板
function renderRiskWarningChart(data) {
    const chartDom = document.getElementById('riskWarningChart');
    
    if (riskWarningChart) {
        riskWarningChart.dispose();
    }
    
    riskWarningChart = echarts.init(chartDom);
    
    // 计算各区域的风险等级（基于累计确诊数）
    const regions = data.regional_data.regions;
    const confirmed = data.regional_data.confirmed;
    
    // 定义风险等级阈值
    const riskLevels = [
        { min: 0, max: 1000, label: '低风险', color: '#64ffda' },
        { min: 1001, max: 5000, label: '中风险', color: '#ffd166' },
        { min: 5001, max: 10000, label: '高风险', color: '#ff9f1c' },
        { min: 10001, max: Infinity, label: '极高风险', color: '#ff6b6b' }
    ];
    
    // 根据确诊数确定风险等级
    const riskData = regions.map((region, index) => {
        const count = confirmed[index] || 0;
        let level = riskLevels[0];
        for (let i = 0; i < riskLevels.length; i++) {
            if (count >= riskLevels[i].min && count <= riskLevels[i].max) {
                level = riskLevels[i];
                break;
            }
        }
        return {
            name: region,
            value: count,
            level: level.label,
            itemStyle: { color: level.color }
        };
    });
    
    const option = {
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(17, 34, 64, 0.8)',
            borderColor: '#64ffda',
            borderWidth: 1,
            textStyle: {
                color: '#e6f1ff'
            },
            formatter: function(params) {
                return `${params.name}<br/>累计确诊: ${formatNumber(params.value)}<br/>风险等级: ${params.data.level}`;
            }
        },
        series: [
            {
                name: '风险预警',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#0a192f',
                    borderWidth: 2
                },
                label: {
                    show: true,
                    formatter: '{b}\n{d}%',
                    color: '#e6f1ff'
                },
                labelLine: {
                    show: true
                },
                data: riskData
            }
        ]
    };
    
    riskWarningChart.setOption(option);
}

// 调整图表大小
function resizeRiskWarningChart() {
    if (riskWarningChart) {
        riskWarningChart.resize();
    }
}

export { renderRiskWarningChart, resizeRiskWarningChart };