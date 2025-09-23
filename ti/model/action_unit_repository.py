from datetime import datetime
from typing import Dict, List, Optional
from ti.core.Interfaces.view.json_repository_interface import IJsonRepository
from ti.services.dataAccess import getData, saveData
from ti.model.action_unit import ActionUnit


class ActionUnitRepository(IJsonRepository):
    def __init__(self):
        """
        ActionUnit 数据仓库
        管理按日期组织的行动单元数据
        """
        self.data: Dict[str, List[ActionUnit]] = {}
        self.data = self.load()
        super().__init__()

    @property
    def filePath(self):
        return "model/data/dateData.json"
    
    def save(self, data: Dict[str, List[ActionUnit]] = None):
        """
        保存所有日期的ActionUnit数据
        """
        if data is not None: # 这里传入的数据有问题
            print("[DATA]somebody save a blank data")
            self.data = data
            
        
        # 转换为JSON格式
        raw_data = {}
        for date_str, action_units in self.data.items():
            raw_data[date_str] = [au.to_dict() for au in action_units]
        
        saveData(raw_data, self.filePath)
        print(f"保存了ActionUnit数据，共 {len(raw_data)} 个日期")
    
    def load(self) -> Dict[str, List[ActionUnit]]:
        """
        从文件加载所有ActionUnit数据
        """
        try:
            raw_data = getData(self.filePath)
            loaded_data = {}
            
            for date_str, action_units_list in raw_data.items():
                loaded_data[date_str] = []
                for au_dict in action_units_list:
                    if au_dict:  # 过滤空数据
                        action_unit = ActionUnit.from_dict(au_dict)
                        loaded_data[date_str].append(action_unit)
            
            self.data = loaded_data
        except Exception as ex:
            print(f"加载ActionUnit数据失败: {ex}")
            self.data = {}
        
        return self.data
    
    def get_by_id(self, action_unit_id: str) -> Optional[ActionUnit]:
        """
        通过ID获取特定的ActionUnit
        """
        for date_str, action_units in self.data.items():
            for au in action_units:
                if au.id == action_unit_id:
                    return au
        return None

    def get_all(self) -> Dict[str, List[ActionUnit]]:
        """
        获取所有ActionUnit数据
        """
        import copy
        return copy.deepcopy(self.data)
        
    def delete(self, action_unit_id: str):
        """
        删除指定ID的ActionUnit
        """
        for date_str, action_units in self.data.items():
            for i, au in enumerate(action_units):
                if au.id == action_unit_id:
                    del self.data[date_str][i]
                    self.save()
                    print(f"删除ActionUnit: {action_unit_id}")
                    return
        print(f"未找到ActionUnit: {action_unit_id}")
    
    def get_by_date(self, date_str: str) -> List[ActionUnit]:
        """
        获取指定日期的所有ActionUnit
        """
        return self.data.get(date_str, [])
    
    def add_action_unit(self, date_str: str, action_unit: ActionUnit):
        """
        向指定日期添加ActionUnit
        """
        if date_str not in self.data:
            self.data[date_str] = []
        
        self.data[date_str].append(action_unit)
        print(f"添加ActionUnit到 {date_str}: {action_unit.action}")
        self.save()
    
    def get_date_range(self, start_date: str, end_date: str) -> Dict[str, List[ActionUnit]]:
        """
        获取日期范围内的所有ActionUnit
        """
        result = {}
        for date_str, action_units in self.data.items():
            if start_date <= date_str <= end_date:
                result[date_str] = action_units
        return result
    
    def get_by_action_type(self, action_type: str) -> List[ActionUnit]:
        """
        按action_type筛选所有ActionUnit
        """
        result = []
        for date_str, action_units in self.data.items():
            for au in action_units:
                if au.action_type == action_type:
                    result.append(au)
        return result
    
    def get_by_action(self, action: str) -> List[ActionUnit]:
        """
        按action名称筛选所有ActionUnit
        """
        result = []
        for date_str, action_units in self.data.items():
            for au in action_units:
                if au.action == action:
                    result.append(au)
        return result