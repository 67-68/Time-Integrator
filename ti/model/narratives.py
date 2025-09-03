
"""
narrative文本库
presenter会使用一个narrative key在这里寻找对应的文本
它分为两个部分：universal的通用文本和specific, 对于不同行动的文本
"""
PEAK_TIMESPAN = "peak_timeSpan"
SHOW_RATIO = "show_ratio"
POST_EAT_WASTE = "post_eat_waste"


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


    :{
        "presentation":{
            "card_info": {
                "title":
            }
        },
        "sementic_key":[] ,
        "judgement_key":
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
        "sementic_key": {
                "text": ["昨天，在所有行动中，你在“{action}”上专注了最多时间，达到了{timeSpan}分钟，时段为 {start} 至 {end}。"],
                "history_text": []
            },
        "judgement_key":{
                "praise":UNIVERSAL_NARRATION["praise"],
                "doubt_accuracy": ["是不是标错了？"],
                "suggest_rest": ["休息会吧我怕你死了"],
                "prompt_work": ["啥玩意你昨天连一小时的专注都没有？太少了"],
                "ask_attribution": ["咋回事啊？找找自己的原因，是否烈性娱乐过多？"]
        }
    },
    "show_ratio":{
        "presentation":{
            "card_info": {
                "title":["时间分布展示"]
            }
        },
        "sementic_key":{
            "text": ["工作:{work.timeSpan}min, {work.ratio}% \n休息:{rest.timeSpan}min, {rest.ratio}% \n浪费:{waste.timeSpan}min, {waste.ratio}%"]
            },
        "judgement_key":{
            "neutral_showinfo":["test"]
            
        }
    },
    "post_eat_waste":{
        "presentation":{
            "card_warning": {
                "title":["饭后摸鱼陷阱"]
            }
        },
        "sementic_key":{
            "text": ["昨天，你在“{data.meal.action}”({data.meal.start} - {data.meal.end})之后，立刻就开始“{data.waste.action}(到{data.waste.end})”，持续了{data.waste.timeSpan}分钟。"],
            "history_text": ["数据显示这已经不是第一次发生这种情况了。"]
        },
        "judgement_key":{
            "warning":["你浪费了很多时间哦～这些时间本可以用来睡觉，如今隔断了你的时间，让你更不容易睡着，污染了你的正反馈，即使是工作也不能专心。\n下次注意吧，喵。"]
        }
    }
}
