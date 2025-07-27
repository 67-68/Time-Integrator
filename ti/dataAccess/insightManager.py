from PyQt6.QtCore import QObject

from ti.dataAccess.insightCacheService import InsightCache_service

class InsightManager:
    """_summary_
    这个类会接收当前创建好的卡片信息
    并帮助管理它们
    当它被要求输出的时候
    会输出每个卡片id下最重要的一张卡片
    同时,它会帮助把当前卡片归档
    """
    def __init__(self,ICS: InsightCache_service):
        self.cards = {}
        self.ICS = ICS
        
    def add_card(self,card:dict) -> None:
        """_summary_
        这个函数负责把卡片加入insight Manager中
        它会把卡片添加进历史数据
        并输出适合的卡片，当被要求输出的时候
        Args:
            card (dict): 卡片信息
        """
        id = card["id"]
        if id not in self.cards:
            self.cards[id] = [card]
        
        
        self.ICS.add_history_data(card)
    
    def get_current_cards(self):
        """_summary_
        这个函数用来筛选和输出需要的卡片
        首先它会对每个id内的卡片进行筛选
        挑选出最重要的一张卡片，去除其他的
        然后在所有id中选出前十最重要的卡片
        """
        newCards = []
        #这里出过问题
        # 1. 遍历字典中所有的ID
        for id in self.cards:
            # 2. 对每个ID下的卡片列表(self.cards[id])进行排序，并选出最重的一张
            best_card_for_id = sorted(self.cards[id], key=lambda card: card["weight"], reverse=True)[0]
            newCards.append(best_card_for_id)
        
        # 3. 对收集到的“最佳卡片”列表(newCards)进行最终排序
        final_sorted_cards = sorted(newCards, key=lambda card: card["weight"], reverse=True)
        
        # 4. 返回前10张卡片，如果不足10张则全部返回
        return final_sorted_cards[:10]