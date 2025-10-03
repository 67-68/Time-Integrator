from abc import ABC,abstractmethod


class IRepository(ABC):
    """
    所有repository的interface

    Args:
        ABC (_type_): _description_
    """
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

    def get_by_id(self,id: str):
        """
        通过id
        uuid 或者类别ID 获取一个存档
        """
        pass
    
    def get_all(self):
        """
        获取所有存档
        """
        pass
        
    def delete(self,id:str):
        """
        删除一个存档

        Args:
            id (str): _description_
        """
        pass
    
    def get_by_date(self,date): # 后续或许会出一个date protocol, 但是现在就这样吧
        return