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
    
"""  ---------- UNIVERSAL FUNCTION -----------"""
#  ---------- 处理获取列表 ----------
#UNIVERSAL; INPUT currentState; OUTPUT actionList
def getAutoCompletion(currentState,actionDataLoc):
    # ------ 获取行动list ------
    if currentState == InputState.AWAIT_ACTION:
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
    if enumClass == ActionType:
        return ["w","r","s","u"]
        #work, rest, waste, unknown


#这一整个函数好像也是类似状态机的东西，但是是一种连续的状态
#  ---------- 获取UI数据 ----------
#UNIVERSAL; INPUT str text; OUTPUT it advice and data
def parseData_API(text,actionList,typeEnumName):
    #  --------- 初始化返回值 ----------
    advice = {
        "data":{
            "start":"",
            "end":"",
            "action_type":"",
            "action":"",
            "actionDetail":""
        },
        "nextState":"",
        "parseIndex":0
    }
    
    #  ---------- START阶段的处理 ----------
    #  ------ 判断是否可以被处理 ------
    if len(text) < 1 or not text[:4].isdigit():
        advice["nextState"] = InputState.AWAIT_START
        advice["parseIndex"] = 0
        return advice
    
    #  ------ 开始两种情况的赋值 ------
    if len(text) <= 2:
        advice["data"]["start"] = text
    else:
        advice["data"]["start"] = f'{text[0:2]}:{text[2:4]}'
        advice["nextState"] = InputState.AWAIT_START
    
    #  ------ 判断是否进入下一阶段 ------
    if len(text) >= 4:
        advice["nextState"] = InputState.AWAIT_END
        
    #  ---------- END阶段的处理 ----------
        text = text[4:] #截取一下方便处理，现在它就是从end开始的了
        #  ------ 找到End范围 ------
        #找到第一个不是数字的letter
        for letter in text:
            if not letter.isdigit():
                index = text.find(letter)
                break
            
        #  ------ 判定是否正常 ------
        #在这个块内，数据被判定为不正常，无法解析全部，但可以解析一部分有数字的
        if index <= 1 or index == 3:
            if index == 1:
                advice["data"]["end"] = text[0]
            elif index == 3:
                advice["data"]["end"] = f'{text[0:2]}:{text[2]}'
            
            advice["parseIndex"] = 4 + index - 1 #这一行有问题吗
            return advice
        
        #  ------ 赋值 ------
        #在这个块内，数据被期望正常，可以解析
        if index == 2:
            start = advice["data"]["start"][0:2]
            advice["data"]["end"] = f'{start}:{text[0:2]}'
        elif index >= 4: 
            advice["data"]["end"] = f'{text[0:2]}:{text[2:4]}'
        
        advice["nextState"] = InputState.AWAIT_ACTION
        advice["parseIndex"] = 4 + index - 1
        
    #  ---------- 处理Action ----------
        
        
        
        
        
        
    
        
"""  ---------- 状态机 ----------- """
#UNIVERSAL; INPUT dict action{enum state, userAction, text}; OUTPUT dict result{enum state, keyActionList(to update GUI)}
def stateMachineParser_API(currentState,text,eventType,actionDataLoc):
    actionList = getAutoCompletion(currentState,actionDataLoc)
    
    #  ------ 初始化需要返回的列表 ------
    suggestions = {
        "expectedType":"",
        "suggestList":[],
        "UIdata": {
            "start":"",
            "end":"",
            "action":"",
            "actionType":"",
            "actionDetail":""
        }
    }
    
    
    #  ---------- 处理输入 ----------
    #即，之前提到过的仅状态机处理的文字输入部分，不需要依赖于eventType
    suggestions = parseData_API(text,actionList,ActionType)
    
    
    #  ----------- 判定 ----------
    #  ------ 补全判定 ------
    if eventType == UserActionType.TEXT_INPUT and currentState == InputState.AWAIT_ACTION:
        completionList = getAutoCompletion(currentState)
        if text[4:8].isdigit():
            endSpan = 4
        else:
            endSpan = 2
        
        keyIndex = endSpan + 4 + 1
        key = text[keyIndex:]
        keyList = getAutoCompleteWithKey_API(key,completionList)
        
        
        



        
        