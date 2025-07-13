from Core.analysis.aggregators import getTotal_timeSpan
from Core.analysis.matchers import action_is, action_type_is, date_is, matchAll
import datetime 

"""
这里临时存放创建好的matcher
"""



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
        report = {}    
        #  ------ 生成文本报告 ------
        todayData = self.currentData[self.today] #显然这样比用matcher筛选更方便

        
        return report
    
    
    
    
    
    
    
    
    
    
    
    # def get_hesitation_then_waste_text(self):
    #     """_summary_
    #     这个函数返回所有数据中
    #     "犹豫",hesitation行动跟着waste情况的所有时间的报告
    #     """
    #     data = {}
    #     data["type"] = "card_warning"
    #     actionUnits = sequenceMatcher(hesitation_matcher,waste_matcher)
    #     actionUnits = sequenceDataParser(actionUnits,all)



    