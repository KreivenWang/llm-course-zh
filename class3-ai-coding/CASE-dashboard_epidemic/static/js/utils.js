// 格式化数字
function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
}

// 中英文区域名称映射
const regionNameMap = {
    '中西区': 'Central and Western',
    '湾仔区': 'Wan Chai',
    '东区': 'Eastern',
    '南区': 'Southern',
    '油尖旺区': 'Yau Tsim Mong',
    '深水埗区': 'Sham Shui Po',
    '九龙城区': 'Kowloon City',
    '黄大仙区': 'Wong Tai Sin',
    '观塘区': 'Kwun Tong',
    '葵青区': 'Kwai Tsing',
    '荃湾区': 'Tsuen Wan',
    '屯门区': 'Tuen Mun',
    '元朗区': 'Yuen Long',
    '北区': 'North',
    '大埔区': 'Tai Po',
    '沙田区': 'Sha Tin',
    '西贡区': 'Sai Kung',
    '离岛区': 'Islands'
};

// 英文到中文区域名称映射（反向映射）
const englishToChineseMap = {
    'Central and Western': '中西区',
    'Wan Chai': '湾仔区',
    'Eastern': '东区',
    'Southern': '南区',
    'Yau Tsim Mong': '油尖旺区',
    'Sham Shui Po': '深水埗区',
    'Kowloon City': '九龙城区',
    'Wong Tai Sin': '黄大仙区',
    'Kwun Tong': '观塘区',
    'Kwai Tsing': '葵青区',
    'Tsuen Wan': '荃湾区',
    'Tuen Mun': '屯门区',
    'Yuen Long': '元朗区',
    'North': '北区',
    'Tai Po': '大埔区',
    'Sha Tin': '沙田区',
    'Sai Kung': '西贡区',
    'Islands': '离岛区'
};

export { formatNumber, regionNameMap, englishToChineseMap };