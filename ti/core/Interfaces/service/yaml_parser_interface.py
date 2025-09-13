from abc import abstractmethod
from ti.core.Interfaces.service.parser_interface import IParser


class IYamlParser(IParser):
    @property
    @abstractmethod
    def rules_file_path(self):
        """
        存放所有的解析规则
        """
    
    @abstractmethod
    def parse_data(self):
        """
        根据规则解析数据
        """
        pass
        