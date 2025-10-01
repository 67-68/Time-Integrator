from ti.core.eventBus import EventBus
from ti.features.insight.model.insight_event import CardGenerated
from ti.features.intervention.model.events.special_events import AddToInsightCardEvent
from ti.model.yaml_repository import YamlRepository
from typing import Dict, List


class InsightConnector:
    def __init__(self, bus: EventBus, repo: YamlRepository):
        """
        这个类用来把需要塞入的Intervention View塞进Insight Card
        """
        self.waiting_list: Dict[str, List[AddToInsightCardEvent]] = {}  # key: insight_card_id, value: 等待的干预卡片列表
        self.bus = bus
        self.repo = repo  # InsightCardRepository, 按理来说返回一个insight_card_model

        # 订阅事件
        bus.subscribe_event(AddToInsightCardEvent, self.add_new_waitor)
        bus.subscribe_event(CardGenerated, self.new_insight_card_generated)

    def add_new_waitor(self, event: AddToInsightCardEvent):
        """
        这个函数增加一个新的InterventionCard等待者
        等待属于他们的InsightCard产生

        Args:
            event (AddToInsightCardEvent): 包含干预卡片和洞察卡片ID的事件
        """
        insight_card_id = event.insight_card_id

        # 如果这个洞察卡片ID还没有在等待列表中，创建新的列表
        if insight_card_id not in self.waiting_list:
            self.waiting_list[insight_card_id] = []

        # 添加等待的干预卡片
        self.waiting_list[insight_card_id].append(event)
        print(f"[InsightConnector] 添加等待的干预卡片到洞察卡片 {insight_card_id}")

        # 立即尝试匹配，可能洞察卡片已经存在
        self.matching(insight_card_id)

    def matching(self, insight_card_id: str = None):
        """
        这个函数用来匹配当前的等待者和InsightCard
        它会从Repository获取每一张洞察卡片
        使用一个循环匹配每一个等待者和每一张洞察卡片

        Args:
            insight_card_id (str, optional): 指定要匹配的洞察卡片ID. Defaults to None.
        """
        # 获取所有洞察卡片
        all_insight_cards = self.repo.get_all()

        # 如果指定了洞察卡片ID，只处理该ID
        card_ids_to_process = [insight_card_id] if insight_card_id else list(self.waiting_list.keys())

        for card_id in card_ids_to_process:
            if card_id not in self.waiting_list:
                continue

            # 检查洞察卡片是否存在
            if card_id in all_insight_cards:
                insight_card = all_insight_cards[card_id]
                waiting_events = self.waiting_list[card_id]

                # 为每个等待的干预卡片执行添加操作
                for event in waiting_events:
                    self._add_intervention_to_insight_card(insight_card, event)

                # 清空该洞察卡片的等待列表
                del self.waiting_list[card_id]
                print(f"[InsightConnector] 成功将干预卡片添加到洞察卡片 {card_id}")

    def new_insight_card_generated(self, event: CardGenerated):
        """
        这个函数作为回调函数，当新的洞察卡片生成时调用matching函数

        Args:
            event (CardGenerated): 洞察卡片生成事件
        """
        print(f"[InsightConnector] 收到新的洞察卡片生成事件: {event.card_id}")
        self.matching(event.card_id)

    def _add_intervention_to_insight_card(self, insight_card, intervention_event: AddToInsightCardEvent):
        """
        将干预卡片添加到洞察卡片的具体实现

        Args:
            insight_card: 洞察卡片模型
            intervention_event (AddToInsightCardEvent): 干预卡片事件
        """
        # 这里需要实现具体的添加逻辑
        # 例如：将干预卡片作为子组件添加到洞察卡片中
        # 或者将干预卡片的信息存储到洞察卡片的元数据中

        # 临时实现：打印日志
        print(f"[InsightConnector] 将干预卡片 {intervention_event.view} 添加到洞察卡片 {insight_card.get('card_uuid', 'unknown')}")

        # TODO: 实现具体的添加逻辑
        # 例如：insight_card.add_intervention_component(intervention_event.view)
        