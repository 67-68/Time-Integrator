from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.Interfaces.page_extension_interface import IPageExtension
from ti.core.Interfaces.path_register_provider_interface import IPathRegisterProvider
from ti.core.loggerService import LoggerService
from ti.model.core_pages import CoreView
from ti.model.page_contributions import PageContribution


class MenuPlugin(
    IPathRegisterProvider,
    IPageExtension
):
    def __init__(self):
        super().__init__()
        
        # 创建logger
        self.logger = LoggerService("./ti/features/Menu", "Menu")
        self.logger.log("初始化", "MenuPlugin初始化完成")
    
    def initialize(self, eventBus):
        self.bus = eventBus
        self.bus.publish("PagePluginRegistered", self.page_contributions)
        self.logger.log("事件总线", "事件总线初始化完成并发布页面插件注册事件")
    
        
    def shutdown(self):
        self.logger.log("关闭", "MenuPlugin正在关闭")
        return super().shutdown()
    
    @property
    def name(self):
        return "menu"
    
    @property
    def page_contributions(self):
        """
        用来存储这个类有什么自定义的界面
        以及它们会被放到哪里

        Returns:
            list[PageContribution]: _description_
        """
        parent_page = CoreView.MENU_PAGE.value
        page_id = "Menu_view"
        navigation_name = "欢迎界面"
        
        Menu_plugin_page = PageContribution(
            page_id,
            navigation_name,
            parent_page,
            create_page_callback=self.create_page
        )
        
        return [Menu_plugin_page]
    
    
    def create_page(self, page_id):
        if page_id == "Menu_view":
            return self.create_Menu_view()
        
        
    def create_Menu_view(self):
        self.logger.log("创建视图", "开始创建欢迎视图")
        # 创建一个空的menuView返回
        
        return MenuPage()
    
    @staticmethod
    def register_class():
        # 返回一个空的路径注册器
        class MenuPathRegister:
            pass
        
        return MenuPathRegister