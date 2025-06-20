from enum import Enum

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
        

"""  ---------- 状态机 ----------- """
#UNIVERSAL; INPUT dict action{enum state, userAction, text}; OUTPUT dict result{enum state, keyActionList(to update GUI)}
def stateMachineParser_API(currentState,text,eventType,actionDataLoc):
    autoCompletion = getAutoCompletion(currentState,actionDataLoc)
    expectedState = None
    
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
        
        
        
    #  ------ type转变判定 ------
    #START -> END
    if eventType == UserActionType.TEXT_INPUT:
        if currentState == InputState.AWAIT_START and len(text) == 4:
            expectedState = InputState.AWAIT_END
        elif currentState == InputState.AWAIT_END and len(text):
            pass
        #TODO