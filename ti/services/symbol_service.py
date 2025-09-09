from ti.core.Interfaces.path_register_interface import PathRegisterInterface


class SymbolService:
    def __init__(self):
        """
        这个类供所有的repository
        从yaml配置文件中的字段
        查找对应symbol
        """
        self.registers:dict[type[PathRegisterInterface]] = {}
        
    def regist_register(
        self,
        register: type[PathRegisterInterface]
    ):
        """
        用来登记一个register进入总数据库

        Args:
            register (type[PathRegisterInterface]): _description_
        """
        self.registers[register.domain] = register
        print(f"登记了{register.domain}进入yaml符号数据库")
        
    def find_symbol(self,domain,symbol_name):
        register:type[PathRegisterInterface] = self.registers[domain]
        symbol_path = register.get_symbol_path()
        return symbol_path
    
    def get_symbol(self):
        """
        从symbol_path获取symbol
        """
        #TODO