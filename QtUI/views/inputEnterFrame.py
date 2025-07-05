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
        #  ------ 初始化 ------
        super().__init__(parent)
        
        self.IEF = Ui_inputEnterFrame()
        self.IEF.setupUi(self)
        
        #  --- 赋值 ---
        self.PE = self.IEF.propertyEnterFrameBase
        self.FE = self.IEF.fastEnterFrameBase
        
        #  --- 创建wordBank ---
        wordBank = getAutoCompletion_API(actionDataLoc)
        self.FE.setWordBank(wordBank)
        self.PE.setWordBank(wordBank)
        
        #  --- 创建presentor实例 ---
        self.translator = Translator()
        self.stateMachine = StateMachinePresenter(wordBank)
            
        #  ------ 上行事件获取 ------
        self.PE.propertyChanged.connect(lambda d: self._on_PE_text_change(d))
        self.FE.userActionHappen.connect(lambda pack:self._on_FE_action_Happened(pack))
  
    
    """  ------ 区分功能 ------ """
    #这个函数用来处理FE往上面传过来的事件,把rawUserAction转化为UserAction.这意味着每个判断的框内至少都应该有一条语句重新赋值eventType
    def _on_FE_action_Happened(self,FE_To_IEF):
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
        presenterAdvice = self.stateMachine.processEvent_API(userAction)
        
        #  --- 激活dropdown功能 ---
        if presenterAdvice["dropdownAction"]: 
            self._on_dropdown_start(presenterAdvice["data"]["action"]) #TODO:这里需要修改，把它传下去而不是直接修改
            
        #  --- 同步功能 ---
        self.fillPE(presenterAdvice["data"])
    
    """  ------ 速记和属性同步功能 ------ """
    #  ------ 下行命令传输 ------
    def getData(self):
        actionUnit = self.IEF.propertyEnterFrameBase.getData()
        return actionUnit
    
    def fillPE(self,actionUnit):
        with QSignalBlocker(self.PE):
            self.PE.fillData(actionUnit)
    
    def _on_PE_text_change(self,data):
        #fillFE
        with QSignalBlocker(self.FE): 
            fastData = self.translator.properToFast(data)
            self.FE.fillData(fastData) #顺便传输下行指令
        
        #顺便设定一下prefix
        self.PE.set_dropdown_prefix(data["action"])
        
    #SPECIFIC; INPUT error; UPDATE propertyFrame to show the error
    def showError(self,error):
        self.IEF.propertyEnterFrameBase.showError(error)
    

        
    """  ------ dropdown 功能 ------ """
    #这个函数是dropdown功能的入口函数，传输需要筛选的key并让它展示
    def _on_dropdown_start(self,key):
        self.FE.set_dropdown_prefix(key)
        
        
    """  ------ 初始化填充速记和属性功能 ------ """
    #  ------ 下行命令传输 ------
    def fillData(self,actionUnit):
        with QSignalBlocker(self.PE), QSignalBlocker(self.FE.FE.fastEntry):
            #  --- 拆包 ---
            text = self.translator.properToFast(actionUnit)

            self.PE.fillData(actionUnit)
            self.FE.fillData(text)