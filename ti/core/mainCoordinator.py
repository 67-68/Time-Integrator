from ti.features.capture.capture_plugin import CapturePlugin
from ti.presenters.page_presenter import PagePresenter
from ti.services.page_factory import PageFactory
from ti.features.insight.insight_plugin import InsightPlugin
from ti.features.insight.presenter.cardPresenter import InsightPresenter
from ti.features.menu.menu_plugin import MenuPlugin
from ti.services.symbol_service import SymbolService
from ti.view.BasicDialog import BasicDialog
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader
from ti.features.intervention.interventionPlugin import InterventionPlugin
from ti.features.detector.detector_plugin import DetectorPlugin
from ti.services.serviceContainer import ServiceContainer
from ti.view.MainWindow import MainWindow

class MainCoorinator():
    def __init__(
        self,
        service: ServiceContainer,  # <-- 应该传入一个实例
        main_window: MainWindow,
        ui: dict # <--- 所有UI的包
    ):
        
        self.service = service
        self.ui = ui
        self.main_window = main_window
        self.presenter = {}
        
        self.bus: EventBus = self.service.getService("bus")
    
        # 添加界面
        self.add_page("analysis")
        self.add_page("capture")
        self.add_page("menu")
        self.main_window.set_page("capture")
    
        self.create_state()
        self.activate_symbol_service()
        
        
        # 插件加载先于业务逻辑
        self.activatePlugins()
    
        # 监测事件
        self.bus.subscribe("dialog_needed",self.show_dialog)
        self.bus.subscribe("end_dialog",self.end_dialog)
        self.bus.subscribe("change_page",self._on_mainWindow_change_page)
    
    def _on_mainWindow_change_page(self,page_name):
        self.main_window._on_page_switch_button_clicked(page_name)
    
    def create_state(self):
        self.controller = {}
        self.loader:DynamicExtensionLoader = self.service.getService("loader")
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
        plugins = [DetectorPlugin,MenuPlugin,CapturePlugin,InsightPlugin,InterventionPlugin]
        
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
        if registers:
            for register in registers:
                self.symbol.regist_register(register)
                print(f"[SYM]Registered {register}")
            
            
    def add_page(self,page_name):
        fac:PageFactory = self.service.getService("page_factory")
        page = fac.create_page(page_name,self.main_window)
        self.main_window.add_page(page)
        
        name = page.page_name
        presenter = PagePresenter(self.bus,page)
        presenter.initialize()
        self.presenter[name] = presenter
        
        
