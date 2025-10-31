import json
import os
import dashscope
from dashscope.api_entities.dashscope_response import Role

# 从环境变量中，获取 DASHSCOPE_API_KEY
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key

def get_weather_data(city: str, date_time: str):
    """
    一个虚假的天气查询函数，用于模拟高德 API 的调用结果。

    参数:
    city (str): 城市名称或城市编码。
    date_time (str): 查询的天气时间点或日期 (例如: "今天下午", "明天", "2024-10-01")。

    返回:
    dict: 包含虚假天气信息的字典。
    """
    print(f"\n[函数调用模拟] 正在查询 {city} 在 {date_time} 的天气...")

    # 简单地返回一个虚假的、但结构化的数据
    weather_info = {
        "city": city,
        "date_time": date_time,
        "weather_condition": "晴转多云",
        "temperature_range": "18°C ~ 25°C",
        "wind": "微风 2级",
        "humidity": "60%",
        "real_time_temperature": "22°C"
    }
    return weather_info


# 封装模型响应函数
def get_response(messages):
    try:
        print(f"正在调用API，消息数量: {len(messages)}")
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        print(f"API调用成功，状态码: {response.status_code}")
        return response
    except Exception as e:
        print(f"API调用出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"完整错误堆栈: {traceback.format_exc()}")
        return None


# 使用function call进行QA
def run_conversation(user_prompt):
    # 1. 定义系统指令
    system_prompt = (
        "你是一个专业的旅行天气助手。你的任务是根据用户的需求，查询出发地和目的地的具体时间段天气，并给出"
        "详细的穿衣建议和出行注意事项。如果用户提到两个地点或两个时间段，你可能需要多次调用函数。"
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

        print('response=', response)
        message = response.output.choices[0].message
        messages.append(message)
        print('message=', message)

        # 检查是否有函数调用 - 直接检查字典键
        message_dict = dict(message)
        if 'function_call' in message_dict and message_dict['function_call']:
            print("处理函数调用...")
            function_call = message_dict['function_call']
            tool_name = function_call['name']
            arguments = json.loads(function_call['arguments'])
            print('arguments=', arguments)
            
            # 执行函数
            tool_response = get_weather_data(
                city=arguments.get('city'),
                date_time=arguments.get('date_time'),
            )
            tool_info = {"role": "function", "name": tool_name, "content": json.dumps(tool_response, ensure_ascii=False)}
            print('tool_info=', tool_info)
            messages.append(tool_info)
            print('messages=', messages)
            
            # 继续循环，让模型处理函数结果
            continue
        else:
            # 没有函数调用，返回最终结果
            print('对话完成，最终响应:', response)
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
        print("最终结果:", result)
    else:
        print("对话执行失败")

