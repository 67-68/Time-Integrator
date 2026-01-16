import uuid
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.core.definitions import YESTERDAY
from ti.features.capture.model.selection_condition import SelectionCondition
from ti.model.action_unit_repository import ActionUnitRepository
from ti.model.action_unit import ActionUnit
from ti.model.yaml_repository import YamlRepository

"""
这个文件用来存储数据相关的操作，现在使用ActionUnit Repository
"""
class DataService(QObject):
    actionUnit_added = pyqtSignal(ActionUnit) # 新增加AU的信号，现在传递ActionUnit对象
    
    _instance = None
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.repository = ActionUnitRepository()
        self._repositories: dict[str,IRepository] = None # 存储其他类型的数据模型, TODO 以后要全部换成这个
    
    @classmethod
    def get_instance(cls):
        """
        返回全局变量
        给装饰器使用

        Returns:
            _type_: _description_
        """
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance
        
        
    def createNewData(self) -> ActionUnit:
        """
        创建新的空ActionUnit对象
        """
        return ActionUnit(
            id=str(uuid.uuid4()),
            date="",
            action="",
            start="",
            end="",
            action_type="",
            action_detail="",
            timeSpan=0,
            urgency=None,
            importance=None
        )
    
    def get_yesterday_AU(self):
        """
        获取昨天的ActionUnit数据
        """
        return self.repository.get_by_date(YESTERDAY)
    
    def get_date_range_AU(self, start_date: str, end_date: str) -> list[ActionUnit]:
        """
        获取日期范围内的所有ActionUnit
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            list[ActionUnit]: 日期范围内的所有ActionUnit
        """
        date_range_data = self.repository.get_date_range(start_date, end_date)
        all_aus = []
        for date_aus in date_range_data.values():
            all_aus.extend(date_aus)
        return all_aus
    
    def add_actionUnit(self, au: ActionUnit):
        """
        添加或更新ActionUnit
        现在接收ActionUnit对象而不是字典
        """
        date = au.date
        
        # 检查是否已存在（更新操作）
        existing_units = self.repository.get_by_date(date)
        for i, existing_au in enumerate(existing_units):
            if existing_au.id == au.id:
                # 更新现有记录
                existing_units[i] = au
                self.repository.data[date] = existing_units
                self.repository.save()
                self.actionUnit_added.emit(au)
                return
        
        # 添加新记录
        self.repository.add_action_unit(date, au)
        self.actionUnit_added.emit(au)
        
    def get_date_data(self, date: str):
        """
        获取指定日期的ActionUnit列表
        """
        return self.repository.get_by_date(date)
    
    def get_data(self):
        """
        获取所有ActionUnit数据
        """
        return self.repository.get_all()
    
    def delete_actionUnit(self, action_unit_id: str):
        """
        删除ActionUnit
        """
        self.repository.delete(action_unit_id)
    
    def find_action_unit_by_date_and_start(self, date: str, start_time: str):
        """
        根据日期和开始时间查找ActionUnit
        :param date: 日期字符串
        :param start_time: 开始时间字符串
        :return: 找到的ActionUnit或None
        """
        action_units = self.repository.get_by_date(date)
        for au in action_units:
            if au.start == start_time:
                return au
        return None
    
    
    def parse_selection_condition(self,selection_condition: SelectionCondition):
        """
        注意！Selection里面的Data Model type 需要是DataModel类本身

        Args:
            selection_condition (SelectionCondition): _description_

        Returns:
            _type_: _description_
        """
        repo = self._repositories[selection_condition.data_type]
        data = repo.get_by_date(selection_condition.date)
        return data
        
    def match_date(self,date):
        def matcher(data):
            if data.date == date:
                return data
        return matcher
    
    def add_repository(self,repo: YamlRepository):
        self._repositories[repo.model_class] = repo # 使用data class 类本身存储
        
    