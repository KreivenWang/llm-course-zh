#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatOllama Service 单例模块
提供对Ollama模型的访问服务
"""

from langchain_ollama import ChatOllama


class ChatOllamaService:
    """ChatOllama Service 单例类"""
    _instance = None
    _initialized = False

    def __new__(cls):
        """创建单例实例"""
        if cls._instance is None:
            cls._instance = super(ChatOllamaService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化ChatOllama服务"""
        if not self._initialized:
            # 使用qwen3:14b模型
            self.model = ChatOllama(model="qwen3:14b")
            self._initialized = True

    def get_model(self):
        """获取ChatOllama模型实例"""
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
chat_ollama_service = ChatOllamaService()