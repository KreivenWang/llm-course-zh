"""
工具脚本：管理元数据存储
"""
import os
import sys
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metadata_store.metadata_store import MetadataStore

def list_all_metadata():
    """列出所有存储的元数据"""
    print("=== 所有文档元数据 ===")
    metadata_store = MetadataStore()
    all_metadata = metadata_store.list_all_metadata()
    
    if not all_metadata:
        print("没有找到任何元数据记录。")
        return
    
    for i, metadata in enumerate(all_metadata, 1):
        print(f"\n{i}. 文档ID: {metadata.get('doc_id', 'Unknown')}")
        print(f"   源文件: {metadata.get('source_file', 'N/A')}")
        print(f"   分块数量: {metadata.get('chunk_count', 'N/A')}")
        print(f"   文本长度: {metadata.get('text_length', 'N/A')}")
        print(f"   页数: {metadata.get('page_count', 'N/A')}")
        print(f"   嵌入模型: {metadata.get('embedding_model', 'N/A')}")
        print(f"   创建时间: {metadata.get('created_at', 'N/A')}")
        print(f"   更新时间: {metadata.get('updated_at', 'N/A')}")
        print(f"   保存路径: {metadata.get('save_path', 'N/A')}")

def view_metadata(doc_id: str):
    """查看特定文档的元数据"""
    print(f"=== 文档 '{doc_id}' 的元数据 ===")
    metadata_store = MetadataStore()
    metadata = metadata_store.get_metadata(doc_id)
    
    if metadata:
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
    else:
        print(f"未找到文档ID为 '{doc_id}' 的元数据。")

def delete_metadata(doc_id: str):
    """删除特定文档的元数据"""
    print(f"=== 删除文档 '{doc_id}' 的元数据 ===")
    metadata_store = MetadataStore()
    success = metadata_store.delete_metadata(doc_id)
    
    if success:
        print(f"成功删除文档ID为 '{doc_id}' 的元数据。")
    else:
        print(f"删除文档ID为 '{doc_id}' 的元数据失败或该文档不存在。")

if __name__ == "__main__":
    print("元数据存储管理工具")
    print("1. 列出所有元数据")
    print("2. 查看特定文档元数据")
    print("3. 删除特定文档元数据")
    
    choice = input("\n请选择操作 (1-3): ").strip()
    
    if choice == "1":
        list_all_metadata()
    elif choice == "2":
        doc_id = input("请输入文档ID: ").strip()
        view_metadata(doc_id)
    elif choice == "3":
        doc_id = input("请输入要删除的文档ID: ").strip()
        delete_metadata(doc_id)
    else:
        print("无效的选择。")