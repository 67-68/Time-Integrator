from ti.core.Interfaces.symbol_path_register_interface import ISymbolPathRegister
import importlib
from typing import Any, Optional

from ti.features.detector.detector_path_register import DetectorPathRegister
from ti.features.insight.insight_path_register import InsightPathRegister
from ti.model.core_path_register import CorePathRegister


class SymbolService:
    def __init__(self):
        """
        这个类供所有的repository
        从yaml配置文件中的字段
        查找对应symbol
        """
        self.registers: dict[str, ISymbolPathRegister] = {}
        
        
        
        self.regist_register(CorePathRegister())
        # self.regist_register(InsightPathRegister())
        self.regist_register(DetectorPathRegister())
        # Intervention path register is registered separately in intervention plugin
        
        
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
            symbol_path: 符号的完整路径，格式为 "module.path.to.symbol" 或 "Class.enum_value.value"
            
        Returns:
            Any: 导入的符号对象
        """
        if not symbol_path:
            raise ValueError("Symbol path cannot be empty")
            
        # 检查是否是枚举值格式（如 "ti.features.intervention.model.model.INVEvent.USER_ACCEPTED.value"）
        if symbol_path.endswith(".value") and symbol_path.count(".") >= 4: #Speial states可以加载，但我没看到其他enum类被加载
            # 处理枚举值格式
            try:
                # 移除 .value 后缀，获取完整的类路径
                full_class_path = symbol_path[:-6]  # 移除 ".value"
                # 分割模块路径和类路径
                if "." in full_class_path:
                    module_path, class_path, constant = full_class_path.rsplit(".", 2)
                    # 导入模块
                    module = importlib.import_module(module_path)
                    # 使用eval获取枚举值
                    result = eval(f"module.{class_path}.{constant}.value")
                    return result
            except Exception as e:
                raise AttributeError(f"Could not resolve enum symbol '{symbol_path}': {e}")
        
        # 普通符号路径格式
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
    
    def fill_symbols(self, data):
        """
        遍历数据，解析 A.B 格式的符号引用
        
        Args:
            data: 要解析的数据（可以是字典、列表、字符串等）
            
        Returns:
            Any: 解析后的数据
        """
        if not data:
            return data
            
        def resolve_value(value):
            """递归解析值中的符号引用"""
            if isinstance(value, str):
                # 检查是否是 A.B 格式的符号引用
                if "." in value and not value.startswith(("http://", "https://")):
                    # 特殊情况处理：不要分割连续的点或点前后没有内容的情况
                    # 1. 超过一个点连在一起（如 ".."）
                    # 2. 点之前或之后没有东西（如 ".value" 或 "value."）
                    # 3. 包含花括号（如格式化字符串模板）
                    if ".." in value or value.startswith(".") or value.endswith(".") or ("{" in value and "}" in value):
                        return value
                    
                    try:
                        # 尝试解析符号
                        domain, symbol_name = value.split(".", 1)
                        
                        # 首先检查是否可以使用路径注册器的resolve_enum_symbol方法
                        if domain in self.registers:
                            register = self.registers[domain]
                            if hasattr(register, 'resolve_enum_symbol'):
                                resolved_value = register.resolve_enum_symbol(value)
                                if resolved_value != value:
                                    # 如果路径注册器处理了该值，直接使用get_symbol解析最终路径
                                    return self.get_symbol(resolved_value)
                        
                        # 否则使用常规符号解析
                        resolved_symbol = self.resolve_symbol(domain, symbol_name)
                        return resolved_symbol
                    except (ValueError, ImportError, AttributeError) as e:
                        print(f"Warning: Could not resolve symbol '{value}': {e}")
                        return value
            elif isinstance(value, dict):
                # 处理字典的键和值
                resolved_dict = {}
                for k, v in value.items():
                    # 首先解析键（如果键是符号引用）
                    resolved_key = k
                    if isinstance(k, str) and "." in k and not k.startswith(("http://", "https://")):
                        # 特殊情况处理：不要分割连续的点或点前后没有内容的情况
                        # 1. 超过一个点连在一起（如 ".."）
                        # 2. 点之前或之后没有东西（如 ".value" 或 "value."）
                        # 3. 包含花括号（如格式化字符串模板）
                        if ".." in k or k.startswith(".") or k.endswith(".") or ("{" in k and "}" in k):
                            pass  # 不处理这种情况
                        else:
                            try:
                                domain, symbol_name = k.split(".", 1)
                                resolved_key = self.resolve_symbol(domain, symbol_name)
                            except (ValueError, ImportError, AttributeError) as e:
                                print(f"Warning: Could not resolve key symbol '{k}': {e}")
                    
                    # 然后递归解析值
                    resolved_value = resolve_value(v)
                    resolved_dict[resolved_key] = resolved_value
                return resolved_dict
            elif isinstance(value, list):
                return [resolve_value(item) for item in value]
            return value
        
        # 递归解析整个数据结构
        return resolve_value(data)