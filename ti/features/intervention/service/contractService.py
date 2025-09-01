from ti.features.intervention.model.model import INV_Contract, INV_Contract_Recipe, INV_Contract_State


class INV_ContractService:
    def __init__(self):
        """
        这个类封装所有和Contract相关的服务
        """
        pass
    
    def create_new_contract(
        self,
        contractRecipe: INV_Contract_Recipe
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
    
    def log_contract(self,contract:INV_Contract):
        """_summary_
        这个类用来归档contract.
        它会调用(还没写)logger
        Args:
            contract (INV_Contract): _description_
        """
        pass
    
    def contract_duration_check(self,contract: INV_Contract):
        """
        这个类用来检查是否contract应该被归档

        Args:
            contract (INV_Contract): _description_
        """
        # 大概就是找出duration和创建时间匹配一下
        pass

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
        
        