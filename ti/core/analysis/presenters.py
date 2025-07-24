
from Data import themes
from Data import narratives
from ti.utils import flatten_dict

"""
presenter take in analyzer处理完成的数据(list)
给他们附加上外观和文字
card_type
sementic_key
judgement_key
"""
def present_peak_timeSpan(data):
    timeSpan = data["timeSpan"]
    
    #在将来可能需要改造成为一个平均值什么的，或者用户自己设置，因为如果用户真天天专注这么长时间，那么就可以
    if timeSpan > 90:
        card_type = themes.CARD_WARNING
        judgement_key = ["doubt_accuracy","suggest_rest"]
    elif timeSpan > 60:
        card_type = themes.CARD_SUCCESS
        judgement_key = ["praise"]
    else:
        card_type = themes.CARD_WARNING
        judgement_key = ["prompt_work","ask_attribution"]
    
    return {
        "card_type": card_type,
        "judgement_key": judgement_key,
        "sementic_key": narratives.PEAK_TIMESPAN,
        "data":data
    }
    
def present_ratio_distribution(data):
    """
    接收类似这样的数据
    data  {
        "work":{
            timeSpan:
            (maybe...actionUnits)
        }
        "waste":
        "rest":
    }
    """
    return {
        "card_type": themes.CARD_INFO,
        "judgement_key":["neutral_showinfo"],
        "sementic_key":narratives.SHOW_RATIO,
        "data":flatten_dict(data)
    }
    
    
    