from ti.presenters.cardPresenter import CardPresenter
from ti.view.views.BasicDialog import BasicDialog
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader, ExtensionRegister
from ti.features.intervention.interventionPlugin import InterventionPlugin
from ti.services.serviceContainer import ServiceContainer


class MainCoorinator():
    def __init__(
        self,
        service: ServiceContainer,  # <-- 应该传入一个实例
        ui: dict # <--- 所有UI的包
    ):
        
        self.service = service
        self.ui = ui
    
        self.create_state()
        
        # 插件加载先于业务逻辑
        self.activatePlugins()
        
        # 初始化卡片
        self.card_controller.create_yesterday_report()
        
        # 监测事件
        self.bus.subscribe("dialog_needed",self.show_dialog)
        
    def create_state(self):
        self.controller = {}
        
        self.AP = self.ui["AP"]
        self.card_controller = CardPresenter(self.service,self.AP)
        self.controller["CCT"] = self.card_controller
        
        self.loader:DynamicExtensionLoader = self.service.getService("loader")
        
        self.bus: EventBus = self.service.getService("bus")
        
    def getController(self,controller):
        """_summary_
        return a single controller
        available: 
        
        CardController: CCT
        
        Args:
            controller (str): controller name
        """
        return self.controller[controller]
    
    def activatePlugins(self):
        """_summary_
        这个函数创建插件的实例并激活他们
        """        
        plugins = [InterventionPlugin]
        
        self.loader.discover_and_register_plugins(plugins)
        
    def show_dialog(self,ui):
        dialog = BasicDialog(ui,parent=self.ui["MW"])
        result = dialog.exec()
        
        