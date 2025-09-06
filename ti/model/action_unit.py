from dataclasses import dataclass, asdict
from typing import Optional, Any
import uuid


@dataclass
class ActionUnit:
    # 必需字段
    action: str
    start: str  # 保持字符串格式与现有数据兼容
    end: str
    action_type: str
    action_detail: str
    date: str
    
    # 可选字段
    id: str = ""
    timeSpan: int = 0
    urgency: Optional[str] = None
    importance: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理，生成ID等"""
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def __getitem__(self, key) -> Any:
        """
        魔法方法：支持字典式访问 au["field"]
        与 .get() 方法功能相同，但会在键不存在时抛出 KeyError
        """
        # 如果是数字索引，抛出 TypeError（ActionUnit 不是序列）
        if isinstance(key, int):
            raise TypeError(f"ActionUnit indices must be strings, not int. Use au.field_name or au['field_name'] instead of au[{key}]")
        
        # 如果不是字符串，转为字符串处理
        if not isinstance(key, str):
            key = str(key)
            
        # # 处理字段名的映射
        # field_mapping = {
        #     "actionDetail": "action_detail",  # 兼容旧的命名
        # }
        
        # # 使用映射后的字段名
        # actual_key = field_mapping.get(key, key)
        
        # 检查属性是否存在
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' not found in ActionUnit")
    
    def get(self, key: str, default=None) -> Any:
        """
        字典式访问方法，提供向后兼容
        支持原有的字典访问模式，但返回默认值而不是抛出异常
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def keys(self):
        """返回所有字段名，支持 ** 解包操作，包括映射字段"""
        base_keys = set(self.__dict__.keys())
        # 添加映射字段名
        base_keys.add("action_detail")  # 映射到 action_detail
        return base_keys
    
    def values(self):
        """返回所有字段值，支持 ** 解包操作"""
        return self.__dict__.values()
    
    def items(self):
        """返回所有字段的键值对，支持 ** 解包操作，包括映射字段"""
        items = dict(self.__dict__)
        # 添加映射字段
        if hasattr(self, 'action_detail'):
            items["action_detail"] = self.action_detail
        return items.items()
    
    def to_dict(self) -> dict:
        """转换为字典格式，用于JSON序列化"""
        data = asdict(self)
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ActionUnit':
        """从字典创建ActionUnit对象"""
        # 过滤掉不存在的字段
        valid_fields = {f for f in cls.__dataclass_fields__}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    