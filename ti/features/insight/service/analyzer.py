"""
首先需要说明,对于所有analyzer
都是输入一个actionUnit, 输出一个dict包裹着的数据
"""                    
from typing import List, Dict, Any
from ti.features.insight.model.insight_card_generation_models import RawCardData
from ti.model.action_unit import ActionUnit
                    
"""
这些函数进行特殊数据的获取，类似极值和平均值
他们接受matcher处理之后的数据
"""
def getTotal_timeSpan(actionUnits: List[ActionUnit]) -> int:
    total = 0
    for au in actionUnits:
        total += au.timeSpan
    return total

def find_longest_timeSpan(actionUnits: List[ActionUnit], config: Dict[str, Any]) -> RawCardData:
    matcher = config["matcher"]
    peak = 0
    data = actionUnits[0]
    for au in actionUnits:
        if matcher(au) and au.timeSpan > peak:
            peak = au.timeSpan
            data = au
    
    return RawCardData(
        id="peak_work_analysis",
        data={"timeSpan": peak, "data": data},
        weight=peak
    )

def find_ratio_distribution(actionUnits: List[ActionUnit], config: Dict[str, Any]) -> RawCardData:
    """
    这个数据分析函数会返回work, rest和waste在一段时间内的分布
    """
    matcher = config["matcher"] #虽然暂时用不着，但还是写上
    
    data = {
        "work":{
            "timeSpan":0,
            },
        "waste":{
            "timeSpan":0
            },
        "rest":{
            "timeSpan":0
            },
        "total":{
            "timeSpan":0
            }
    }
    
    for au in actionUnits:
        if matcher(au):
            at = au.action_type
            tp = au.timeSpan
            data[at ]["timeSpan"] += tp
            data["total"]["timeSpan"] += tp
    
    #计算其他的数据
    for key in data:
        data[key]["ratio"] = round(data[key]["timeSpan"]/data["total"]["timeSpan"] * 100,2)
    
    return RawCardData(
        id="daily_ratio_distribution",
        data=data,
        weight=data["total"]["timeSpan"]
    )
    