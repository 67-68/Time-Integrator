from ti.UI.presenters.conditional_cardPresenter import Conditional_ReportGenerator
from ti.UI.presenters.fixed_cardPresenter import Fixed_ReportGenerator
from ti.UI.views.analysis.AnalysisPage import AnalysisPage
from ti.assets.card_recipe import Card_recipe
from ti.dataAccess.dataService import DataService
from ti.dataAccess.insightManager import InsightManager
from ti.services.serviceContainer import ServiceContainer
from PyQt6.QtCore import pyqtSignal


class CardPresenter():
    # 创建信号
    card_generated = pyqtSignal(dict)
    
    def __init__(
        self,
        service: ServiceContainer,
        ui: AnalysisPage
    ):
        """_summary_
        专门管理卡片的controller
        管理analysis_page
        受mainCoodinator管辖
        它相当于替代了原本的analysis page的地位
        
        data: 处理的数据，由app类分发
        """
        # 获取服务
        self.service = service
        self.dataService: DataService = service.getService("DS")
        
        # 获取配方
        recipe = Card_recipe()
        cond_recipe = recipe.get_conditional_recipe()
        fixed_recipe = recipe.get_fixed_recipe()
        
        # 获取数据
        self.yesterday_data = self.dataService.get_yesterday_AU()
        
        # 获取传入的服务
        IE = self.service.getService("IE")
        IM = self.service.getService("IM")
        
        # 开始初始化卡片相关
        self.CR = Conditional_ReportGenerator(
            self.yesterday_data,
            cond_recipe,
            IE,
            IM
        )
        
        self.FR = Fixed_ReportGenerator(
            self.yesterday_data,
            fixed_recipe
        )
        
        # 持有卡片状态
        self.cards = {}

        # 绑定UI
        self.ui = ui
        
    def create_yesterday_report(self):
        # 获取固定卡片
        fixed_cards = self.FR.create_report()
        
        # 创建条件卡片
        cond_cards = self.CR.create_report()
        
        # breakpoint()
        
        # 卡片汇总
        self.cards = cond_cards + fixed_cards
    
        # 临时传递，按理来说不应该这么搞. UI + service -> mess
        IS = self.service.getService("IS")
        FS = self.service.getService("FS")
        
        # 填充入GUI
        self.ui.add_cards(self.cards,IS,FS)