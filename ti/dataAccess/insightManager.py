from PyQt6.QtCore import QObject

from ti.dataAccess.insightCacheService import InsightCacheService

class InsightManager:
    """_summary_
    这个类会接收当前创建好的卡片信息
    并帮助管理它们
    当它被要求输出的时候
    会输出每个卡片id下最重要的一张卡片
    同时,它会帮助把当前卡片归档
    """
    def __init__(self,ICS: InsightCacheService):
        self.cards = {}
        self.ICS = ICS
        
    def add_card(self,raw_card_data:dict,pre_card_data:dict) -> None:
        """_summary_
        这个函数负责把卡片加入insight Manager中
        首先 它会把原始卡片数据添加进历史数据
        然后 它会把经过presenter处理过的卡片信息加入待选列表(因此,presenter should pack weight key)
        并输出适合的卡片，当被要求输出的时候
        Args:
            raw_card_data (dict): 原始的卡片信息和数据
            pre_card_data (dict): 经过presenter加工的卡片信息
            
        """
        id = raw_card_data["card_id"]
        if id not in self.cards:
            self.cards[id] = [pre_card_data] #这里搞错了 不是id而是card_id
        # 这里的设计应该是使用card_id来检测是否是修改
        
        # TODO: present_pack会检测，原始数据就不会了？
        self.ICS.add_history_data(raw_card_data)
    
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