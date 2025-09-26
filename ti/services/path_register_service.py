"""
Path Register Service - 可配置的符号路径注册服务

这个服务提供了一种统一的方式来创建和管理符号路径注册器，
通过配置减少重复代码和错误。
"""

from ti.model.plugin.symbol_path_register_interface import ISymbolPathRegister
from ti.model.symbol_models import SymbolModel, SymbolType
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PathRegisterConfig:
    """Path Register 配置类"""
    domain: str
    domain_file_path: str  # 基础路径，用于确定其他文件的路径
    enum_mapping: Dict[str, str] = None
    
    def __post_init__(self):
        if self.enum_mapping is None:
            self.enum_mapping = {}


class PathRegisterService(ISymbolPathRegister):
    """
    可配置的符号路径注册服务
    
    通过配置来创建符号路径注册器，减少重复代码和错误。
    """
    
    def __init__(self, config: PathRegisterConfig):
        self._config = config
        self._symbols: Dict[str, SymbolModel] = {}
        self._enum_mapping = config.enum_mapping
        self.paths = []
        self.load_data()
    
    @property
    def enum_mapping(self):
        return self._enum_mapping
    
    @property
    def domain(self) -> str:
        return self._config.domain
    
    @property
    def class_file_path(self) -> str:
        return f"{self._config.domain_file_path}/classes.yaml"
    
    @property
    def class_method_file_path(self) -> str:
        return f"{self._config.domain_file_path}/class_methods.yaml"
    
    @property
    def function_file_path(self) -> str:
        return f"{self._config.domain_file_path}/functions.yaml"
    
    @property
    def enum_file_path(self) -> str:
        return f"{self._config.domain_file_path}/enums.yaml"
    
    def get_symbol_path(self, symbol_id):
        return super().get_symbol_path(symbol_id)
    
    def search_symbol_data(self, symbol_type=None, domain=None):
        return super().search_symbol_data(symbol_type, domain)
    
    def get_symbol_model(self) -> Dict[str, SymbolModel]:
        """Get all symbol models"""
        return self._symbols
    
    def load_data(self) -> None:
        """Load data from YAML files"""
        # Load from separate files
        self._load_from_file(self.class_method_file_path, "class_methods")
        self._load_from_file(self.function_file_path, "functions")
        self._load_from_file(self.class_file_path, "classes")
        self._load_from_file(self.enum_file_path, "enum_classes")
    
    def _load_from_file(self, file_path, key):
        return super()._load_from_file(file_path, key)
    
    def resolve_enum_symbol(self, symbol_ref: str) -> str:
        """
        解析枚举符号引用
        格式: domain.ENUM_NAME 或 domain.ENUM_CLASS.ENUM_VALUE.value
        """
        if not symbol_ref.startswith(f"{self.domain}."):
            return symbol_ref
        
        # 移除 "domain." 前缀
        enum_path = symbol_ref.split(".", 1)[1]
        
        # 检查是否是简单枚举名
        if enum_path in self.enum_mapping:
            return f"{self._config.domain_file_path.replace('/', '.')}.{self.enum_mapping[enum_path]}"
        
        # 检查是否是复杂枚举路径格式：ENUM_CLASS.ENUM_VALUE.value
        if enum_path.endswith(".value") and enum_path.count(".") >= 2:
            # 格式：ENUM_CLASS.ENUM_VALUE.value
            full_enum_path = f"{self._config.domain_file_path.replace('/', '.')}.{enum_path}"
            return full_enum_path
        
        return symbol_ref
    
    def regist_symbol_path(self, symbol_model):
        return super().regist_symbol_path(symbol_model)