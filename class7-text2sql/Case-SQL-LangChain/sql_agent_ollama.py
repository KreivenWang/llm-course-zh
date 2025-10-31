#!/usr/bin/env python
# coding: utf-8

# In[6]:


"""
使用Ollama进行本地MySQL数据表的查询
"""

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_ollama import ChatOllama  # 使用Ollama的Chat模型

# 修改为本地MySQL连接配置
db_user = "root"
db_password = "0099"
db_host = "localhost:3306"
db_name = "test_db"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
print("数据库连接成功:")
print(db)

# 创建Ollama语言模型实例
# 默认连接本地运行的Ollama服务 (http://localhost:11434)
# 你可能需要根据自己的情况调整模型名称，比如 "llama3", "mistral", "gemma" 等
llm = ChatOllama(
    model="qwen3:14b",  # 可以根据需要更改模型名称
    temperature=0.01,
)

print("Ollama模型连接成功!")

# 创建数据库工具包
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# 创建SQL智能体
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

print("SQL智能体创建成功!")

# 示例查询
print("\n开始执行查询...")

# Task: 描述数据表
print("\n查询: 描述与订单相关的表及其关系")
try:
    result = agent_executor.run("描述与订单相关的表及其关系")
    print(f"结果: {result}")
except Exception as e:
    print(f"查询执行失败: {e}")

# 额外的查询，适用于我们的本地数据库
print("\n查询: 找出订单金额最高的前5个订单")
try:
    result = agent_executor.run("找出订单金额最高的前5个订单")
    print(f"结果: {result}")
except Exception as e:
    print(f"查询执行失败: {e}")

print("\n查询: 找出ID为1的客户的所有订单")
try:
    result = agent_executor.run("找出ID为1的客户的所有订单")
    print(f"结果: {result}")
except Exception as e:
    print(f"查询执行失败: {e}")
# %%
