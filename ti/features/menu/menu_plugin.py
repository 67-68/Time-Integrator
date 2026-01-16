from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.services.loggerService import LoggerService
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt6.QtCore import Qt
from ti.services.serviceContainer import ServiceContainer
from ti.features.menu.view.time_pie_chart import TimePieChart
from ti.features.menu.presenter.menu_presenter import MenuPresenter


class MenuPlugin(
    IPageExtension
):
    def __init__(self):
        super().__init__()
        
        # 创建logger
        self.logger = LoggerService("./ti/features/menu", "Menu")
        self.logger.log("初始化", "MenuPlugin初始化完成")
        
        # 初始化presenter
        self.presenter = None
    
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
        self.logger.log("创建视图", "开始创建菜单视图")
        
        # 创建自定义的菜单视图
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)
        
        # 添加上面的欢迎标签
        welcome_label = QLabel("欢迎来到TI")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(welcome_label)
        
        # 添加时间分析组件
        self.setup_time_analysis_section(layout)
        
        return menu_widget
    
    def setup_time_analysis_section(self, layout):
        """设置时间分析部分"""
        # 获取数据服务
        service_container = ServiceContainer()
        data_service = service_container.getService("DS")
        
        # 创建presenter
        self.presenter = MenuPresenter(data_service)
        
        # 创建饼图
        pie_chart = TimePieChart()
        self.presenter.set_pie_chart(pie_chart)
        
        # 设置时间范围改变回调
        pie_chart.set_time_range_changed_callback(self.presenter.set_time_range)
        
        # 添加饼图到布局
        layout.addWidget(pie_chart)
        
        # 添加刷新按钮
        refresh_button = QPushButton("刷新时间分析")
        refresh_button.clicked.connect(self.presenter.refresh_data)
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(refresh_button)
        
        # 自动分析数据
        self.presenter.analyze_yesterday_time()