from abc import abstractmethod
from ti.core.Interfaces.repository_interface import IRepository
from ti.core.Interfaces.yaml_parser_interface import IYamlParser


class IYamlRepository(IRepository):
    @property
    @abstractmethod
    def yaml_parser(self) -> type[IYamlParser]:
        """
        应该返回一个yaml parser类的实例
        """
        pass