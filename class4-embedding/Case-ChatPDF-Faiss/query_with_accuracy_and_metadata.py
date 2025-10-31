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

def extract_text_with_page_numbers(pdf) -> Tuple[str, List[int]]:
    """
    从PDF中提取文本并记录每行文本对应的页码
    
    参数:
        pdf: PDF文件对象
    
    返回:
        text: 提取的文本内容
        page_numbers: 每行文本对应的页码列表
    """
    text = ""
    page_numbers = []

    for page_number, page in enumerate(pdf.pages, start=1):
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
            page_numbers.extend([page_number] * len(extracted_text.split("\n")))

    return text, page_numbers

def process_text_with_splitter(text: str, page_numbers: List[int], save_path: str = None, pdf_path: str = None) -> FAISS:
    """
    处理文本并创建向量存储
    
    参数:
        text: 提取的文本内容
        page_numbers: 每行文本对应的页码列表
        save_path: 可选，保存向量数据库的路径
        pdf_path: 源PDF文件路径
    
    返回:
        knowledgeBase: 基于FAISS的向量存储对象
    """
    # 创建文本分割器，用于将长文本分割成小块
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # 分割文本
    chunks = text_splitter.split_text(text)
    print(f"文本被分割成 {len(chunks)} 个块。")
        
    # 创建嵌入模型
    embeddings = OllamaEmbeddings(
        model="qwen3-embedding:4b"
    )
    
    # 从文本块创建知识库
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    print("已从文本块创建知识库。")
    
    # 改进：存储每个文本块对应的页码信息
    # 创建原始文本的行列表和对应的页码列表
    lines = text.split("\n")
    
    # 为每个chunk找到最匹配的页码
    page_info = {}
    for chunk in chunks:
        # 查找chunk在原始文本中的开始位置
        start_idx = text.find(chunk[:100])  # 使用chunk的前100个字符作为定位点
        if start_idx == -1:
            # 如果找不到精确匹配，则使用模糊匹配
            for i, line in enumerate(lines):
                if chunk.startswith(line[:min(50, len(line))]):
                    start_idx = i
                    break
            
            # 如果仍然找不到，尝试另一种匹配方式
            if start_idx == -1:
                for i, line in enumerate(lines):
                    if line and line in chunk:
                        start_idx = text.find(line)
                        break
        
        # 如果找到了起始位置，确定对应的页码
        if start_idx != -1:
            # 计算这个位置对应原文中的哪一行
            line_count = text[:start_idx].count("\n")
            # 确保不超出页码列表长度
            if line_count < len(page_numbers):
                page_info[chunk] = page_numbers[line_count]
            else:
                # 如果超出范围，使用最后一个页码
                page_info[chunk] = page_numbers[-1] if page_numbers else 1
        else:
            # 如果无法匹配，使用默认页码-1（这里应该根据实际情况设置一个合理的默认值）
            page_info[chunk] = -1
    
    knowledgeBase.page_info = page_info
    
    # 如果提供了保存路径，则保存向量数据库和页码信息
    if save_path:
        # 确保目录存在
        os.makedirs(save_path, exist_ok=True)
        
        # 保存FAISS向量数据库
        knowledgeBase.save_local(save_path)
        print(f"向量数据库已保存到: {save_path}")
        
        # 保存页码信息到同一目录
        with open(os.path.join(save_path, "page_info.pkl"), "wb") as f:
            pickle.dump(page_info, f)
        print(f"页码信息已保存到: {os.path.join(save_path, 'page_info.pkl')}")
        
        # 使用元数据存储管理器保存文档元数据
        metadata_store = MetadataStore()
        doc_id = os.path.basename(pdf_path) if pdf_path else "unknown_pdf"
        
        # 创建文档元数据
        doc_metadata = {
            "doc_id": doc_id,
            "source_file": pdf_path,
            "chunk_count": len(chunks),
            "text_length": len(text),
            "page_count": len(set(page_numbers)),
            "pages_with_content": sorted(list(set(page_numbers))),
            "embedding_model": "qwen3-embedding:4b",
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "vector_store": "FAISS",
            "save_path": save_path
        }
        
        # 存储元数据
        if metadata_store.store_metadata(doc_id, doc_metadata):
            print(f"元数据已保存到元数据存储中: {doc_id}")
        else:
            print(f"保存元数据失败: {doc_id}")

    return knowledgeBase

def load_knowledge_base(load_path: str, embeddings = None) -> FAISS:
    """
    从磁盘加载向量数据库和页码信息
    
    参数:
        load_path: 向量数据库的保存路径
        embeddings: 可选，嵌入模型。如果为None，将创建一个新的DashScopeEmbeddings实例
    
    返回:
        knowledgeBase: 加载的FAISS向量数据库对象
    """
    # 如果没有提供嵌入模型，则创建一个新的
    if embeddings is None:
        embeddings = OllamaEmbeddings(
            model="qwen3-embedding:4b"
        )
    
    # 加载FAISS向量数据库，添加allow_dangerous_deserialization=True参数以允许反序列化
    knowledgeBase = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)
    print(f"向量数据库已从 {load_path} 加载。")
    
    # 加载页码信息
    page_info_path = os.path.join(load_path, "page_info.pkl")
    if os.path.exists(page_info_path):
        with open(page_info_path, "rb") as f:
            page_info = pickle.load(f)
        knowledgeBase.page_info = page_info
        print("页码信息已加载。")
    else:
        print("警告: 未找到页码信息文件。")
    
    # 尝试从元数据存储中加载相关元数据
    metadata_store = MetadataStore()
    # 查找保存的文档ID信息
    if os.path.exists(os.path.join(load_path, "page_info.pkl")):
        # 如果向量数据库已保存在该路径，则尝试找到对应的元数据
        # 这里我们假定doc_id可以从向量库的路径或信息中推断出来
        
        # 简单的实现: 尝试从向量库的路径中提取信息
        doc_id = os.path.basename(load_path)
        
        # 尝试获取元数据
        doc_metadata = metadata_store.get_metadata(doc_id)
        if doc_metadata:
            print(f"已从元数据存储加载文档信息: {doc_metadata.get('source_file', 'Unknown')}")
        
    return knowledgeBase

def query_with_accuracy_and_metadata(knowledge_base, query: str, k: int = 3):
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

# 读取PDF文件
pdf_reader = PdfReader('./浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf')
# 提取文本和页码信息
text, page_numbers = extract_text_with_page_numbers(pdf_reader)

print(f"提取的文本长度: {len(text)} 个字符。")
    
# 处理文本并创建知识库，同时保存到磁盘
save_dir = "./vector_db"
knowledgeBase = process_text_with_splitter(text, page_numbers, save_path=save_dir, pdf_path='./浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf')

# 从向量数据库加载（演示加载过程）
# 创建嵌入模型
embeddings = OllamaEmbeddings(model="qwen3-embedding:4b")
# 从磁盘加载向量数据库
knowledgeBase = FAISS.load_local("./vector_db", embeddings, allow_dangerous_deserialization=True)

# 加载页码信息
page_info_path = os.path.join("./vector_db", "page_info.pkl")
if os.path.exists(page_info_path):
    with open(page_info_path, "rb") as f:
        page_info = pickle.load(f)
    knowledgeBase.page_info = page_info
    print("页码信息已加载。")

# 执行查询示例
queries = [
    "客户经理被投诉了，投诉一次扣多少分",
    "客户经理每年评聘申报时间是怎样的？",
    "客户经理考核标准是什么"
]

for query in queries:
    query_with_accuracy_and_metadata(knowledgeBase, query)
    print("\n" + "="*60 + "\n")