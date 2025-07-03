from Core.analysis.APITools import getAutoCompletion_API
from QtUI.views.rawUI.ui_rawInputEnterFrame import Ui_inputEnterFrame
from PyQt6.QtWidgets import QFrame
from QtUI.presentors.translator import Translator
from QtUI.presentors.StateMachinePresenter import StateMachinePresenter
from PyQt6.QtCore import QSignalBlocker,QTimer
from Core.Definitions import InputState, RawUserAction, UserActionType

actionDataLoc = "Data/actionData.json"

class InputEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.IEF = Ui_inputEnterFrame()
        self.IEF.setupUi(self)
        
        #  --- 赋值 ---
        self.PE = self.IEF.propertyEnterFrameBase
        self.FE = self.IEF.fastEnterFrameBase
        
        #  --- 创建wordBank ---
        wordBank = getAutoCompletion_API(actionDataLoc)
        self.FE.setWordBank(wordBank)
        
        #  --- 创建presentor实例 ---
        self.translator = Translator()
        self.stateMachine = StateMachinePresenter(wordBank)
            
        #  --- 承接上行事件 ---
        self.PE.propertyChanged.connect(self._on_text_changed)
        self.FE.userActionHappen.connect(lambda pack:self._on_UserAction_Happened(pack))
  
    
    """  ------ 本地逻辑处理 ------ """
    #这个函数用来处理FE往上面传过来的事件,把rawUserAction转化为UserAction.这意味着每个判断的框内至少都应该有一条语句重新赋值eventType
    def _on_UserAction_Happened(self,FE_To_IEF):
        #  ------ 首先初始化 ------
        rawEventType = FE_To_IEF["rawEventType"]
        userAction = FE_To_IEF
        
        #  ------ 开始判断 ------
        if rawEventType == RawUserAction.TEXT_CHANGED: #首先大分类，看出基本的行动类别
            userAction["eventType"] = UserActionType.TEXT_INPUT
            
        elif rawEventType == RawUserAction.RETURN_PRESSED:
            if self.stateMachine.currentState == InputState.AWAIT_ACTION_DETAIL:
                userAction["eventType"] = UserActionType.FINAL_SUBMIT
                
        else:
            return
    
        #  ------ 状态机给出建议 ------
        #  --- 获取建议 ---
        presenterAdvice = self.stateMachine.processEvent_API(userAction)
        
        #  --- 赋值 ---
        text = presenterAdvice["fastEntryText"]
        data = presenterAdvice["data"]
        dropdownAction = presenterAdvice["dropdownAction"]
        
        #  --- 实施建议 ---
        if dropdownAction: 
            self.FE.fastEntry.showDropdown(data["action"]) #TODO:这里需要修改，把它传下去而不是直接修改
    
    def _on_text_changed(self):
        with QSignalBlocker(self.FE): #既然在单向数据流和原则指导下，核心逻辑在inputEnterFrame, 那么捂不捂嘴具体的控件无所谓
            data = self.PE.getData()
            fastData = self.translator.properToFast(data)
            self.FE.fillData(fastData)
        #在这里，fastEntry的渠道没有必要留着了，它通过正规的渠道传输
    
    
    """  ------ 命令下行 ------ """
    def fillData(self,actionUnit):
        with QSignalBlocker(self.PE), QSignalBlocker(self.FE.FE.fastEntry):
            #  --- 拆包 ---
            text = self.translator.properToFast(actionUnit)

            self.PE.fillData(actionUnit)
            self.FE.fillData(text)
    
    def getData(self):
        actionUnit = self.IEF.propertyEnterFrameBase.getData()
        return actionUnit
        
    #SPECIFIC; INPUT error; UPDATE propertyFrame to show the error
    def showError(self,error):
        self.IEF.propertyEnterFrameBase.showError(error)
        

        
        
        
        
    
    
