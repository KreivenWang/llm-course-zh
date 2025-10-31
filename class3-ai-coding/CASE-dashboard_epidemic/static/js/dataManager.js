import { formatNumber } from './utils.js';
import { renderTrendChart } from './charts/trendChart.js';
import { renderRegionalChart } from './charts/regionalChart.js';
import { renderRiskWarningChart } from './charts/riskWarningChart.js';
import { renderTrendAnalysisChart } from './charts/trendAnalysisChart.js';
import { renderHkMapChart } from './charts/hkMapChart.js';

// 更新指标卡片
function updateMetrics(data) {
    document.getElementById('newConfirmed').textContent = formatNumber(data.latest_stats.new_confirmed);
    document.getElementById('cumulativeConfirmed').textContent = formatNumber(data.latest_stats.cumulative_confirmed);
    document.getElementById('existingConfirmed').textContent = formatNumber(data.latest_stats.existing_confirmed);
    document.getElementById('newRecovered').textContent = formatNumber(data.latest_stats.new_recovered);
    document.getElementById('newDeaths').textContent = formatNumber(data.latest_stats.new_deaths);
    
    // 更新时间
    document.getElementById('updateTime').textContent = `数据更新至：${data.latest_stats.latest_date}`;
}

// 获取数据并更新图表
async function fetchDataAndRender() {
    try {
        // 获取疫情数据
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.error) {
            console.error('数据获取失败:', data.error);
            return;
        }
        
        // 更新指标卡片
        updateMetrics(data);
        
        // 渲染图表
        renderTrendChart(data);
        renderRegionalChart(data);
        renderRiskWarningChart(data);
        renderTrendAnalysisChart(data);
        
        // 获取地理数据并渲染香港疫情地图
        const geoResponse = await fetch('/api/hongkong_geojson');
        const geoJson = await geoResponse.json();
        renderHkMapChart(geoJson, data);
    } catch (error) {
        console.error('获取数据时发生错误:', error);
    }
}

export { updateMetrics, fetchDataAndRender };