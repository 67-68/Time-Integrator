from dataclasses import dataclass
from ti.core.analysis.matchers import Matcher
from ti.features.intervention.model.model import INV_Contract
from ti.features.intervention.model.repository import INV_Card_Repository
from ti.services.realTimeMonitorService import RealTimeMonitor


class ContractRegister:
    def __init__(
        self,
        monitor: RealTimeMonitor,
        repository: INV_Card_Repository
        ):
        """
        这个类用来登记contract到monitor
        """
        self.monitor = monitor
        self.rep = repository
        self.registedContract = {}
    
    def add_monitor_project(self,contract: INV_Contract):
        # 这里需要获取Detector的Hook, 从配方中
        recipe = self.rep.get_recipe_by_id(contract.recipe_id)
        hook = recipe.detector.config.sequence.hook
        
        monitor_pack = INV_Monitor_Pack(contract.contract_id,hook)
        self.monitor.add_monitor_project()
        
        self.registedContract[contract.contract_id] = None
        print(f"{contract.contract_id}被登记进入监视器")
        
    
@dataclass
class INV_Monitor_Pack:
    contract_uuid: str
    hook: list[Matcher]