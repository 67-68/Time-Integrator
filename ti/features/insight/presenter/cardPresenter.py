import uuid


from ti.features.insight.presenter.conditional_cardPresenter import Conditional_ReportGenerator
from ti.features.insight.presenter.fixed_cardPresenter import Fixed_ReportGenerator
from ti.features.insight.model.insight_card_recipe_repository import Insight_Card_Recipe_Repository
from ti.core.eventBus import EventBus
from ti.features.insight.presenter.insight_card_presenter import InsightCardPresenter
from ti.features.insight.view.insight_card import InsightCard
from ti.features.insight.view.insight_view import InsightView
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.dataAccess.dataService import DataService
from ti.services.dataAccess.insightManager import InsightManager
from ti.services.engine.insightEngine import InsightEngine
from ti.services.formatter import FormatService
from ti.services.serviceContainer import ServiceContainer
from PyQt6.QtCore import pyqtSignal

from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import FixedCardResult, PresentedCardData
from ti.services.symbol_service import SymbolService


class CardPresenter():
    # 创建信号
    card_generated = pyqtSignal(dict)
    
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService,
        data_service: DataService,
        engine: InsightEngine,
        manager: InsightManager,
        bus: EventBus,
        view: InsightView,
        format: FormatService
    ):
        """_summary_
        专门管理卡片的controller
        管理analysis_page
        受mainCoodinator管辖
        它相当于替代了原本的analysis page的地位
        
        data: 处理的数据，由app类分发
        """    
        # 获取服务
        self.dataService = data_service
        self.cache = SessionCache()
        self.view = view
        self.format = format
        
        # 获取配方
        recipe_repo = Insight_Card_Recipe_Repository(yaml_parser, symbol_service)
        cond_recipe = recipe_repo.get_conditional_recipes()
        fixed_recipe = recipe_repo.get_fixed_recipes()
        
        # 获取数据
        self.yesterday_data = self.dataService.get_yesterday_AU()
        
        # 获取传入的服务
        IE = engine
        IM = manager
        self.bus: EventBus = bus
        
        
        self.currentCards = {}
        self.presenter = {}
        
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
        
    def create_yesterday_report(self) -> list:
        # 获取固定卡片
        fixed_cards = self.FR.create_report(self.cache)
        
        # 创建条件卡片
        cond_cards = self.CR.create_report()
        
        # 卡片汇总
        self.cards = cond_cards + fixed_cards
        
        # 填充入GUI
        cards = self.get_ui_card(self.cards)
        return cards
        
    def get_ui_card(self,cards):
        for idx, card_data in enumerate(cards): # card_data也就是formatter处理后的pre_data
            # 处理不同类型的卡片数据
            if isinstance(card_data, (PresentedCardData, FixedCardResult)):
                # 如果是dataclass对象，转换为字典
                card_dict = {
                    "card_type": card_data.card_type,
                    "judgement_key": card_data.judgement_key,
                    "sementic_key": card_data.sementic_key,
                    "data": card_data.data,
                    "weight": card_data.weight,
                    "id": card_data.id
                }
                # 对于FixedCardResult，添加额外的字段
                if isinstance(card_data, FixedCardResult):
                    card_dict["duration"] = card_data.duration
                    card_dict["card_type_id"] = card_data.card_type_id
                
                data = self.format.format_card(card_dict)
                card_data_for_presenter = card_dict
            else:
                # 如果是字典，直接使用
                data = self.format.format_card(card_data)
                card_data_for_presenter = card_data
            
            card = InsightCard(data, parent=self.view) 
            
            self.bus.publish("insight_card_ui_created",(card,self.cache))
            
            card_data_for_presenter["card_type_id"] = card_data_for_presenter["sementic_key"]
            card_data_for_presenter["card_uuid"] = uuid.uuid4()
            
            self.currentCards[idx] = card
            cardPresenter = InsightCardPresenter(
                self.currentCards[idx]
            )
            
            self.presenter[idx] = cardPresenter
            
            # self.cards.append(self.currentCards[idx])     # 保存引用，防止被垃圾回收
            self.view.add_card(card)