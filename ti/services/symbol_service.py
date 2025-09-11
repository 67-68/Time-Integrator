from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
import importlib
from typing import Any, Optional


class SymbolService:
    def __init__(self):
        """
        这个类供所有的repository
        从yaml配置文件中的字段
        查找对应symbol
        """
        self.registers: dict[str, ISymbolPathRegister] = {}
        
    def regist_register(
        self,
        register: ISymbolPathRegister
    ):
        """
        用来登记一个register进入总数据库

        Args:
            register (ISymbolPathRegister): 符号路径注册器实例
        """
        self.registers[register.domain] = register
        print(f"登记了{register.domain}进入yaml符号数据库")
        
    def find_symbol(self, domain: str, symbol_name: str) -> Optional[str]:
        """
        根据域名和符号名称查找符号路径
        
        Args:
            domain: 符号所属的领域/模块
            symbol_name: 符号名称
            
        Returns:
            Optional[str]: 符号的完整路径，如果找不到返回None
        """
        if domain not in self.registers:
            raise ValueError(f"Domain '{domain}' not registered")
            
        register = self.registers[domain]
        symbol_model = register.get_symbol_path(symbol_name)
        return symbol_model.symbol_path if symbol_model else None
    
    def get_symbol(self, symbol_path: str) -> Any:
        """
        从symbol_path获取symbol对象
        
        Args:
            symbol_path: 符号的完整路径，格式为 "module.path.to.symbol"
            
        Returns:
            Any: 导入的符号对象
        """
        if not symbol_path:
            raise ValueError("Symbol path cannot be empty")
            
        # 分割模块路径和符号名称
        if "." not in symbol_path:
            raise ValueError(f"Invalid symbol path format: {symbol_path}")
            
        # 分割模块路径和符号名称
        module_path, symbol_name = symbol_path.rsplit(".", 1)
        
        try:
            # 动态导入模块
            module = importlib.import_module(module_path)
            # 获取符号
            symbol = getattr(module, symbol_name)
            return symbol
        except ImportError as e:
            raise ImportError(f"Could not import module '{module_path}': {e}")
        except AttributeError as e:
            raise AttributeError(f"Symbol '{symbol_name}' not found in module '{module_path}': {e}")
    
    def resolve_symbol(self, domain: str, symbol_name: str) -> Any:
        """
        解析符号：先查找符号路径，然后获取符号对象
        
        Args:
            domain: 符号所属的领域/模块
            symbol_name: 符号名称
            
        Returns:
            Any: 解析后的符号对象
        """
        # 第一步：查找符号路径
        symbol_path = self.find_symbol(domain, symbol_name)
        if not symbol_path:
            raise ValueError(f"Symbol '{symbol_name}' not found in domain '{domain}'")
        
        # 第二步：获取符号对象
        return self.get_symbol(symbol_path)