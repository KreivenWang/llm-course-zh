"""
知识库管理器，用于创建和重用知识库
"""
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List, Tuple
import os
import pickle
import time

class KnowledgeBaseManager:
    def __init__(self, pdf_path: str, vector_store_path: str = "./vector_db", embeddings_model: str = "qwen3-embedding:4b"):
        """
        初始化知识库管理器
        
        参数:
            pdf_path: PDF文件路径
            vector_store_path: 向量存储路径
            embeddings_model: 嵌入模型名称
        """
        self.pdf_path = pdf_path
        self.vector_store_path = vector_store_path
        self.embeddings_model = embeddings_model
        self.embeddings = OllamaEmbeddings(model=embeddings_model)
        self.knowledge_base = None
        
    def extract_text_with_page_numbers(self, pdf) -> Tuple[str, List[int]]:
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

    def process_text_with_splitter(self, text: str, page_numbers: List[int]) -> FAISS:
        """
        处理文本并创建向量存储
        
        参数:
            text: 提取的文本内容
            page_numbers: 每行文本对应的页码列表
        
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
            
        # 从文本块创建知识库
        knowledgeBase = FAISS.from_texts(chunks, self.embeddings)
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
        
        # 保存向量数据库和页码信息
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        # 保存FAISS向量数据库
        knowledgeBase.save_local(self.vector_store_path)
        print(f"向量数据库已保存到: {self.vector_store_path}")
        
        # 保存页码信息到同一目录
        with open(os.path.join(self.vector_store_path, "page_info.pkl"), "wb") as f:
            pickle.dump(page_info, f)
        print(f"页码信息已保存到: {os.path.join(self.vector_store_path, 'page_info.pkl')}")

        return knowledgeBase

    def load_or_create_knowledge_base(self) -> FAISS:
        """
        加载已存在的知识库或创建新的知识库
        
        返回:
            knowledge_base: 知识库对象
        """
        # 检查向量数据库是否已存在
        if os.path.exists(self.vector_store_path) and os.path.exists(os.path.join(self.vector_store_path, "index.faiss")):
            print(f"从 {self.vector_store_path} 加载已存在的向量数据库...")
            knowledge_base = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            
            # 加载页码信息
            page_info_path = os.path.join(self.vector_store_path, "page_info.pkl")
            if os.path.exists(page_info_path):
                with open(page_info_path, "rb") as f:
                    page_info = pickle.load(f)
                knowledge_base.page_info = page_info
                print("页码信息已加载。")
            else:
                print("警告: 未找到页码信息文件。")
            
            self.knowledge_base = knowledge_base
            return knowledge_base
        else:
            print(f"未找到已保存的向量数据库，正在从PDF创建新的知识库...")
            # 读取PDF文件
            pdf_reader = PdfReader(self.pdf_path)
            # 提取文本和页码信息
            text, page_numbers = self.extract_text_with_page_numbers(pdf_reader)
            
            print(f"提取的文本长度: {len(text)} 个字符。")
                
            # 处理文本并创建知识库，同时保存到磁盘
            knowledge_base = self.process_text_with_splitter(text, page_numbers)
            self.knowledge_base = knowledge_base
            return knowledge_base

    def query_knowledge_base(self, query: str, k: int = 3):
        """
        查询知识库
        
        参数:
            query: 查询字符串
            k: 返回的文档数量
        
        返回:
            查询结果文档列表
        """
        if self.knowledge_base is None:
            self.load_or_create_knowledge_base()
        
        # 执行相似度搜索
        docs = self.knowledge_base.similarity_search_with_score(query, k=k)
        return docs