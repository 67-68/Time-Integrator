
from abc import ABC,abstractmethod


class ICardGenerator(ABC):
    """
    这个类作为所有卡片generator的接口
    """
    def create_report(self):
        """
        获取卡片
        """
        return
    
