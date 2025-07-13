"""
narrative文本库
presenter会使用一个narrative key在这里寻找对应的文本
它分为两个部分：universal的通用文本和specific, 对于不同行动的文本
"""
PEAK_TIMESPAN = "peak_timeSpan"

UNIVERSAL_NARRATION = {
    "praise":["做的很棒！请保持！！！！！","go work!"]
}

"""
基本结构
{
    {行动}:{
        "presentation": {                   #根据不同主题卡片展示的不同外观
            "success": {                    #胜利主题
                "title": []                 #标题
                #未来可能加入更多外观，例如副标题
            }
        },
        "sementic_key": [ ],                #展示数据的文本
        "judgement_key": {                  #对数据做出评价的文本
            {不同预先被定义好的judgement_key}: []
        }
    }
}

对于每条存储文本的地方都要加入列表，因此避免重复，每条！
"""


SPECIFIC_NARRATION = {
    "peak_timeSpan":{
        "presentation":{
            "card_success":{
                "title": ["深度专注新纪录！✨","你小子居然能专注这么久？"]
            },
            "card_warning":{
                "title": ["数据观察：专注时长异常 🧐","数据异常！一级警报！"]
            }
        },
        "sementic_key": ["今天，你在“{action}”上创造了长达{timeSpan}的专注记录，时段为 {start} 至 {end}。"],
        "judgement_key":{
                "praise":UNIVERSAL_NARRATION["praise"],
                "doubt_accuracy": ["是不是标错了？"],
                "suggest_rest": ["休息会吧我怕你死了"],
                "prompt_work": ["啥玩意你今天连一小时的专注都没有？"],
                "ask_attribution": ["咋回事啊？找找自己的原因"]
        }
    }
}


