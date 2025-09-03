from datetime import datetime
from ti.features.intervention.model.contract_log_repository import INV_ContractLogRepository
from ti.features.intervention.model.model import INV_Contract, INV_ContractLog


class InterventionLogger:
    """
    这个文件用来管理和创建Intervention的历史数据
    负责将 Contract 转换为 ContractLog 并存储
    """
    def __init__(self, log_repository: INV_ContractLogRepository = None):
        self.log_repository = log_repository or INV_ContractLogRepository()
    
    def log_contract(self, contract: INV_Contract, completion_reason: str = "completed"):
        """
        将 Contract 转换为 Log 并存储
        
        Args:
            contract: 要归档的合同
            completion_reason: 完成原因 ("completed", "timeout", "abandoned")
        """
        contract_log = self._convert_contract_to_log(contract, completion_reason)
        self.log_repository.add_log(contract_log)
        print(f"Contract {contract.contract_uuid} 已归档为 Log {contract_log.log_id}")
        return contract_log.log_id
    
    def _convert_contract_to_log(self, contract: INV_Contract, completion_reason: str) -> INV_ContractLog:
        """
        内部方法：将 Contract 转换为 ContractLog
        """
        now = datetime.now()
        
        contract_log = INV_ContractLog(
            original_contract_id=contract.contract_uuid,
            log_category_id=f"{contract.contract_category_id}_log",  
            original_contract_category_id=contract.contract_category_id,
            user_id="default_user",
            
            created_at=contract.create_time,
            willingness_decision_at=None,
            execution_triggered_at=None, 
            resolved_at=now,
            
            final_willingness_status=self._get_willingness_status(contract),
            final_execution_status=completion_reason,
            
            willingness_notes=None,
            execution_notes=None,
            trigger_context=None
        )
        
        return contract_log
    
    def _get_willingness_status(self, contract: INV_Contract) -> str:
        """获取用户意愿状态"""
        if contract.current_state in ["agreed", "completed"]:
            return "accepted"
        elif contract.current_state == "declined":
            return "declined"
        else:
            return "unknown"