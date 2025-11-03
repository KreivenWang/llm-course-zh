from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from services.chat_ollama_service import chat_ollama_service
from tesla_data_source import TeslaDataSource

# Create the LLM and the Agent
llm = chat_ollama_service.get_model()  # 使用ChatOllamaService提供的Ollama模型  

tesla_data_source = TeslaDataSource(llm)

# 使用 StructuredTool 正确定义工具
tools = [
    StructuredTool.from_function(
        func=tesla_data_source.find_product_description,
        name="find_product_description",
        description="根据产品名称查询产品的描述和定价信息"
    ),
    StructuredTool.from_function(
        func=tesla_data_source.find_company_info,
        name="find_company_info",
        description="查询公司的介绍信息和车型"
    )
]

# The recommended way to create and use an agent in V1
agent = create_agent(llm, tools)

# Invoke the agent (it handles the execution loop internally)
# result = agent.invoke({"messages": [{"role": "user", "content": "Model 3 多少钱?"}]})
result = agent.invoke({"messages": [{"role": "user", "content": "有哪些车的型号?"}]})

# 打印结果
print(result)
