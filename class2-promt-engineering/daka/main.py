import requests
from daka.prompt import get_prompt
from daka.query import query_ollama

# 使用示例
print("流式响应：")

user_prompt = """
用typescript描述自定义请求
"""
prompt = get_prompt(user_prompt)
query_ollama(prompt, stream=True)