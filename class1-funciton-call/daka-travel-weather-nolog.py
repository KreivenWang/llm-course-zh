import json
import os
import random
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

def get_weather_data(city: str, date_time: str):
    """
    一个虚假的天气查询函数，用于模拟高德 API 的调用结果。
    现在支持随机生成多种天气情况，更真实地模拟天气API的响应。

    参数:
    city (str): 城市名称或城市编码。
    date_time (str): 查询的天气时间点或日期 (例如: "今天下午", "明天", "2024-10-01")。

    返回:
    dict: 包含随机生成的虚假天气信息的字典。
    """
    # print(f"\n[函数调用模拟] 正在查询 {city} 在 {date_time} 的天气...")

    # 定义各种天气情况的数据池
    weather_conditions = [
        "晴", "多云", "阴", "小雨", "中雨", "大雨", "雷阵雨",
        # "雪", "小雪", "中雪", "大雪", "雾", "霾", "沙尘暴"
    ]
    
    # 根据城市和季节调整温度范围
    city_temp_ranges = {
        "北京": {"min": -5, "max": 35},
        "上海": {"min": 0, "max": 38},
        "广州": {"min": 8, "max": 40},
        "深圳": {"min": 10, "max": 38},
        "西安": {"min": -3, "max": 36},
        "香港": {"min": 12, "max": 35},
        "成都": {"min": 2, "max": 32},
        "杭州": {"min": 1, "max": 37},
        "南京": {"min": -2, "max": 36},
        "武汉": {"min": 0, "max": 38}
    }
    
    # 风力等级
    wind_levels = ["无风", "微风 1级", "微风 2级", "轻风 3级", "和风 4级", "清风 5级", "强风 6级", "疾风 7级"]
    
    # 湿度范围
    humidity_ranges = [(30, 50), (50, 70), (70, 85), (85, 95)]
    
    # 随机选择天气情况
    weather_condition = random.choice(weather_conditions)
    
    # 根据城市获取温度范围，如果没有则使用默认范围
    temp_range = city_temp_ranges.get(city, {"min": 0, "max": 30})
    min_temp = random.randint(temp_range["min"], temp_range["max"] - 10)
    max_temp = random.randint(min_temp + 5, temp_range["max"])
    
    # 随机选择风力
    wind = random.choice(wind_levels)
    
    # 随机选择湿度
    humidity_range = random.choice(humidity_ranges)
    humidity = f"{random.randint(humidity_range[0], humidity_range[1])}%"
    
    # 实时温度在最小和最大温度之间
    real_time_temp = random.randint(min_temp, max_temp)
    
    # 根据天气情况调整一些参数
    if "雨" in weather_condition or "雪" in weather_condition:
        # 下雨下雪时湿度通常较高
        humidity = f"{random.randint(70, 95)}%"
        wind = random.choice(["微风 1级", "微风 2级", "轻风 3级", "和风 4级"])
    elif "晴" in weather_condition:
        # 晴天时湿度通常较低
        humidity = f"{random.randint(30, 60)}%"
    elif "雾" in weather_condition or "霾" in weather_condition:
        # 雾霾天气湿度高，风力小
        humidity = f"{random.randint(80, 95)}%"
        wind = random.choice(["无风", "微风 1级", "微风 2级"])
    
    # 构建天气信息
    weather_info = {
        "city": city,
        "date_time": date_time,
        "weather_condition": weather_condition,
        "temperature_range": f"{min_temp}°C ~ {max_temp}°C",
        "wind": wind,
        "humidity": humidity,
        "real_time_temperature": f"{real_time_temp}°C"
    }
    
    return weather_info


# 封装模型响应函数
def get_response(messages):
    try:
        # print(f"正在调用API，消息数量: {len(messages)}")
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        # print(f"API调用成功，状态码: {response.status_code}")
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"完整错误堆栈: {traceback.format_exc()}")
        return None


# 使用function call进行QA
def run_conversation(user_prompt):
    print(f"用户: {user_prompt}")

    # 1. 定义系统指令
    system_prompt = (
        "你是一个专业的旅行天气助手。你的任务是根据用户的需求，查询出发地和目的地的具体时间段天气。"
        "结果以MD表格的形式展示，每个时间段包括详细的穿衣建议，出行注意事项，必备物品。"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 开始循环处理对话
    while True:
        # 获取模型响应
        response = get_response(messages)
        if not response or not response.output:
            print("获取响应失败")
            return None

        # print('response=', response)
        message = response.output.choices[0].message
        messages.append(message)
        # print('message=', message)

        # 检查是否有函数调用 - 直接检查字典键
        message_dict = dict(message)
        if 'function_call' in message_dict and message_dict['function_call']:
            # print("处理函数调用...")
            function_call = message_dict['function_call']
            tool_name = function_call['name']
            arguments = json.loads(function_call['arguments'])
            # print('arguments=', arguments)
            
            # 执行函数
            tool_response = get_weather_data(
                city=arguments.get('city'),
                date_time=arguments.get('date_time'),
            )
            tool_info = {"role": "function", "name": tool_name, "content": json.dumps(tool_response, ensure_ascii=False)}
            # print('tool_info=', tool_info)
            messages.append(tool_info)
            # print('messages=', messages)
            
            # 继续循环，让模型处理函数结果
            continue
        else:
            return message


functions = [
    {
        "name": "get_weather_data",
        "description": "用于查询指定城市和时间段的详细天气情况。当你需要知道具体天气数据来回答问题或给出建议时，请调用此函数。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "需要查询的城市名称，如 '北京', '上海' 等。"
                },
                "date_time": {
                    "type": "string",
                    "description": "查询的具体时间段或日期，如 '今天上午', '明天', '2024-10-01' 等。"
                }
            },
            "required": ["city", "date_time"]
        }
    }
]

if __name__ == "__main__":   
    # query = "我明天从香港到西安，早上8点出发。"
    query = "我明天从香港到西安早上8点出发，呆一天，大后天回。"
    result = run_conversation(query)
    if result:
        print("最终结果:", result.content)
    else:
        print("对话执行失败")

