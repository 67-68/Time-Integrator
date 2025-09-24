from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.detector.model.model import Detector_Recipe
from ti.features.intervention.model.model import INV_Contract, INV_Contract_Recipe
from ti.services.realTimeMonitor import Monitor_Pack, RealTimeMonitor
from ti.features.detector.model.detectorFactory import DetectorFactory


class INV_ContractRegister:
    def __init__(
        self,
        monitor: RealTimeMonitor,
        rep: DetectorRepository,
        detector_factory: DetectorFactory
        ):
        """
        这个类用来登记contract到monitor
        """
        self.monitor = monitor
        self.rep = rep
        self.detector_factory = detector_factory
        self.registedContract = {}
        
        # 为intervention模块创建默认线程
        self.thread_id = "intervention_default"
        self._ensure_thread_exists()
    
    def _ensure_thread_exists(self):
        """确保intervention线程存在"""
        try:
            self.monitor.create_thread(self.thread_id, self.detector_factory)
            print(f"[INV_ContractRegister] Created thread: {self.thread_id}")
        except ValueError:
            # 线程已存在，继续使用
            print(f"[INV_ContractRegister] Thread {self.thread_id} already exists")
    
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
        
        # 使用线程API添加监控项目
        self.monitor.add_monitor_to_thread(self.thread_id, monitor_pack)
        
        self.registedContract[contract.contract_category_id] = None
        print(f"{contract.contract_category_id}被登记进入监视器线程{self.thread_id}")
