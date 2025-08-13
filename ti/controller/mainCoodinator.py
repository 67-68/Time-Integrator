from ti.controller.cardController import CardController
from ti.services.serviceContainer import ServiceContainer


class MainCoodinator():
    def __init__(
        self,
        service: ServiceContainer,  # <-- 应该传入一个实例
        ui: dict # <--- 所有UI的包
    ):
        # 获取服务
        self.service = service
        
        # 获取UI
        self.ui = ui
        self.AP = ui["AP"]
        
        # 创建下辖的controller
        self.card_controller = CardController(service,self.AP)

        self.controller = {}
        self.controller["CCT"] = self.card_controller
        
        # 初始化卡片
        self.card_controller.create_yesterday_report()
        
    def getController(self,controller):
        """_summary_
        return a single controller
        available: 
        
        CardController: CCT
        
        Args:
            controller (str): controller name
        """
        return self.controller[controller]