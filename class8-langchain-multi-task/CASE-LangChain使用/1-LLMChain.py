from langchain_core.prompts import PromptTemplate
# from langchain_community.llms import Tongyi  # 导入通义千问Tongyi模型
# import dashscope
# import os

# # 从环境变量获取 dashscope 的 API Key
# api_key = os.environ.get('DASHSCOPE_API_KEY')
# dashscope.api_key = api_key
 
# # 加载 Tongyi 模型
# llm = Tongyi(model_name="qwen-turbo", dashscope_api_key=api_key)  # 使用通义千问qwen-turbo模型

from services.chat_ollama_service import chat_ollama_service

# 获取Ollama模型实例
llm = chat_ollama_service.get_model()

# 创建Prompt Template
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}? Please respond in chinese. Reason your answer.",
)

# 新推荐用法：将 prompt 和 llm 组合成一个"可运行序列"
chain = prompt | llm

# 使用 invoke 方法传入输入
result1 = chain.invoke({"product": "colorful socks"})
print(result1.content)

result2 = chain.invoke({"product": "肉鸽游戏"})
print(result2.content)

