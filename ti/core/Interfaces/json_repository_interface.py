from abc import ABC,abstractmethod

from ti.core.Interfaces.repository_interface import IRepository



class IJsonRepository(IRepository):
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
    