import { formatNumber, regionNameMap, englishToChineseMap } from '../utils.js';

let hkMapChart = null;

// 渲染香港疫情地图
function renderHkMapChart(geoJson, data) {
    const chartDom = document.getElementById('hkMapChart');
    
    if (hkMapChart) {
        hkMapChart.dispose();
    }
    
    hkMapChart = echarts.init(chartDom);
    
    // 注册地图
    echarts.registerMap('HK', geoJson);
    
    // 获取区域名称和累计确诊数据
    const regions = data.regional_data.regions;
    const confirmed = data.regional_data.confirmed;
    
    // 构建地图数据，使用英文区域名称进行匹配
    const mapData = regions.map((region, index) => {
        const englishName = regionNameMap[region] || region;
        return {
            name: englishName,
            value: confirmed[index] || 0
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
                const chineseName = englishToChineseMap[params.name] || params.name;
                if (params.value) {
                    return `${chineseName}<br/>累计确诊: ${formatNumber(params.value)}`;
                }
                return `${chineseName}<br/>暂无数据`;
            }
        },
        visualMap: {
            min: 0,
            max: Math.max(...confirmed),
            inRange: {
                color: ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d']
            },
            textStyle: {
                color: '#e6f1ff'
            },
            calculable: true
        },
        series: [
            {
                name: '香港疫情地图',
                type: 'map',
                map: 'HK',
                roam: false,
                zoom: 1.2,
                selectedMode: false,
                label: {
                    show: true,
                    color: '#000',
                    fontSize: 10,
                    formatter: function(params) {
                        return englishToChineseMap[params.name] || params.name;
                    }
                },
                itemStyle: {
                    areaColor: '#eee',
                    borderColor: '#444',
                    borderWidth: 0.5
                },
                emphasis: {
                    label: {
                        show: true,
                        color: '#fff',
                        formatter: function(params) {
                            return englishToChineseMap[params.name] || params.name;
                        }
                    },
                    itemStyle: {
                        areaColor: '#2a77c9'
                    }
                },
                data: mapData
            }
        ]
    };
    
    hkMapChart.setOption(option);
}

// 调整图表大小
function resizeHkMapChart() {
    if (hkMapChart) {
        hkMapChart.resize();
    }
}

export { renderHkMapChart, resizeHkMapChart };