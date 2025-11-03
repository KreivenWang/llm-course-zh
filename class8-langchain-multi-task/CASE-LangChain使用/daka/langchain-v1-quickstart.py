from langchain.agents import create_agent
from langchain.tools import tool # Example Tool
from services.chat_gemini_service import chat_gemini_service

# Define a tool
@tool
def get_current_weather(city: str) -> str:
    """Returns the current weather in a given city."""
    # ... implementation ...
    return f"The weather in {city} is sunny."

# Create the LLM and the Agent
llm = chat_gemini_service.get_model()  # 使用ChatGeminiService提供的Gemini模型  
tools = [get_current_weather]

# The recommended way to create and use an agent in V1
agent = create_agent(llm, tools)

# Invoke the agent (it handles the execution loop internally)
result = agent.invoke({"messages": [{"role": "user", "content": "What is the weather in Paris?"}]})

# 打印结果
print(result)
