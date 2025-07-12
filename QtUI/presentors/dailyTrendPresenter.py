
from Core.analysis.analyzer import action_is, action_type_is, matchAll

"""
这里临时存放创建好的matcher
"""
#找到所有犹豫行动项目
hesitation_matcher = matchAll(
    action_is("犹豫"),
    action_type_is("waste")
)

waste_matcher = matchAll(
    action_type_is("waste")
)


"""
主类
"""
class DailyTrendReportPresenter():
    def __init__(self,data):
        self.currentData = data
        
    def createReport(self):
        """_summary_
        调用函数，获取所有需要的文本数据和卡片类型
        """
        report = {}    
        #  ------ 生成文本报告 ------
        #  --- 每日信息 ---
        
        
        
        #  ------ 打包传送回去 ------
        
        
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



    