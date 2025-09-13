from ti.features.capture.capture_plugin import CapturePlugin
from ti.features.core_capture.CapturePage import New_CapturePage
from ti.features.detector.detector_path_register import DetectorPathRegister
from ti.features.insight.insight_path_register import InsightPathRegister
from ti.features.insight.presenter.cardPresenter import CardPresenter
from ti.model.model_path_register import CorePathRegister
from ti.presenters.capture_page_presenter import CapturePagePresenter
from ti.services.symbol_service import SymbolService
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
        
        self.activate_symbol_service()
        
        # 插件加载先于业务逻辑
        self.activatePlugins()
        
        # 初始化卡片
        self.card_controller.create_yesterday_report()
        
        # 监测事件
        self.bus.subscribe("dialog_needed",self.show_dialog)
        self.bus.subscribe("end_dialog",self.end_dialog)
        
    def create_state(self):
        self.controller = {}
        
        self.AP = self.ui["AP"]
        insight_card_recipe_rep = self.service.getService
        self.card_controller = CardPresenter(self.service,self.AP,insight_card_recipe_rep)
        self.controller["CCT"] = self.card_controller
        
        self.loader:DynamicExtensionLoader = self.service.getService("loader")
        
        self.bus: EventBus = self.service.getService("bus")
        
        self.symbol: SymbolService = self.service.getService("symbol")
        
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
        plugins = [CapturePlugin,InterventionPlugin]
        
        self.loader.discover_and_register_plugins(plugins)
        
    def show_dialog(self,ui):
        self.dialog = BasicDialog(ui,parent=self.ui["MW"])
        self.dialog.show()
        
    def end_dialog(self,view_id):
        self.dialog.close()
        
    def activate_symbol_service(self):
        """
        这个函数用来激活symbol service
        """
        
        
        registers = self.loader.get_registers()
        
        # 创建核心的register
        registers.append(InsightPathRegister())
        registers.append(CorePathRegister())
        registers.append(DetectorPathRegister())
        

        
        if registers:
            for register in registers:
                self.symbol.regist_register(register)
                print(f"[SYM]Registered {register}")
                
