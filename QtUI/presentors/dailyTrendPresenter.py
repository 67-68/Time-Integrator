import datetime 
from Data.card_recipe import DAILY_CARD_RECIPE
from QtUI.presentors.formatter import format_card
"""
主类
"""
class DailyTrendReportPresenter():
    def __init__(self,data):
        self.currentData = data
        self.today = datetime.date.today
        
    def createTodayReport(self):
        """_summary_
        调用函数，获取所有需要的文本数据和卡片类型
        """  
        todayData = self.currentData[self.today] #显然这样比用matcher筛选更方便
        cardData = []

        #  ----- 获取卡片信息 ------
        for card in DAILY_CARD_RECIPE:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            
            data = analyzer(todayData,config)
            data = presenter(data)
            data = format_card(data)

            cardData.append(data)
        
        return cardData