"""
Metadata Store for managing document metadata
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import hashlib

class MetadataStore:
    def __init__(self, storage_path: str = "./metadata_store"):
        """
        初始化元数据存储
        
        Args:
            storage_path: 元数据存储路径
        """
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        
    def _get_metadata_file_path(self, doc_id: str) -> str:
        """
        获取元数据文件路径
        
        Args:
            doc_id: 文档ID
            
        Returns:
            元数据文件的完整路径
        """
        # 使用文档ID的哈希值作为文件名，避免特殊字符问题
        doc_hash = hashlib.md5(doc_id.encode('utf-8')).hexdigest()
        return os.path.join(self.storage_path, f"{doc_hash}.json")
    
    def store_metadata(self, doc_id: str, metadata: Dict[str, Any]) -> bool:
        """
        存储文档元数据
        
        Args:
            doc_id: 文档ID
            metadata: 元数据字典
            
        Returns:
            是否存储成功
        """
        try:
            # 添加时间戳
            metadata['created_at'] = datetime.now().isoformat()
            metadata['updated_at'] = datetime.now().isoformat()
            metadata['doc_id'] = doc_id
            
            # 确定文件路径
            file_path = self._get_metadata_file_path(doc_id)
            
            # 写入元数据到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
                
            return True
        except Exception as e:
            print(f"存储元数据时出错: {e}")
            return False
    
    def update_metadata(self, doc_id: str, metadata_updates: Dict[str, Any]) -> bool:
        """
        更新文档元数据
        
        Args:
            doc_id: 文档ID
            metadata_updates: 要更新的元数据字段
            
        Returns:
            是否更新成功
        """
        try:
            # 获取现有元数据
            current_metadata = self.get_metadata(doc_id)
            
            if current_metadata is None:
                # 如果元数据不存在，创建新的
                current_metadata = {}
            
            # 更新元数据
            current_metadata.update(metadata_updates)
            current_metadata['updated_at'] = datetime.now().isoformat()
            
            # 存储更新后的元数据
            return self.store_metadata(doc_id, current_metadata)
        except Exception as e:
            print(f"更新元数据时出错: {e}")
            return False
    
    def get_metadata(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档元数据
        
        Args:
            doc_id: 文档ID
            
        Returns:
            元数据字典或None（如果不存在）
        """
        try:
            file_path = self._get_metadata_file_path(doc_id)
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                return metadata
            else:
                return None
        except Exception as e:
            print(f"获取元数据时出错: {e}")
            return None
    
    def delete_metadata(self, doc_id: str) -> bool:
        """
        删除文档元数据
        
        Args:
            doc_id: 文档ID
            
        Returns:
            是否删除成功
        """
        try:
            file_path = self._get_metadata_file_path(doc_id)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except Exception as e:
            print(f"删除元数据时出错: {e}")
            return False
    
    def list_all_metadata(self) -> List[Dict[str, Any]]:
        """
        列出所有元数据记录
        
        Returns:
            所有元数据记录的列表
        """
        try:
            metadata_list = []
            
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.storage_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        metadata_list.append(metadata)
                        
            return metadata_list
        except Exception as e:
            print(f"列出元数据时出错: {e}")
            return []