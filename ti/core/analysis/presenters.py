
from Data import themes
from Data import narratives
from ti.utils import flatten_dict

"""
presenter take in analyzer处理完成的数据(list)
给他们附加上外观和文字
card_type
sementic_key
judgement_key

它的另一个职责是翻译数据结构, 把analyzer/detector生成的数据结构翻译为formatter可应用的
以及，给数据附上价值判断
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

def present_sequence_data(data: dict) -> dict:
    """_summary_

    Args:
        data (dict): 一个从detector传递过来的, 适合于它的数据结构

    Returns:
        dict: 一个可以被formatter使用的,良好的数据结构
    """
    returnData = {
        "card_type": themes.CARD_WARNING,
        "judgement_key":["warning"],
        "sementic_key":narratives.POST_EAT_WASTE, #注意，这里present的是post_eat_waste, 而不是一个通用的sequence_data
        "data":flatten_dict(data), #是不是这里出问题了？为什么数据结构会是一个data套data?我估计是无法处理列表导致的.我得想个法子处理一下它
        "weight":data["weight"],
        "id":data["id"]
        }

    return returnData


def regist_presenter():
    """_summary_
    这个函数被用来登记所有的presenter函数
    它会创建一个字典
    aim for 输入事件模式，输出presenter函数
    """
    
    presenters = {}
    
    

    
    
    