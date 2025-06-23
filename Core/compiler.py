# UNIVERSAL; INPUT str text, list actionList; OUTPUT dict advice
from Core.actionType import ActionType
from Core.Definitions import InputState, getEnumAbbriviation


def transFastEnter_API(text, actionList):
    # --------- 初始化返回值 ----------
    advice = {
        "data": {
            "start": "",
            "end": "",
            "action_type": "",
            "action": "",
            "actionDetail": ""},
        "nextState": InputState.AWAIT_START,
        "parseIndex": 0
    }

    if not text:
        return advice

    #  ---------- START阶段 ----------
    if len(text) < 4:
        # 输入不完整，但仍可显示
        if text.isdigit():
            advice["data"]["start"] = text
        return advice # 保持在 AWAIT_START 状态

    if not text[:4].isdigit():
        return advice 

    #  ------ 赋值 ------
    advice["data"]["start"] = f"{text[0:2]}:{text[2:4]}"
    advice["nextState"] = InputState.AWAIT_END
    advice["parseIndex"] = 4

    #  ---------- END阶段 ----------
    if len(text) <= advice["parseIndex"]:
        return advice # 没有更多内容可解析

    #切片方便处理
    end_part_text = text[advice["parseIndex"]:]
    end_digits = ""
    
    #  ------ 获取End阶段的内容 ------
    for i, char in enumerate(end_part_text):
        if char.isdigit():
            end_digits += char
        else:
            break
    
    if not end_digits: # start 后面直接跟了字母
        advice["nextState"] = InputState.AWAIT_ACTION_TYPE # 准备解析类型
        return advice
    
    #  ------ 判断赋值 ------
    if len(end_digits) == 2:
        start_hour = advice["data"]["start"][:2]
        advice["data"]["end"] = f"{start_hour}:{end_digits}"
        advice["nextState"] = InputState.AWAIT_ACTION_TYPE
        advice["parseIndex"] += len(end_digits)
    elif len(end_digits) == 4:
        advice["data"]["end"] = f"{end_digits[:2]}:{end_digits[2:]}"
        advice["nextState"] = InputState.AWAIT_ACTION_TYPE
        advice["parseIndex"] += len(end_digits)
    else:
        # end部分不完整 (e.g., 1位或3位)，显示不完整数据，但状态不前进
        advice["data"]["end"] = end_digits
        return advice

    #  ---------- ACTION_TYPE阶段 ----------
    actionType_text = text[advice["parseIndex"]:] #切片
    typeDict = getEnumAbbriviation(ActionType)
    if len(actionType_text) == 0:
        return advice
    
    for type in typeDict:
        if type == actionType_text[0].lower():
            advice["data"]["action_type"] = typeDict[type]
            advice["nextState"] = InputState.AWAIT_ACTION
            advice["parseIndex"] += 1
            break
        
    if advice["nextState"] != InputState.AWAIT_ACTION:
        return advice
    
    #  ---------- ACTION阶段 ----------
    actionText = text[advice["parseIndex"]:] #切片
    if len(actionText) == 0:
        return advice
    
    #注意不要混淆actionText和这里的action
    #  ------ 判断是否转换状态 ------
    for action in actionList:
        if actionText.find(action) >= 0: #这里用startWith会出问题，比如输入c会直接输入code
            advice["data"]["action"] = action
            advice["nextState"] = InputState.AWAIT_ACTION_DETAIL
            advice["parseIndex"] += len(action)
            break
    
    #  ------ 判断是否使用新的action ------
    if actionText[0] == " ":
        if advice["nextState"] != InputState.AWAIT_ACTION_DETAIL:
            secondSpace = actionText.find(" ",1)
            if secondSpace >= 0:
                action = actionText[1:secondSpace]
                advice["data"]["action"] = action
                advice["nextState"] = InputState.AWAIT_ACTION_DETAIL
                advice["parseIndex"] += len(action)
            else:    
                return advice

    #  ------ 把不完整的action也赋值 ------
    if advice["nextState"] == InputState.AWAIT_ACTION:
        advice["data"]["action"] = actionText
        advice["parseIndex"] += len(actionText) 
    
    #  ---------- ACTION_DETAIL阶段 ----------
    detailText = text[advice["parseIndex"]:]
    advice["data"]["actionDetail"] = detailText
    
    #  ---------- 最终返回 ----------
    return advice

#UNIVERSAL; INPUT a set of property; OUTPUT fast entry str
#采用和上面的大编译器一样的架构，如果解析不到就
def transPropToFast_API(start,end,actionType,action,actionDetail):
    text = ""
    
    
        