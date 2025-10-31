#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGemini Service 使用示例
"""
print("ChatGemini Service 示例启动中...")
from services.chat_gemini_service import chat_gemini_service


def main():
    """主函数 - 演示如何使用ChatGemini service"""
    # 获取service实例
    service = chat_gemini_service
    
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


if __name__ == "__main__":
    print("ChatGemini Service 示例开始运行...")
    main()