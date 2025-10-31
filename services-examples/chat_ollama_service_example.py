#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatOllama Service 使用示例
"""

from services.chat_ollama_service import chat_ollama_service


def example():
    """主函数 - 演示如何使用ChatOllama service"""
    # 获取service实例
    service = chat_ollama_service
    
    # 获取模型实例
    model = service.get_model()
    
    # 示例对话
    messages = [
        {"role": "system", "content": "你是一个 helpful 的助手，请用中文回答。"},
        {"role": "user", "content": "你好，你能告诉我你是谁吗？"}
    ]
    
    # 使用模型进行对话
    response = service.chat(messages)
    print("模型响应:")
    print(response.content)
    
    # 或者直接使用模型
    response2 = model.invoke("请用一句话介绍Python编程语言")
    print("\n直接调用模型的响应:")
    print(response2.content)
