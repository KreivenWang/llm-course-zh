from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.callbacks.manager import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from typing import List, Tuple
import os
import pickle
from metadata_store.metadata_store import MetadataStore
import time

def query_with_accuracy_and_metadata_single(knowledge_base, query: str, k: int = 3):
    """
    执行查询，展示匹配准确度和元数据
    
    参数:
        knowledge_base: 知识库对象
        query: 查询字符串
        k: 返回的文档数量
    """
    print(f"\n=== 查询: {query} ===")
    start_time = time.time()
    
    # 执行相似度搜索，找到与查询相关的文档
    docs_with_scores = knowledge_base.similarity_search_with_score(query, k=k)
    
    search_time = time.time() - start_time
    print(f"搜索完成，耗时: {search_time:.3f} 秒")
    print(f"找到 {len(docs_with_scores)} 个相关文档片段")
    
    # 准备文档上下文和展示准确度信息
    context_parts = []
    print("\n--- 匹配准确度和元数据详情 ---")
    
    # 首先展示每个文档片段的详细信息
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        content = getattr(doc, "page_content", "")
        source_page = knowledge_base.page_info.get(content.strip(), "未知")
        
        # 计算相似度百分比（分数越小越相似，所以我们用一个转换公式）
        # FAISS的相似度分数通常是距离，分数越小表示越相似
        max_score = max(doc_tuple[1] for doc_tuple in docs_with_scores) if docs_with_scores else 1  # 获取最大分数用于归一化
        similarity_percentage = max(0, min(100, (1 - score / (max_score + 0.001)) * 100))
        
        print(f"\n文档片段 {i}:")
        print(f"  相似度得分: {score:.4f}")
        print(f"  估算相似度: {similarity_percentage:.2f}%")
        print(f"  来源页码: {source_page}")
        # 只显示第一行，如果超过50个字符则截断并显示...
        first_line = content.split('\n')[0] if content.split('\n') else ""
        preview = first_line[:50] + "..." if len(first_line) > 50 else first_line
        print(f"  内容预览: {preview}")
        
        # 添加到上下文，以便AI能参考这些内容，并包含元数据信息
        context_parts.append(f"文档片段 {i} (相似度: {similarity_percentage:.2f}%, 来源页码: {source_page}): {content}")
    
    # 构建最终的上下文
    context = "\\n\\n".join(context_parts)
    
    # 加载LLM
    llm = ChatOllama(model="qwen3:14b")
    
    # 创建提示模板，明确指示AI只基于提供的上下文进行回答
    template = """请仅基于以下上下文中的信息回答问题，不要使用上下文之外的知识：
    {context}
    
    问题: {question}
    
    请在回答中引用相关文档片段的来源页码。
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 使用回调函数跟踪API调用成本
    with get_openai_callback() as cost:
        # 直接使用格式化的上下文和查询调用llm
        messages = prompt.invoke({"context": context, "question": query})
        response = llm.invoke(messages)
        print(f"\n查询已处理。成本: {cost}")
        # 如果response是AIMessage对象，获取内容部分
        if hasattr(response, 'content'):
            print(f"AI回答: {response.content}")
        else:
            print(f"AI回答: {response}")
            
    print(f"\n来源页码: {[knowledge_base.page_info.get(getattr(doc[0], 'page_content', '').strip(), '未知') for doc in docs_with_scores]}")
    
    # 获取存储的元数据
    metadata_store = MetadataStore()
    all_metadata = metadata_store.list_all_metadata()
    if all_metadata:
        print(f"\n--- 文档元数据 ---")
        for metadata in all_metadata:
            print(f"文档ID: {metadata.get('doc_id', 'Unknown')}")
            print(f"源文件: {metadata.get('source_file', 'N/A')}")
            print(f"分块数量: {metadata.get('chunk_count', 'N/A')}")
            print(f"文本长度: {metadata.get('text_length', 'N/A')}")
            print(f"页数: {metadata.get('page_count', 'N/A')}")
            print(f"嵌入模型: {metadata.get('embedding_model', 'N/A')}")
            print(f"保存路径: {metadata.get('save_path', 'N/A')}")
            print(f"创建时间: {metadata.get('created_at', 'N/A')}")
            print(f"更新时间: {metadata.get('updated_at', 'N/A')}")


# 从向量数据库加载
embeddings = OllamaEmbeddings(model="qwen3-embedding:4b")
knowledgeBase = FAISS.load_local("./vector_db", embeddings, allow_dangerous_deserialization=True)

# 加载页码信息
page_info_path = os.path.join("./vector_db", "page_info.pkl")
if os.path.exists(page_info_path):
    with open(page_info_path, "rb") as f:
        page_info = pickle.load(f)
    knowledgeBase.page_info = page_info
    print("页码信息已加载。")

# 执行单个查询示例
query_with_accuracy_and_metadata_single(knowledgeBase, "客户经理被投诉了，投诉一次扣多少分")