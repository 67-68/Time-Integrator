from ti.features.insight.presenter.conditional_cardPresenter import Conditional_ReportGenerator
from ti.features.insight.presenter.fixed_cardPresenter import Fixed_ReportGenerator
from ti.view.views.analysis.AnalysisPage import AnalysisPage
from ti.features.insight.model.insight_card_recipe_repository import Insight_Card_Recipe_Repository
from ti.core.eventBus import EventBus
from ti.services.dataAccess.dataService import DataService
from ti.services.serviceContainer import ServiceContainer
from PyQt6.QtCore import pyqtSignal

from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import PresentedCardData


class CardPresenter():
    # 创建信号
    card_generated = pyqtSignal(dict)
    
    def __init__(
        self,
        service: ServiceContainer,
        ui: AnalysisPage,
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
        self.cache = SessionCache()
        
        # 获取配方
        yaml_parser = self.service.getService("yaml_parser")
        symbol_service = self.service.getService("symbol")
        recipe_repo = Insight_Card_Recipe_Repository(yaml_parser, symbol_service)
        cond_recipe = recipe_repo.get_conditional_recipes()
        fixed_recipe = recipe_repo.get_fixed_recipes()
        
        # 获取数据
        self.yesterday_data = self.dataService.get_yesterday_AU()
        
        # 获取传入的服务
        IE = self.service.getService("IE")
        IM = self.service.getService("IM")
        self.bus: EventBus = self.service.getService("bus")
        
        # 开始初始化卡片相关
        self.CR = Conditional_ReportGenerator(
            self.yesterday_data,
            cond_recipe,
            IE,
            IM,
            self.cache
        )
        
        self.FR = Fixed_ReportGenerator(
            self.yesterday_data,
            fixed_recipe
        )
        
        # 持有卡片状态
        self.cards: list[PresentedCardData] = []

        # 绑定UI
        self.ui = ui
        
    def create_yesterday_report(self):
        # 获取固定卡片
        fixed_cards = self.FR.create_report(self.cache)
        
        # 创建条件卡片
        cond_cards = self.CR.create_report()
        
        # breakpoint()
        
        FS = self.service.getService("FS")
        
        # 卡片汇总
        self.cards = cond_cards + fixed_cards
        
        # 填充入GUI
        self.ui.add_cards(self.cards,FS,self.bus,self.cache)