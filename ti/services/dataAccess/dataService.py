import uuid
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from ti.core.definitions import YESTERDAY
from ti.model.action_unit_repository import ActionUnitRepository
from ti.model.action_unit import ActionUnit

"""
这个文件用来存储数据相关的操作，现在使用ActionUnit Repository
"""
class DataService(QObject):
    actionUnit_added = pyqtSignal(ActionUnit) # 新增加AU的信号，现在传递ActionUnit对象
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.repository = ActionUnitRepository()
    
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
    
    # ===== 新增的便利方法 =====
    
    def get_by_action_type(self, action_type: str):
        """
        按action_type获取ActionUnit
        """
        return self.repository.get_by_action_type(action_type)
    
    def get_by_id(self, action_unit_id: str):
        """
        通过ID获取ActionUnit
        """
        return self.repository.get_by_id(action_unit_id)
    
    def delete_actionUnit(self, action_unit_id: str):
        """
        删除ActionUnit
        """
        self.repository.delete(action_unit_id)
    