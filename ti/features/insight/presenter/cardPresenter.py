import uuid

from ti.core.eventBus import EventBus
from ti.features.insight.model.insight_card_repository import InsightCardRepository
from ti.features.insight.model.insight_event import SaveInsightCard
from ti.features.insight.presenter.insight_card_presenter import InsightPresenter
from ti.features.insight.service.reportGenerationService import ReportGenerationService
from ti.features.insight.service.uiCardFactory import InsightCardFactory
from ti.features.insight.view.insight_card import InsightCard
from ti.features.insight.view.insight_view import InsightView
from ti.services.dataService import DataService
from ti.features.insight.service.formatter import InsightFormatService
from PyQt6.QtCore import pyqtSignal

from ti.features.insight.model.insight_card_generation_models import FixedCardResult, PresentedCardData
from ti.services.loggerService import LoggerService


class InsightPresenter():
    # 创建信号
    card_generated = pyqtSignal(dict)
    
    def __init__(
        self,
        data_service: DataService,
        bus: EventBus,
        view: InsightView,
        format: InsightFormatService,
        report_generation_service: ReportGenerationService,
        ui_card_factory: InsightCardFactory,
        card_repository: InsightCardRepository
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
        self.view = view
        self.bus: EventBus = bus
        self.report_generation_service = report_generation_service
        self.ui_card_factory = ui_card_factory
        self.card_repository = card_repository
        
        # 创建logger
        self.logger = LoggerService("./ti/features/insight", "card_presenter")
        
        # 从报告生成服务获取缓存
        self.cache = self.report_generation_service.cache
        
        # 订阅保存卡片事件
        self.bus.subscribe_event(SaveInsightCard, self._on_save_insight_card)
        
        self.currentCards = {}
        self.presenter = {}
        
        # 持有卡片状态
        self.cards: list[PresentedCardData] = []
        
        self.logger.log("初始化", "卡片Presenter初始化完成")
        
    def create_yesterday_report(self) -> list:
        self.logger.log("报告生成", "开始生成昨日报告")
        
        # 使用报告生成服务创建卡片
        self.cards = self.report_generation_service.create_yesterday_report()
        
        # 填充入GUI
        self.fill_ui_card(self.cards)
        
        # 保存生成的卡片
        self.save_generated_cards(self.cards)
        
        if self.currentCards:        
            self.logger.log("UI渲染", f"成功渲染 {len(self.currentCards)} 张卡片到界面")
        else:
            self.logger.log("UI渲染", f"没有卡片被渲染")
        return self.currentCards
        
    def fill_ui_card(self, cards):
        for idx, card_data in enumerate(cards): # card_data也就是formatter处理后的pre_data
            # 使用UI工厂创建卡片
            ui_result = self.ui_card_factory.create_ui_card(
                card_data, self.view, self.cache
            )
            
            self.currentCards[idx] = ui_result["card"]
            self.presenter[idx] = ui_result["presenter"]
            
            # 保存引用，防止被垃圾回收
            self.view.add_card(ui_result["card"])
    
    def save_generated_cards(self, cards):
        """保存当天生成的卡片"""
        if not cards:
            self.logger.log("卡片保存", "没有卡片需要保存")
            return
        
        try:
            # 转换卡片数据为字典格式并保存
            cards_to_save = [card.to_dict() if hasattr(card, 'to_dict') else card 
                           for card in cards]
            
            self.card_repository.save_today_cards(cards_to_save)
            self.logger.log("卡片保存", f"成功保存 {len(cards)} 张卡片")
            
        except Exception as e:
            self.logger.log("卡片保存错误", f"保存卡片时发生错误: {str(e)}")
    
    def _on_save_insight_card(self, event:SaveInsightCard):
        """
        处理保存洞察卡片事件
        
        Args:
            event: SaveInsightCard事件，包含card_uuid
        """
        print(f"接受事件{event.event_id}")
        from ti.features.insight.model.insight_event import SaveInsightCard
        
        if isinstance(event, SaveInsightCard):
            card_uuid = event.card_uuid
            
            # 遍历活跃卡片，查找匹配的UUID
            for card_data in self.cards:
                if hasattr(card_data, 'id') and card_data.id == card_uuid:
                    # 找到匹配的卡片，保存它
                    try:
                        # 转换卡片数据为字典格式
                        card_dict = card_data.to_dict() if hasattr(card_data, 'to_dict') else card_data
                        
                        # 保存到仓库
                        self.card_repository.save_today_cards([card_dict])
                        self.logger.log("事件保存", f"成功保存卡片 {card_uuid}")
                        return
                    except Exception as e:
                        self.logger.log("事件保存错误", f"保存卡片 {card_uuid} 时发生错误: {str(e)}")
                        return
            
            # 如果没有找到匹配的卡片
            self.logger.log("事件保存", f"未找到活跃卡片 {card_uuid}")