from PyQt6.QtCore import QObject

from ti.services.dataAccess.insightCacheService import InsightCacheService
from ti.features.insight.model.insight_card_generation_models import RawCardData, PresentedCardData



class InsightManager:
    """_summary_
    这个类会接收当前创建好的卡片信息
    并帮助管理它们
    当它被要求输出的时候
    会输出每个卡片id下最重要的一张卡片
    同时,它会帮助把当前卡片归档
    """
    def __init__(self,ICS: InsightCacheService):
        self.cards: Dict[str, PresentedCardData] = {}
        self.ICS = ICS
        
    def add_card(self,raw_card_data: RawCardData, pre_card_data: PresentedCardData) -> None:
        """_summary_
        这个函数负责把卡片加入insight Manager中
        它会把原始卡片数据添加进历史数据
        然后，它会检查新卡片的权重，只保留每个配方ID(recipe_id)下权重最高的卡片。

        Args:
            raw_card_data (dict): 原始的卡片信息和数据, 必须包含 "id" (配方ID)
            pre_card_data (dict): 经过presenter加工的卡片信息, 必须包含 "weight" 键
            
        """
        recipe_id = raw_card_data.id
        new_card_weight = pre_card_data.weight

        # 如果这个配方的卡片还不存在，或者新卡片的权重更高
        if recipe_id not in self.cards or new_card_weight > self.cards[recipe_id].weight:
            self.cards[recipe_id] = pre_card_data
        
        # 无论如何，都记录原始数据历史
        self.ICS.add_history_data(raw_card_data)
    
    def get_current_cards(self):
        """_summary_
        这个函数用来筛选和输出需要的卡片.
        在新的逻辑下, self.cards 中每个id只存储了权重最高的一张卡片.
        因此, 只需要收集所有卡片, 按权重排序, 并返回前10张.
        """
        # 1. 收集所有已经筛选过的最佳卡片
        all_best_cards = list(self.cards.values())
        
        # 2. 对收集到的"最佳卡片"列表进行最终排序
        final_sorted_cards = sorted(all_best_cards, key=lambda card: card.weight, reverse=True)
        
        # 3. 返回前10张卡片，如果不足10张则全部返回
        return final_sorted_cards[:10]

    def reset(self):
        """Clears the current state of the manager."""
        self.cards = {}