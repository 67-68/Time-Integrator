from Core.analysis.APITools import getAutoCompleteWithKey_API, getAutoCompletion_API
from Core.dataAccess.dataManager import getData_API
from Core.translation.fastEnterTranslation import transFastEnter_API
from Core.Definitions import InputState, UserActionType 

    
actionDataLoc = "Data/actionData.json"

"""  ---------- 状态机 ----------- """
#UNIVERSAL; INPUT dict action{enum state, userAction, text}; OUTPUT dict result{enum state, keyActionList(to update GUI)}
def stateMachineParser_API(currentState,text,eventType,userAction): #这里的userAction是确保如果有什么自定义的key一起传过来
    actionList = getAutoCompletion_API(actionDataLoc) 
    
    #  ------ 获取就文本而言的建议 ------
    textAdvice = transFastEnter_API(text,actionList)
    
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
            "actionDetail":textAdvice["data"]["actionDetail"],
        }
    }
    
    #  ---------- 判定 ----------
    #  ------ 补全判定 ------
    if eventType == UserActionType.TEXT_INPUT and suggestions["expectedType"] == InputState.AWAIT_ACTION:
        completionList = getAutoCompletion_API(actionDataLoc)
        key = textAdvice["data"]["action"]
        
        suggestions["suggestList"] = getAutoCompleteWithKey_API(key,completionList)
    
    #  ------ 选定判定 ------ 
    if eventType == UserActionType.CONFIRM_SELECT:        
        suggestions["expectedType"] == InputState.AWAIT_ACTION_DETAIL
        suggestions["data"]["action"] = userAction["selectedVal"]
        
        #这里如果可行可能还是需要修改一下速记现实框的显示，如果有依赖于action长度什么的判断会报错
    
    #  ------ 结束判定 ------
    if eventType == UserActionType.FINAL_SUBMIT:
        suggestions["expectedType"] == InputState.COMPLETE
        suggestions["data"]["actionDetail"] = textAdvice
        
        
    return suggestions
        