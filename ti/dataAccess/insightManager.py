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
        
    def add_card(self,card):
        id = card["id"]
        if id not in self.cards:
            self.cards[id] = []
        
        self.cards[id].append(card)
        
        self.ICS.add_history_data(card)
        