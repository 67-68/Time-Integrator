from datetime import datetime, timedelta
from ti.features.intervention.model.contractRecipeRepository import INV_CON_Recipe_Repository
from ti.features.intervention.model.contractRepository import INV_ContractRepository
from ti.features.intervention.model.model import INV_Contract, INV_Contract_Recipe, INV_Contract_State, INV_Contract_Duration
from ti.features.intervention.service.logger import InterventionLogger
from ti.features.intervention.service.register import INV_ContractRegister


class INV_ContractService:
    def __init__(
        self,
        contract_repository: INV_ContractRepository,
        con_recipe_repos: INV_CON_Recipe_Repository,
        register: INV_ContractRegister,
        logger: InterventionLogger
    ):
        """
        这个类封装所有和Contract相关的服务
        """
        self.logger = logger
        self.contract_rep = contract_repository
        self.recipe_repos = con_recipe_repos
        self.register = register
    
    def create_new_contract(
        self,
        contractRecipe: INV_Contract_Recipe,
    ) -> INV_Contract:
        # 首先获取需要的信息
        contract_category_id = contractRecipe.contract_recipe_id
        duration = contractRecipe.duration
        view_recipe_id = contractRecipe.view_recipe_id
        
        # 然后创建
        contract = INV_Contract(
            contract_category_id=contract_category_id,
            duration= duration,
            current_state= INV_Contract_State.BEFORE_START.value,
            view_recipe_id = view_recipe_id,
        )
        
        return contract
    
    def _log_contract(self,contract:INV_Contract):
        """_summary_
        这个类用来归档contract.
        它会调用(还没写)logger
        Args:
            contract (INV_Contract): _description_
        """
        self.logger.log_contract(contract)
    
    def contract_duration_check(self, contract: INV_Contract) -> bool:
        """
        这个类用来检查是否contract应该被归档
        返回True表示已过期，需要归档

        Args:
            contract (INV_Contract): 要检查的合同
            
        Returns:
            bool: True表示已过期需要归档
        """
        now = datetime.now()
        created_time = contract.create_time
        duration_type = contract.duration
        
        if duration_type == INV_Contract_Duration.TODAY.value:
            # 如果是今天，检查是否已过午夜
            next_day = created_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            return now >= next_day
            
        elif duration_type == INV_Contract_Duration.TO_TOMORROW.value:
            # 到明天，即创建后24小时
            expire_time = created_time + timedelta(days=1)
            return now >= expire_time
            
        elif duration_type == INV_Contract_Duration.THIS_WEEK.value:
            # 到本周末（周日午夜）
            days_until_sunday = (6 - created_time.weekday()) % 7
            if days_until_sunday == 0:
                days_until_sunday = 7
            week_end = created_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_sunday)
            return now >= week_end
            
        else:
            # 未知的duration类型，默认为不过期
            print(f"未知的duration类型: {duration_type}")
            return False

    def contract_active_check(self,contract: INV_Contract) -> bool:
        """
        这个方法用来检查是否contract需要被添加进monitor
        它不负责检查是否contract过期了

        Args:
            contract (INV_Contract): _description_
        """
        # 检查是否agreed 但不是active
        # TODO: 或许我需要把matchers 也给contract设计
        return contract.current_state == INV_Contract_State.AGREED.value
        
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
    
    def runLifeCycle(self,contract: INV_Contract) -> INV_Contract:
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
        pastDue = self.contract_duration_check(contract) 
        if pastDue:
            self._log_contract(contract)
            self.contract_rep.delete(contract)
            return 
        
        # 检查是否有效 
        # active同时Timespan符合要求 
        # 自动注册到monitor
        need_monitored = self.contract_active_check(contract)
        if need_monitored: 
            self.add_contract_to_monitor(contract)
            
        # 最后保存回去
        self.contract_rep.add_contract(contract)
    
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
            contract = self.create_new_contract(recipe)
            contract.detector_recipe_id = detector_recipe_id
            self.contract_rep.add_contract(contract)
            
    def add_contract_to_monitor(self,contract: INV_Contract):
        detector_recipe_key = contract.detector_recipe_id
        self.register.add_monitor_project(contract,detector_recipe_key)
        