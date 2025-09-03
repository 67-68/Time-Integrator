from datetime import datetime
from ti.core.Interfaces.jsonRepositoryInterface import JsonRepositoryInterface
from ti.dataAccess.dataAccess import getData, saveData
from ti.features.intervention.model.model import INV_ContractLog


class INV_ContractLogRepository(JsonRepositoryInterface):
    def __init__(self):
        """
        存储已归档的contract日志
        管理干涉的历史记录
        """
        self.logs = {}
        self.logs = self.load()
        super().__init__()

    @property
    def filePath(self):
        return "ti/features/intervention/model/logs.json"
    
    def save(self, data: dict[str, INV_ContractLog] = None):
        """
        一次性保存所有日志数据
        """
        if data is not None:
            self.logs = data
        
        raw_data = {
            log_id: log.to_dict() 
            for log_id, log in self.logs.items()
        }
        
        saveData(raw_data, self.filePath)
        print(f"保存了干涉日志数据，共 {len(raw_data)} 条记录")
    
    def load(self) -> dict[str, INV_ContractLog]:
        """
        从文件加载所有日志数据
        """
        try:
            raw_data = getData(self.filePath)
            for log_id, log_dict in raw_data.items():
                if log_dict:
                    self.logs[log_id] = INV_ContractLog.from_dict(log_dict)
        except Exception as ex:
            print(f"加载干涉日志失败: {ex}")
            self.logs = {}
        
        return self.logs
    
    def add_log(self, log: INV_ContractLog):
        """
        添加新的日志记录
        自动保存
        """
        self.logs[log.log_id] = log
        print(f"添加干涉日志: {log.log_id}")
        self.save()
        
    def get_by_id(self, log_id: str) -> INV_ContractLog | None:
        """
        通过日志ID获取记录
        """
        import copy
        log = self.logs.get(log_id)
        return copy.deepcopy(log) if log else None

    def get_all(self) -> dict[str, INV_ContractLog]:
        """
        获取所有日志记录
        """
        import copy
        return copy.deepcopy(self.logs)
        
    def delete(self, log_id: str):
        """
        删除指定的日志记录
        """
        if log_id in self.logs:
            del self.logs[log_id]
            self.save()
            print(f"删除干涉日志: {log_id}")
        else:
            print(f"未找到日志记录: {log_id}")
    
    def get_by_category(self, category_id: str) -> list[INV_ContractLog]:
        """
        按原始contract类别获取日志记录
        """
        return [
            log for log in self.logs.values() 
            if log.original_contract_category_id == category_id
        ]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> list[INV_ContractLog]:
        """
        按日期范围获取日志记录
        """
        return [
            log for log in self.logs.values()
            if start_date <= log.created_at <= end_date
        ]