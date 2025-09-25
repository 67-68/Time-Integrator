from tinydb import TinyDB, Query
from pydantic import BaseModel
from uuid import UUID
from typing import List, Type, Optional
import yaml
import json
import os

from ti.core.Interfaces.model.repository_interface import IRepository

# --- 一个全新的、强大的Repository ---
class YamlRepository(IRepository):
    def __init__(self, db_path: str):
        # 检查文件是否存在且是YAML格式，如果是则转换为JSON
        self.db_path = db_path
        self._convert_yaml_to_json_if_needed()
        # 数据库就是一个JSON文件！
        self.db = TinyDB(db_path, indent=2)
    
    def _convert_yaml_to_json_if_needed(self):
        """如果文件是YAML格式，转换为JSON格式"""
        if not os.path.exists(self.db_path):
            return
            
        try:
            # 尝试读取文件内容
            with open(self.db_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 如果文件为空，直接返回
            if not content:
                return
            
            # 尝试解析为YAML
            yaml_data = yaml.safe_load(content)
            
            # 如果成功解析为YAML，转换为JSON格式
            if yaml_data is not None:
                # 创建临时文件备份
                backup_path = self.db_path + '.yaml_backup'
                os.rename(self.db_path, backup_path)
                
                # 写入JSON格式数据
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump(yaml_data, f, ensure_ascii=False, indent=2)
                
                print(f"Converted YAML file to JSON: {self.db_path}")
                
        except (yaml.YAMLError, json.JSONDecodeError):
            # 如果既不是YAML也不是JSON，保持原样
            pass

    def save(self, contract: BaseModel):
        # 使用 model_dump 将Pydantic模型转为字典
        contract_dict = contract.model_dump(mode='json') 
        # upsert = update or insert
        self.db.upsert(contract_dict, Query().contract_id == str(contract.contract_id))

    def get_by_id(self, contract_id: UUID) -> Optional[BaseModel]:
        result = self.db.get(Query().contract_id == str(contract_id))
        if result:
            # 这里需要知道具体的模型类型，暂时返回字典
            # 实际使用中应该传入具体的模型类
            return result
        return None
    
    def load(self) -> List[BaseModel]:
        """加载所有数据"""
        all_data = self.db.all()
        # 返回原始数据，调用者需要知道如何转换为具体模型
        return all_data
    
    def get_all(self) -> List[dict]:
        """获取所有存档"""
        return self.db.all()
    
    def delete(self, contract_id: str):
        """删除一个存档"""
        self.db.remove(Query().contract_id == contract_id)
        
    def query(self, **kwargs) -> List[dict]:
        """根据条件查询数据"""
        query = Query()
        conditions = []
        
        for field, value in kwargs.items():
            conditions.append(query[field] == value)
        
        if conditions:
            # 构建复合查询条件
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition = combined_condition & condition
            
            return self.db.search(combined_condition)
        
        return self.db.all()
    
    def count(self) -> int:
        """获取数据总数"""
        return len(self.db)
    
    def clear(self):
        """清空所有数据"""
        self.db.truncate()
    
    def update_field(self, contract_id: str, field: str, value):
        """更新特定字段"""
        self.db.update({field: value}, Query().contract_id == contract_id)
    
    def exists(self, contract_id: str) -> bool:
        """检查记录是否存在"""
        return self.db.contains(Query().contract_id == contract_id)
    
    