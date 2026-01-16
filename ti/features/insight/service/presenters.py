
from ti.model import themes
from ti.services.utils import flatten_dict
from ti.features.insight.model.insight_card_generation_models import RawCardData, PresentedCardData

# Narrative key constants (previously from narratives.py)
PEAK_TIMESPAN = "peak_timeSpan"
SHOW_RATIO = "show_ratio"
POST_EAT_WASTE = "post_eat_waste"

"""
presenter take in analyzer处理完成的数据(list)
给他们附加上外观和文字
card_type
sementic_key
judgement_key

它的另一个职责是翻译数据结构, 把analyzer/detector生成的数据结构翻译为formatter可应用的
以及，给数据附上价值判断
"""
def present_peak_timeSpan(data: RawCardData) -> PresentedCardData:
    timeSpan = data.data["timeSpan"]
    
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
    
    return PresentedCardData(
        card_type=card_type,
        judgement_key=judgement_key,
        sementic_key=PEAK_TIMESPAN,
        data=data.data,
        weight=data.weight if data.weight is not None else 0.0,
        id=data.id
    )
    
def present_ratio_distribution(data: RawCardData) -> PresentedCardData:
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
    return PresentedCardData(
        card_type=themes.CARD_INFO,
        judgement_key=["neutral_showinfo"],
        sementic_key=SHOW_RATIO,
        data=flatten_dict(data.data),
        weight=data.weight if data.weight is not None else 0.0,
        id=data.id
    )

def present_sequence_data(data: RawCardData) -> PresentedCardData:
    """_summary_

    Args:
        data (dict): 一个从detector传递过来的, 适合于它的数据结构

    Returns:
        dict: 一个可以被formatter使用的,良好的数据结构
    """
    card_type_id = data.id
    # 有点懵逼，为什么这个Sementic key和Card type可以假定传过来的一定是那个配方？需要使用字典修改，另类判定
    returnData = PresentedCardData(
        card_type=themes.CARD_WARNING,
        judgement_key=["warning"],
        sementic_key=card_type_id, #注意，这里present的是post_eat_waste, 而不是一个通用的sequence_data
        data=flatten_dict(data.data), #是不是这里出问题了？为什么数据结构会是一个data套data?我估计是无法处理列表导致的.我得想个法子处理一下它
        weight=data.weight, # 我需要找个方法在配方定义这些东西
        id=data.id,
    )

    return returnData
    
    

    
    
    