from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
import os

# 修改为本地MySQL连接配置
db_user = "root"
db_password = "0099"
db_host = "localhost:3306"
# 假设数据库名为 test_db
db_name = "test_db"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
print(db.table_info)