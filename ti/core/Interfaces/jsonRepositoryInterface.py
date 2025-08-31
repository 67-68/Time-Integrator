from abc import ABC,abstractmethod

from ti.dataAccess.dataAccess import getData, saveData

class JsonRepositoryInterface(ABC):
    """_summary_
    这个类是repository的接口
    规定了所有repository必须包含
    1. 文件路径
    2. 加载
    3. 存储
    首先，它会加载所有的文件出来
    Args:
        ABC (_type_): _description_
    """
    @property
    @abstractmethod
    def filePath(self) -> str:
        """_summary_
        抽象名字方法
        返回一个文件路径
        Returns:
            str: _description_
        """
        pass
    
    @abstractmethod
    def save(self):
        """_summary_
        基本的存储
        Args:
            data (_type_): _description_
        """
        pass
    
    @abstractmethod
    def load(self):
        """
        基本的加载
        """
        pass