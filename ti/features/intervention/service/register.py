from ti.core.definitions import Monitor_Pack

from ti.domain.detector.detectorRepository import DetectocRepository
from ti.domain.detector.model import Detector_Recipe
from ti.features.intervention.model.model import INV_Contract, INV_Contract_Recipe
from ti.services.realTimeMonitor import RealTimeMonitor


class INV_ContractRegister:
    def __init__(
        self,
        monitor: RealTimeMonitor,
        rep: DetectocRepository
        ):
        """
        这个类用来登记contract到monitor
        """
        self.monitor = monitor
        self.rep = rep
        self.registedContract = {}
        
    
    def add_monitor_project(
        self,
        contract: INV_Contract,
        detector_recipe_key: str
    ):
        
        detector_recipe = self.rep.get_recipe_by_id(detector_recipe_key)
        
        hook_matchers = detector_recipe.config.sequence.hook
        
        monitor_pack = Monitor_Pack(
            contract.contract_category_id, #理论上来说是contract id
            hook_matchers
        )
        
        self.monitor.add_monitor_project(monitor_pack)
        
        self.registedContract[contract.contract_category_id] = None
        print(f"{contract.contract_category_id}被登记进入监视器")
