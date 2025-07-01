from Core.Definitions import InputState, UserActionType
from Core.logic.stateMachineParser import stateMachineParser_API
from Core.translation.fastEnterTranslation import transFastToProp_API


class StateMachinePresenter():
    def __init__(self,wordBank):
        self.wordBank = wordBank
        self.currentState = InputState.AWAIT_START
    
    #SPECIFIC; INPUT nothing; OUTPUT currentState
    def parsingCurrentState(self):
        return self.currentState   
    
    
    #UNIVERSAL; INPUT dict userAction(state,text,eventType); UPDATE state and property above
    def processEvent_API(self,userAction):
        #  ------ 获取需要的变量 ------
        currentState = self.parsingCurrentState()
        text = userAction["text"]
        eventType = userAction["eventType"]
        
        #  ------ 传回建议 ------
        presenterAdvice = {}
        fastEntryText = ""
        dropdownAction = ""
        data = {}
        
        #  ---------- 询问状态机，给出建议 ----------
        suggestion = stateMachineParser_API(currentState,text,eventType,userAction)
        
        #  ------ 修改速记提示框的显示 ------
        if eventType == UserActionType.CONFIRM_SELECT: #执行confirm_select的时候才需要传wordBank
            #  --- 判断是否action为空 ---
            action_to_replace = transFastToProp_API(text,self.wordBank).get("data", {}).get("action", "")
        
            # 2. 获取状态机确认“之后”的action是什么
            new_action = suggestion["data"]["action"]

            # 3. 执行替换
            if action_to_replace and new_action: # 只有当之前确实解析出了一个action时才替换
                fastEntryText = text.replace(action_to_replace, new_action, 1)
                 
            else: # 如果之前没解析出来，就直接追加
                fastEntryText = text + new_action
            
        #  ------ 实施建议 ------
        #  --- 插入新东西 ---
        if suggestion["expectedType"] == InputState.AWAIT_ACTION:
            actionStr = suggestion["data"]["action"]
            dropdownAction = "FILTER"

        #  ------ 统一赋值 ------
        presenterAdvice["fastEntryText"] = fastEntryText
        presenterAdvice["data"] = suggestion["data"]
        presenterAdvice["dropdownAction"] = dropdownAction
        
        return presenterAdvice