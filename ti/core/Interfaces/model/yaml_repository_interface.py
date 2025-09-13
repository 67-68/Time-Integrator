from abc import abstractmethod
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.core.Interfaces.service.yaml_parser_interface import IYamlParser


class IYamlRepository(IRepository):
    @property
    @abstractmethod
    def yaml(self) -> type[IYamlParser]:
        """
        应该返回一个yaml parser类的实例
        """
        pass
    
    @property
    @abstractmethod
    def rule_file_path(self):
        """
        返回规则文件的位置
        """
        pass