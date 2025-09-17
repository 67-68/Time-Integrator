from ti.features.capture.capture_plugin import CapturePlugin
from ti.features.core_capture.CapturePage import New_CapturePage
from ti.features.insight.presenter.cardPresenter import CardPresenter
from ti.services.symbol_service import SymbolService
from ti.view.views.BasicDialog import BasicDialog
from ti.core.eventBus import EventBus
from ti.core.extensionRegister import DynamicExtensionLoader
from ti.features.intervention.interventionPlugin import InterventionPlugin
from ti.services.serviceContainer import ServiceContainer
from ti.features.core_capture.capture_page_presenter import CapturePagePresenter

class MainCoorinator():
    def __init__(
        self,
        service: ServiceContainer,  # <-- 应该传入一个实例
        ui: dict # <--- 所有UI的包
    ):
        
        self.service = service
        self.ui = ui
    
        self.create_state()
        # 替换旧的capture page为新的capture page
        self.replace_capture_page()
        
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
        self.card_controller = CardPresenter(self.service,self.AP)
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
        if registers:
            for register in registers:
                self.symbol.regist_register(register)
                print(f"[SYM]Registered {register}")
    
    def replace_capture_page(self):
        """
        替换旧的capture page为新的capture page
        """
        print("=" * 50)
        print("开始替换capture page")
        print("=" * 50)
        
        # 获取main window实例
        main_window = self.ui["MW"]
        
        # 删除旧的capture page
        self._remove_old_capture_page(main_window)
        
        # 添加新的capture page
        self._add_new_capture_page(main_window)
        
        # 连接新capture page的信号
        self._connect_new_capture_page_signals()
        
        print("=" * 50)
        print("capture page替换完成")
        print("=" * 50)
    
    def _remove_old_capture_page(self, main_window):
        """删除旧的capture page"""
        print("删除旧的capture page...")
        
        # 获取stacked widget
        stacked_widget = main_window.MW.stackedWidget
        
        # 查找旧的capture page
        old_capture_page = None
        for i in range(stacked_widget.count()):
            widget = stacked_widget.widget(i)
            if hasattr(widget, 'objectName') and widget.objectName() == "capturePageBase":
                old_capture_page = widget
                break
        
        if old_capture_page:
            # 从stacked widget中移除
            stacked_widget.removeWidget(old_capture_page)
            # 删除对象
            old_capture_page.deleteLater()
            print("旧的capture page已删除")
        else:
            print("未找到旧的capture page")
    
    def _add_new_capture_page(self, main_window):
        """添加新的capture page"""
        print("添加新的capture page...")
        
        # 创建新的capture page和presenter
        self.new_capture_page = New_CapturePage(main_window)
        self.new_capture_page.setObjectName("capturePageBase")
        
        # 获取event bus
        bus = self.service.getService("bus")
        
        # 创建presenter
        self.capture_page_presenter = CapturePagePresenter(self.new_capture_page, bus)
        
        # 添加到stacked widget
        main_window.MW.stackedWidget.addWidget(self.new_capture_page)
        
        # 更新UI引用
        main_window.CP = self.new_capture_page
        main_window.ui["CP"] = self.new_capture_page
        
        print("新的capture page已添加")
    
    def _connect_new_capture_page_signals(self):
        """连接新capture page的信号"""
        print("连接新capture page的信号...")
        
        # 获取main window实例
        main_window = self.ui["MW"]
        
        # 重新连接信号（因为capture page被替换了）
        main_window.connectSignal()
        
        print("新capture page信号连接完成")
                
