from enum import Enum
from abc import ABC,abstractmethod
from typing import Optional

import yaml

from ti.model.symbol_models import SymbolModel, SymbolType

class ISymbolPathRegister(ABC):
    @property
    @abstractmethod
    def domain(self):
        """
        用来登记这个register负责哪一个模块
        """
        pass
    
    @property
    @abstractmethod
    def class_file_path(self):
        """
        存储类yaml符号类对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def class_method_file_path(self):
        """
        存储类yaml符号类方法对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def function_file_path(self):
        """
        存储函数yaml符号对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def enum_file_path(self):
        """
        存储enum类yaml符号对应文件的路径
        """
        pass
    
    
    
    @abstractmethod
    def regist_symbol_path(self, symbol_model: SymbolModel) -> None:
        """
        Register a symbol path
        """
        # Use symbol_name as the key for storage
        if symbol_model.symbol_name:
            self._symbols[symbol_model.symbol_name] = symbol_model
        else:
            # Fallback to original format if no symbol_name
            symbol_id = f"{symbol_model.symbol_type.value}:{symbol_model.symbol_path}"
            self._symbols[symbol_id] = symbol_model
    @property
    @abstractmethod
    def enum_mapping(self):
        return self._enum_mapping

    @abstractmethod
    def get_symbol_path(self, symbol_id: str) -> Optional[SymbolModel]:
        """
        Get symbol by id or symbol_name
        """
        if symbol_id.endswith(".value"):
            symbol_id = symbol_id.split(".")[0]
        try:
            if symbol_id in self.enum_mapping:
                # 返回枚举符号的SymbolModel
                return SymbolModel(
                    symbol_type=SymbolType.ENUM_CLASS,
                    symbol_path=self.enum_mapping[symbol_id],
                    symbol_domain="model"
                )
        except Exception as e:
            print("no enum mapping")
        
        # First try to find by symbol_name (new format)
        # Try exact match first
        symbol = self._symbols.get(symbol_id)
        if symbol:
            return symbol
        
        # Then try case-insensitive match
        for key, symbol_model in self._symbols.items():
            if key.lower() == symbol_id.lower():
                return symbol_model
        
        # Fallback to search by symbol_type:path format
        for symbol_model in self._symbols.values():
            if symbol_model.symbol_path == symbol_id:
                return symbol_model
        
        return None
    
    @abstractmethod
    def search_symbol_data(self, symbol_type: Optional[SymbolType] = None, 
                          domain: Optional[str] = None) -> list[SymbolModel]:
        """
        Search symbols by type and/or domain
        """
        results = []
        for symbol in self._symbols.values():
            if symbol_type and symbol.symbol_type != symbol_type:
                continue
            if domain and symbol.symbol_domain != domain:
                continue
            results.append(symbol)
        return results    
    
    @abstractmethod
    def get_symbol_model(self):
        """
        返回这个symbol相关的信息
        返回dataclass: symbol model
        """
    
    @abstractmethod
    def load_data(self):
        """
        在这里加载存储的三个model文件的数据
        存入类变量
        """
        pass
    
    @abstractmethod
    def _load_from_file(self,file_path,key):
        """
        Load data from a specific YAML file
        """
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                
            if data and key in data:
                for name in data[key]:
                    item = data[key][name]
                    if not isinstance(item,str):
                    
                        symbol = SymbolModel(
                            symbol_type=SymbolType(item['symbol_type']),
                            symbol_path=item['symbol_path'],
                            symbol_domain=item['symbol_domain'],
                            symbol_name=name  # Populate symbol_name with the YAML key
                        )
                        self.regist_symbol_path(symbol)
                        
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
        except Exception as e:
            print(f"Error loading symbol data from {file_path}: {e}")
    
