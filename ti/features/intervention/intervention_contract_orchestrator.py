
from ti.core.eventBus import EventBus
from ti.features.intervention.model.contractRecipeRepository import INV_CON_Recipe_Repository
from ti.features.intervention.model.contractRepository import INV_ContractRepository
from ti.features.intervention.model.model import INV_Contract, INV_Contract_State, INV_Special_States
from ti.features.intervention.model.view_repository import INV_Card_Repository
from ti.features.intervention.presenter.cardPresenter import INV_State_Publish
from ti.features.intervention.service.contractService import INV_ContractService
from ti.features.intervention.service.register import INV_ContractRegister

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
        view_recipe_repos: INV_Card_Repository,
        parent = None,
    ):
        super().__init__(parent)
        
        self.recipe_repos = con_recipe_repos
        self.service = contract_service
        self.contract_rep = contract_repository
        self.register = register
        self.bus = bus
        self.view_recipe_repos = view_recipe_repos
        
        self.runLifeCycle_all()
        self.connect_signal()
        
        # TODO: 把所有active contract的状态
        # 在检查如果没有过期之后
        # 初始化为agreed, 或者干脆重新注册一遍
    
    def create_contract(
        self,
        contract_id,
        detector_recipe_id: str
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
            contract.detector_recipe_id = detector_recipe_id
            self.contract_rep.add_contract(contract)
        

    
    def connect_signal(self):
        """
        这个函数用来监视monitor
        和presenter状态转换

        Args:
            contract_id (_type_): _description_
        """
        self.bus.subscribe("intervention_state_created",self._on_state_created)
    
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
    
    def _on_state_created(self,publish_pack: INV_State_Publish):
        special_states = publish_pack.special_state
        view_id = publish_pack.recipe.view_id
        print(f"accept special states:{special_states}from {view_id}")
        contract = self.contract_rep.get_by_view_id(view_id)
        
        # 处理special states
        for state in special_states:
            # 之后用对应表，现在直接if
            if state == INV_Special_States.ACCEPTED_CONTRACT.value:
                self._on_contracted_activated(contract)
                self.runLifeCycle(contract)
                
    def runLifeCycle_all(self):
        """
        这个函数检查是否有不符合其状态的contract
        在修改完之后调用
        进行各种必要的检查
        会返回符合条件的contract
        不负责保存！
        """
        # 首先加载出来
        contracts = self.contract_rep.load()
        passed_contracts = {}
        
        # 然后进行生命周期检查
        for contract_id in contracts:
            contract = contracts[contract_id]
            contract = self.runLifeCycle(contract) #在这里出错了，contract是uuid而不是contract类
            if contract:
                contract_id = contract.contract_uuid
                passed_contracts[contract_id] = contract
                
        self.contract_rep.save(passed_contracts)
    
    def runLifeCycle(self,contract) -> INV_Contract:
        """
        进行各种必要的检查
        会返回contract
        如果符合条件
        代处理不符合条件的contract
        不负责保存！
        在修改完成之后需要手动更新

        Args:
            contract (_type_): _description_

        Returns:
            bool: _description_
        """
        pastDue = self.service.contract_duration_check(contract) 
        if pastDue:
            self.service.log_contract(contract)
            return 
        
        # 检查是否有效 
        # active同时Timespan符合要求 
        # 自动注册到monitor
        need_monitored = self.service.contract_active_check(contract)
        if need_monitored: 
            self.add_contract_to_monitor(contract)
            
        # 最后保存回去
        self.contract_rep.add_contract(contract)
    
    def _on_contracted_activated(self,contract: INV_Contract):
        contract.current_state = INV_Contract_State.AGREED.value
    
    def add_contract_to_monitor(self,contract: INV_Contract):
        detector_recipe_key = contract.detector_recipe_id
        contract_id = contract.contract_category_id
        self.register.add_monitor_project(contract,detector_recipe_key)
        
        # 它来负责监视这个monitor的产出，eventbus 对应的id
        self.connect_monitor_signal(contract_id)
    
    def connect_monitor_signal(self,contract_id):
        self.bus.subscribe(f"{contract_id}_pattern_detected",self._on_pattern_detected)
        