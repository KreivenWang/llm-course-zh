// 导入数据管理模块
import { fetchDataAndRender } from './dataManager.js';

// 导入图表大小调整函数
import { resizeTrendChart } from './charts/trendChart.js';
import { resizeRegionalChart } from './charts/regionalChart.js';
import { resizeHkMapChart } from './charts/hkMapChart.js';
import { resizeRiskWarningChart } from './charts/riskWarningChart.js';
import { resizeTrendAnalysisChart } from './charts/trendAnalysisChart.js';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 首次加载数据
    fetchDataAndRender();
    
    // 每30秒刷新一次数据
    setInterval(fetchDataAndRender, 30000);
});

// 窗口大小改变时重新调整图表大小
window.addEventListener('resize', function() {
    resizeTrendChart();
    resizeRegionalChart();
    resizeHkMapChart();
    resizeRiskWarningChart();
    resizeTrendAnalysisChart();
});
