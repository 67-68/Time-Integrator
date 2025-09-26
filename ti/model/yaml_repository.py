from tinydb import TinyDB, Query
from pydantic import BaseModel
from uuid import UUID
from typing import List, Type, Optional, Generic, TypeVar
import yaml
import json
import os

from ti.core.Interfaces.model.repository_interface import IRepository

# 泛型类型变量，表示具体的BaseModel子类
T = TypeVar('T', bound=BaseModel)


class FileFormatDetector:
    """专门负责检测文件格式的类"""
    
    @staticmethod
    def detect_format(file_path: str) -> str:
        """检测文件格式，返回 'yaml', 'json', 或 'unknown'"""
        if not os.path.exists(file_path):
            return 'json'  # 默认创建JSON文件
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return 'json'
            
            # 首先尝试解析为JSON
            try:
                json.loads(content)
                if file_path.lower().endswith(('.yaml', '.yml')):
                    return 'yaml'
                return 'json'
            except json.JSONDecodeError:
                pass
            
            # 如果不是JSON，尝试解析为YAML
            yaml.safe_load(content)
            return 'yaml'
        except yaml.YAMLError:
            return 'json'
        except Exception:
            return 'unknown'


class DataConverter:
    """专门负责数据格式转换的类"""
    
    @staticmethod
    def convert_to_tinydb_format(data) -> dict:
        """将数据转换为TinyDB格式"""
        tiny_db_data = {"_default": {}}
        
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                tiny_db_data["_default"][str(i)] = item
        elif isinstance(data, dict):
            # 如果已经是TinyDB格式，直接使用
            if "_default" in data:
                return data
            # 否则转换为TinyDB格式
            tiny_db_data["_default"] = data
        
        return tiny_db_data
    
    @staticmethod
    def load_yaml_to_dict(file_path: str) -> dict:
        """从YAML文件加载数据到字典"""
        if not os.path.exists(file_path):
            return {}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return {}
            
            yaml_data = yaml.safe_load(content)
            if yaml_data is None:
                yaml_data = []
            
            return yaml_data
        except (yaml.YAMLError, json.JSONDecodeError):
            return {}
    
    @staticmethod
    def save_dict_to_yaml(data: list, file_path: str):
        """将字典数据保存为YAML文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, indent=2)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            print(f"Error saving to YAML file: {e}")


class StorageStrategy:
    """存储策略接口"""
    
    def initialize(self, db_path: str) -> TinyDB:
        """初始化存储"""
        raise NotImplementedError
    
    def sync_to_source(self, db: TinyDB, db_path: str):
        """同步到源文件"""
        raise NotImplementedError


class YamlStorageStrategy(StorageStrategy):
    """YAML存储策略"""
    
    def __init__(self, identifier_field: str = "project_id"):
        self.temp_json_path = None
        self.identifier_field = identifier_field
    
    def initialize(self, db_path: str) -> TinyDB:
        self.temp_json_path = db_path + '.temp.json'
        self._load_yaml_to_temp_json(db_path)
        return TinyDB(self.temp_json_path, indent=2)
    
    def sync_to_source(self, db: TinyDB, db_path: str):
        all_data = db.all()
        pure_data = [{k: v for k, v in doc.items() if k != 'doc_id'} for doc in all_data]
        DataConverter.save_dict_to_yaml(pure_data, db_path)
    
    def _load_yaml_to_temp_json(self, db_path: str):
        yaml_data = DataConverter.load_yaml_to_dict(db_path)
        
        if isinstance(yaml_data, dict) and all(isinstance(v, dict) for v in yaml_data.values()):
            # 使用顶层键作为标识符，使用配置的identifier字段名
            yaml_data = [{self.identifier_field: pid, **data} for pid, data in yaml_data.items()]
        
        tiny_db_data = DataConverter.convert_to_tinydb_format(yaml_data)
        
        with open(self.temp_json_path, 'w', encoding='utf-8') as f:
            json.dump(tiny_db_data, f, ensure_ascii=False, indent=2)


class JsonStorageStrategy(StorageStrategy):
    """JSON存储策略"""
    
    def initialize(self, db_path: str) -> TinyDB:
        self._convert_json_to_tinydb_format(db_path)
        return TinyDB(db_path, indent=2)
    
    def sync_to_source(self, db: TinyDB, db_path: str):
        # JSON格式不需要额外同步，TinyDB直接操作文件
        pass
    
    def _convert_json_to_tinydb_format(self, db_path: str):
        if not os.path.exists(db_path):
            return
            
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                return
            
            json_data = json.loads(content)
            
            if isinstance(json_data, dict) and "_default" in json_data:
                return
            
            tiny_db_data = DataConverter.convert_to_tinydb_format(json_data)
            
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(tiny_db_data, f, ensure_ascii=False, indent=2)
                
        except json.JSONDecodeError:
            pass


# --- 一个全新的、强大的Repository ---
class YamlRepository(IRepository, Generic[T]):
    def __init__(self, db_path: str, model_class: Type[T], identifier_field: str = "contract_id"):
        """
        这个类处理数据存储
        它接受一个文件路径，读取或者修改它
        它接受一个BaseModel的子类, 输出为它的格式
        它接受一个Identifier作为record 的unique identifier, 使用它来查找东西
        
        它的扩展性基本上不需要修改，如果报错请检查BaseModel
        

        Args:
            db_path (str): _description_
            model_class (Type[T]): _description_
            identifier_field (str, optional): _description_. Defaults to "contract_id".
        """
        self.db_path = db_path
        self.model_class = model_class
        self.identifier = identifier_field
        
        # 使用策略模式
        self.storage_strategy = self._create_storage_strategy(db_path)
        self.db = self.storage_strategy.initialize(db_path)
    
    def _create_storage_strategy(self, db_path: str) -> StorageStrategy:
        """根据文件格式创建相应的存储策略"""
        file_format = FileFormatDetector.detect_format(db_path)
        
        if file_format == 'yaml':
            return YamlStorageStrategy(self.identifier)
        else:
            return JsonStorageStrategy()

    def save(self, item: T):
        self._upsert_item(item)
        self._sync_to_source_file()
    
    def _upsert_item(self, item: T):
        """更新或插入项目"""
        item_dict = item.model_dump(mode='json') 
        
        if hasattr(item, self.identifier):
            identifier_value = getattr(item, self.identifier)
            self.db.upsert(item_dict, Query()[self.identifier] == str(identifier_value))
        else:
            self.db.insert(item_dict)
    
    def _sync_to_source_file(self):
        """同步数据到源文件"""
        self.storage_strategy.sync_to_source(self.db, self.db_path)
    

    def get_by_id(self, identifier_value: str) -> Optional[T]:
        result = self.db.get(Query()[self.identifier] == str(identifier_value))
        if result:
            # 使用传入的模型类将字典转换为具体的BaseModel实例
            return self.model_class(**result)
        return None
    
    def load(self) -> List[T]:
        """加载所有数据"""
        all_data = self.db.all()
        # 将每个字典转换为具体的BaseModel实例
        return [self.model_class(**item) for item in all_data]
    
    def get_all(self) -> List[T]:
        """获取所有存档"""
        all_data = self.db.all()
        return [self.model_class(**item) for item in all_data]
    
    def delete(self, identifier_value: str):
        """删除一个存档"""
        self.db.remove(Query()[self.identifier] == identifier_value)
        self._sync_to_source_file()
        
    def query(self, **kwargs) -> List[T]:
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
            
            results = self.db.search(combined_condition)
            return [self.model_class(**item) for item in results]
        
        all_data = self.db.all()
        return [self.model_class(**item) for item in all_data]
    
    def count(self) -> int:
        """获取数据总数"""
        return len(self.db)
    
    def clear(self):
        """清空所有数据"""
        self.db.truncate()
        self._sync_to_source_file()
    
    def update_field(self, identifier_value: str, field: str, value):
        """更新特定字段"""
        self.db.update({field: value}, Query()[self.identifier] == identifier_value)
        self._sync_to_source_file()
    
    def exists(self, identifier_value: str) -> bool:
        """检查记录是否存在"""
        return self.db.contains(Query()[self.identifier] == identifier_value)
    
    def __del__(self):
        """析构函数，清理临时文件"""
        if isinstance(self.storage_strategy, YamlStorageStrategy):
            temp_path = self.storage_strategy.temp_json_path
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # 忽略删除错误
    
    