import datetime 
from ti.assets.card_recipe import DAILY_CARD_RECIPE
"""
主类
"""
class DailyTrendReportPresenter():
    def __init__(self,data):
        self.currentData = data
        # 将日期格式化为 "YYYY-MM-DD" 字符串，例如 "2025-07-13"
        self.today = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
    def createTodayReport(self):
        """_summary_
        调用函数，获取所有需要的文本数据和卡片类型
        """  
        if self.today not in self.currentData:
            return "No data"
        
        todayData = self.currentData[self.today] #显然这样比用matcher筛选更方便
        cardData = []

        #  ----- 获取卡片信息 ------
        for card in DAILY_CARD_RECIPE:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            
            data = analyzer(todayData,config)
            data = presenter(data)

            cardData.append(data)
        
        return cardData