import datetime 
from ti.assets.card_recipe import Card_recipe
from ti.engine.insightEngine import InsightEngine

"""
主类
"""
class ReportPresenter():
    def __init__(self,data):
        self.currentData = data
        # 将日期格式化为 "YYYY-MM-DD" 字符串，例如 "2025-07-13"
        self.today = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.card_recipe = Card_recipe()
        
        self.IE = InsightEngine(self.card_recipe.get_conditional_card())
        
    def create_yesterday_report(self):
        """_summary_
        function: 创建昨天的报告
        流程:
        使用insightEngine类处理信息
        然后把需要检测的actionUnit输入进去
        """  
        if self.today not in self.currentData:
            return "No data"
        
        todayData = self.currentData[self.today] #显然这样比用matcher筛选更方便
        recipe = self.card_recipe.get_daily_card()
        cardData = []

        #  ----- 获取卡片信息 ------
        for card in recipe:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            
            data = analyzer(todayData,config)
            data = presenter(data)

            cardData.append(data)
        
        for au in todayData:
            self.IE(au)
        
        conditional_card = self.IE.get_cur_cards()
        
        for card in conditional_card:
            cardData.append(card)
        
        return cardData