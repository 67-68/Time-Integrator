from enum import Enum
from APIs.actionType import ActionType

from APIs.json_Interaction import getData_API 
"""  ---------- ENUM CLASS ---------- """
class InputState(Enum):
    AWAIT_START = "awaitStart"
    AWAIT_END = "awaitEnd"
    AWAIT_ACTION_TYPE = "awaitActionType"
    AWAIT_ACTION = "awaitAction"
    AWAIT_ACTION_DETAIL = "awaitActionDetail"
    COMPLETE = "complete"

class UserActionType(Enum):
    TEXT_INPUT = "textINPUT"
    ARROW_UP = "arrowUp"
    ARROW_DOWN = "arrowDown"
    CONFIRM_SELECT = "confirmSelect"
    FINAL_SUBMIT = "finalSubmit"
    
actionDataLoc = "actionData.json"

"""  ---------- UNIVERSAL FUNCTION -----------"""
#  ---------- 处理获取列表 ----------
#UNIVERSAL; INPUT currentState; OUTPUT actionList
def getAutoCompletion(actionDataLoc):
    # ------ 获取行动list ------
    actionData = getData_API(actionDataLoc)
    return list(actionData.keys())
 
#UNIVERSAL; INPUT str key and list; OUTPUT list of item with key
def getAutoCompleteWithKey_API(key,list):
    newList = []
    for item in list:
        if item.find(key) >= 0:
            newList.append(item)
    if newList == []:
        newList.append("nothing match")

    return newList


#UNIVERSAL; INPUT enum ActionType; OUTPUT list of enum abbreviations
def getEnumAbbriviation(enumClass):
    temp = {
            "w":"work",
            "s":"waste",
            "u":"unknown",
            "r":"rest"
    }
    if enumClass == ActionType:
        return temp

#这一整个函数好像也是类似状态机的东西，但是是一种连续的状态
#  ---------- 获取UI数据 ----------
# UNIVERSAL; INPUT str text, list actionList; OUTPUT dict advice
def parseData_API(text, actionList, typeEnumName):
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
    
    #  ------ 把不完整的action也赋值 ------
    advice["data"]["action"] = actionText
    advice["parseIndex"] += len(actionText) 
    
    #注意不要混淆actionText和这里的action
    #  ------ 判断是否转换状态 ------
    for action in actionList:
        if actionText.find(action) >= 0:
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
    
    #  ---------- ACTION_DETAIL阶段 ----------
    detailText = text[advice["parseIndex"]:]
    advice["data"]["actionDetail"] = detailText
    
    #  ---------- 最终返回 ----------
    return advice
        
        

        
"""  ---------- 状态机 ----------- """
#UNIVERSAL; INPUT dict action{enum state, userAction, text}; OUTPUT dict result{enum state, keyActionList(to update GUI)}
def stateMachineParser_API(currentState,text,eventType,userAction): #这里的userAction是确保如果有什么自定义的key一起传过来
    actionList = getAutoCompletion(actionDataLoc) #TODO:这个函数的逻辑到底是怎么写的？为什么要穿actionList
    
    #  ------ 获取就文本而言的建议 ------
    textAdvice = parseData_API(text,actionList,ActionType)
    
    #不要把expectedType和currentState搞混了,但这俩玩意的关系是啥？
    #  ------ 初始化需要返回的列表 ------
    suggestions = {
        "expectedType":textAdvice["nextState"],
        "suggestList":[],
        "data": {
            "start":textAdvice["data"]["start"],
            "end":textAdvice["data"]["end"],
            "action":textAdvice["data"]["action"],
            "action_type":textAdvice["data"]["action_type"],
            "actionDetail":textAdvice["data"]["actionDetail"]
        }
    }
    
    #  ---------- 判定 ----------
    #  ------ 补全判定 ------
    if eventType == UserActionType.TEXT_INPUT and suggestions["expectedType"] == InputState.AWAIT_ACTION:
        completionList = getAutoCompletion(actionDataLoc)
        key = textAdvice["data"]["action"]
        
        suggestions["suggestList"] = getAutoCompleteWithKey_API(key,completionList)
    
    #  ------ 选定判定 ------ 
    if eventType == UserActionType.CONFIRM_SELECT:
        suggestions["previousAction"] = textAdvice["data"]["action"] #结构的修补
        
        suggestions["expectedType"] == InputState.AWAIT_ACTION_DETAIL
        suggestions["data"]["action"] = userAction["selectedVal"]
        
        #这里如果可行可能还是需要修改一下速记现实框的显示，如果有依赖于action长度什么的判断会报错
    
    #  ------ 结束判定 ------
    if eventType == UserActionType.FINAL_SUBMIT:
        suggestions["expectedType"] == InputState.COMPLETE
        suggestions["data"]["actionDetail"] = textAdvice
        
        
    return suggestions
        