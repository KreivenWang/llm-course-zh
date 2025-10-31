#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGemini Service 单例模块
提供对Google Gemini模型的访问服务
"""

from langchain_google_genai import ChatGoogleGenerativeAI
import os


class ChatGeminiService:
    """ChatGemini Service 单例类"""
    _instance = None
    _initialized = False

    def __new__(cls):
        """创建单例实例"""
        if cls._instance is None:
            cls._instance = super(ChatGeminiService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化ChatGemini服务"""
        print("ChatGemini Service 初始化中...")
        if not self._initialized:
            # 检查环境变量中是否有Google API密钥
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("请设置GOOGLE_API_KEY环境变量")
            
            print(f"Google API Key 已设置，长度: {len(api_key)}")
            # 使用gemini-2.5-flash模型
            self.model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key
            )
            print("ChatGemini Service 初始化完成")
            self._initialized = True

    def get_model(self):
        """获取ChatGemini模型实例"""
        return self.model

    def chat(self, messages):
        """使用模型进行对话
        
        Args:
            messages: 对话消息列表
            
        Returns:
            模型响应
        """
        return self.model.invoke(messages)


# 创建全局单例实例
chat_gemini_service = ChatGeminiService()