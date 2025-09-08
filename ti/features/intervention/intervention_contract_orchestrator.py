
from ti.core.eventBus import EventBus
from ti.features.intervention.model.contractRecipeRepository import INV_CON_Recipe_Repository
from ti.features.intervention.model.contractRepository import INV_ContractRepository
from ti.features.intervention.model.model import INV_Contract, INV_Contract_Recipe, INV_Contract_State, INV_Special_States
from ti.features.intervention.presenter.cardPresenter import INV_State_Publish
from ti.features.intervention.service.contractService import INV_ContractService


from PyQt6.QtCore import pyqtSignal, QObject

class INV_Contract_Orchestrator(QObject):
    contract_activated = pyqtSignal(str)
    
    def __init__(
        self,
        con_recipe_repos: INV_CON_Recipe_Repository,
        contract_service: INV_ContractService,
        contract_repository: INV_ContractRepository,
        bus: EventBus,
        parent = None,
    ):
        super().__init__(parent)
        
        self.recipe_repos = con_recipe_repos
        self.service = contract_service
        self.contract_rep = contract_repository
        self.bus = bus
        
        self.service.runLifeCycle_all()
        self.connect_signal()
        
        # TODO: 把所有active contract的状态
        # 在检查如果没有过期之后
        # 初始化为agreed, 或者干脆重新注册一遍
        
    def connect_signal(self):
        """
        这个函数用来监视presenter状态转换

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
        if not special_states:
            return
        for state in special_states:
            # 之后用对应表，现在直接if
            if state == INV_Special_States.ACCEPTED_CONTRACT.value:
                # 表明用户有意愿参与，修改contract状态
                self._on_contracted_activated(contract) # 也就是说，我在这里使用了一个lifeCycle来自动添加，但是并没有函数来连接信号
                contract_id = contract.contract_category_id
                self.bus.subscribe(f"{contract_id}_pattern_detected",self._on_pattern_detected)
                print(f"subscribe {contract_id}_pattern_detected ")
            if state == INV_Special_States.END_INTERVENTION.value:
                self.bus.publish("end_dialog",view_id)
                # 归档
                contract.current_state = INV_Contract_State.COMPLETE.value
                self.service.runLifeCycle(contract)
    
    # 也就是说，过去的历史数据被添加了?但是当前的没有被添加——添加函数压根没被调用
    
    def _on_contracted_activated(self,contract: INV_Contract):
        contract.current_state = INV_Contract_State.AGREED.value
        self.service.runLifeCycle(contract)
    
    def add_contract_to_monitor(self,contract: INV_Contract):
        contract_id = contract.contract_category_id
        self.service.add_contract_to_monitor(contract)
        
        # 它来负责监视这个monitor的产出，eventbus 对应的id
        self.bus.subscribe(f"{contract_id}_pattern_detected",self._on_pattern_detected)
        print(f"subscribe {contract_id}_pattern_detected ")
        

    def create_contract(
        self,
        contract_id,
        detector_recipe_id: str
    ) -> INV_Contract:
        self.service.create_contract(contract_id,detector_recipe_id)
        