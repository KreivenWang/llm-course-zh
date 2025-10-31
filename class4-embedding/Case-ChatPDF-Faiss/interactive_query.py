"""
交互式查询脚本，使用知识库管理器
"""
from knowledge_base_manager import KnowledgeBaseManager
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks.manager import get_openai_callback
from langchain_ollama import ChatOllama
import time

def interactive_query():
    """
    交互式查询，用户可以持续提问
    """
    print("正在初始化知识库管理器...")
    
    # 创建知识库管理器实例
    kb_manager = KnowledgeBaseManager(
        pdf_path='./浦发上海浦东发展银行西安分行个金客户经理考核办法.pdf',
        vector_store_path='./vector_db',
        embeddings_model='qwen3-embedding:4b'
    )
    
    # 加载或创建知识库（只在第一次运行时创建）
    knowledge_base = kb_manager.load_or_create_knowledge_base()
    
    # 加载LLM
    llm = ChatOllama(model="qwen3:14b")
    
    print("\n知识库已准备就绪！您可以开始提问了。")
    print("输入 'quit' 或 'exit' 退出程序。")
    print("="*50)
    
    while True:
        query = input("\n请输入您的问题: ").strip()
        
        if query.lower() in ['quit', 'exit', '退出', 'q']:
            print("感谢使用！再见！")
            break
        
        if not query:
            print("请输入有效的问题。")
            continue
        
        print(f"\n正在搜索答案...")
        start_time = time.time()
        
        # 查询知识库
        docs_with_scores = kb_manager.query_knowledge_base(query, k=3)
        
        search_time = time.time() - start_time
        print(f"搜索完成，耗时: {search_time:.3f} 秒")
        print(f"找到 {len(docs_with_scores)} 个相关文档片段")
        
        # 准备文档上下文
        context_parts = []
        print("\n--- 匹配准确度和元数据详情 ---")
        
        # 展示每个文档片段的详细信息
        for i, (doc, score) in enumerate(docs_with_scores, 1):
            content = getattr(doc, "page_content", "")
            source_page = knowledge_base.page_info.get(content.strip(), "未知")
            
            # 计算相似度百分比
            max_score = max(doc_tuple[1] for doc_tuple in docs_with_scores) if docs_with_scores else 1
            similarity_percentage = max(0, min(100, (1 - score / (max_score + 0.001)) * 100))
            
            print(f"\n文档片段 {i}:")
            print(f"  相似度得分: {score:.4f}")
            print(f"  估算相似度: {similarity_percentage:.2f}%")
            print(f"  来源页码: {source_page}")
            # 只显示第一行，如果超过50个字符则截断并显示...
            first_line = content.split('\n')[0] if content.split('\n') else ""
            preview = first_line[:50] + "..." if len(first_line) > 50 else first_line
            print(f"  内容预览: {preview}")
            
            # 添加到上下文
            context_parts.append(f"文档片段 {i} (相似度: {similarity_percentage:.2f}%, 来源页码: {source_page}): {content}")
        
        # 构建最终的上下文
        context = "\\n\\n".join(context_parts)
        
        # 创建提示模板
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


if __name__ == "__main__":
    interactive_query()