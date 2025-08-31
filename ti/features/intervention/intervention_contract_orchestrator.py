
from ti.core.eventBus import EventBus
from ti.domain.detector.model import Detector_Recipe
from ti.features.intervention.model.contractRecipeRepository import INV_CON_Recipe_Repository
from ti.features.intervention.model.contractRepository import INV_ContractRepository
from ti.features.intervention.model.view_repository import INV_Card_Repository
from ti.features.intervention.service.cardFactory import INV_Card_Factory
from ti.features.intervention.service.contractService import INV_ContractService
from ti.features.intervention.service.register import INV_ContractRegister
from ti.services.realTimeMonitor import RealTimeMonitor
from PyQt6.QtCore import pyqtSignal, QObject

class INV_Contract_Orchestrator(QObject):
    contract_activated = pyqtSignal(str)
    
    def __init__(
        self,
        con_recipe_repos: INV_CON_Recipe_Repository,
        contract_service: INV_ContractService,
        contract_repository: INV_ContractRepository,
        register: INV_ContractRegister,
        bus: EventBus,
        parent = None,
    ):
        super().__init__(parent)
        
        self.recipe_repos = con_recipe_repos
        self.service = contract_service
        self.contract_rep = contract_repository
        self.register = register
        self.bus = bus
        
        # 首先加载出来
        contracts = self.contract_rep.load()
        passed_contracts = {}
        
        # 然后检查是否过期
        for contract in contracts:
            pastDue = contract_service.contract_duration_check(contract) 
            if pastDue:
                contract_service.log_contract(contract)
            else:
                contract_id = contract.contract_uuid
                passed_contracts[contract_id] = contract
            
        # 最后保存回去
        self.contract_rep.save(passed_contracts)
    
    def create_contract(
        self,
        contract_id,
        detector_recipe: str
    ):
        """
        这个方法用来在初始化的使用动态创建contract
        首先它会检查是否已经存在
        如果不存在再根据配方创建

        Args:
            contract_id (_type_): _description_
        """
        # 加载contract
        contract = self.contract_rep.get_by_id(contract_id)
        if not contract:
            recipe = self.recipe_repos.get_recipe_by_id(contract_id)
            contract = self.service.create_new_contract(recipe)
        
        # 送进monitor监视
        self.register.add_monitor_project(contract,detector_recipe)
        
        
        # 它来负责监视这个monitor的产出，eventbus 对应的id
        self.connect_signal(contract_id)
    
    def connect_signal(self,contract_id): #这里应该是contract id吗？还是其他id
        self.bus.subscribe(f"{contract_id}_pattern_detected",self._on_pattern_detected)
    
    def _on_pattern_detected(self,contract_id):
        """
        这个方法用来呈现模态窗口
        首先它会通过contract id获取对应的view id
        然后通过card factory 创建对应的卡片
        card factory对于这个应该有一个专门的方法
        把卡片添加进presenter
        presenter也要有方法
        
        或者，直接上报coordinator
        Args:
            contract_id (_type_): _description_
        """
        contract_recipe = self.recipe_repos.get_recipe_by_id(contract_id)
        view_id = contract_recipe.view_recipe_id
        
        self.contract_activated.emit(view_id)
        
        
        
        
        
        
        
        
        
        