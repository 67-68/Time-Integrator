from ti.model.strategy.strategy_contribution import StrategyContribution


class StrategyRepository:
    """
    用来登记注册Strategy
    """
    _instance = None
    
    def __init__(self):
        self._strategies = {}
    
    def register_strategy(self,contri: StrategyContribution):
        print(f"[STRA_REPO]receive strategy {contri.strategy_id}")
        if not hasattr(self,"_strategies"):
            self._strategies = {}
            
        self._strategies[contri.strategy_id] = contri.strategy
    
    def get_strategy(self,protocol):
        print(f"[STRA_REPO]receive strategy request {protocol}")
        for id,cls in self._strategies.items():
            if isinstance(cls,protocol):
                print(f"[STRA_REPO]find match strategy {cls}")
                return cls #目前第一个就返回，以后可能返回一个列表
        print("[STRA_REPO]Not find any strategy matching")
        
    def get_all_strategy_from_protocol(self,protocol):
        strategies = []
        print(f"[STRA_REPO]receive strategy request {protocol}")
        for id,cls in self._strategies.items():
            if isinstance(cls,protocol):
                print(f"[STRA_REPO]find match strategy {cls}")
                strategies.append(cls) #目前第一个就返回，以后可能返回一个列表
        print(f"[STRA_REPO]find {len(strategies)} strategies matching")
        return strategies
    
    @classmethod
    def get_instance(cls):
        """
        返回全局变量
        给装饰器使用

        Returns:
            _type_: _description_
        """
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance

        
    