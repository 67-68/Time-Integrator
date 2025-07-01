from Core.Definitions import InputState, UserActionType
from Core.dataAccess.dataManager import getData_API
from QtUI.views.rawUI.ui_rawFastEntry import Ui_rawFastEnterFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QShortcut,QKeySequence
from QtUI.presentors.StateMachinePresenter import StateMachinePresenter

actionDataLoc = "Data/actionData.json"

class FastEnterFrame(QFrame):
    #  --- 创建一个信号 ---
    fastTextChanged = pyqtSignal(dict)
    
    def __init__(self, wordBank = None,parent = None):
        super().__init__(parent)
        
        #  --- 获取wordBank --- 由于是提升的没有办法传变量，因此本地硬编码
        wordBank = []
        data = getData_API(actionDataLoc)
        for key in data:
            wordBank.append(key)
        
        #  --- 创建ui ---
        self.fastEnterFrame = Ui_rawFastEnterFrame()
        self.fastEnterFrame.setupUi(self)
        
        #  --- 快捷赋值 ---
        self.fe = self.fastEnterFrame.fastEntry
        
        #  --- 初始化 ---
        self.fe.initialization(wordBank)
        
        #  --- 创建presentor ---
        self.presenter = StateMachinePresenter(wordBank)
        
        #  ------ 把entry和具体的函数绑定 ------
        #  --- 绑定enter和按键变化 ---
        self.fe.returnPressed.connect(self._on_return_key_FUNC)
        self.fe.textChanged.connect(self._on_key_release_FUNC)
        
        #  --- 绑定上下键 ---
        QShortcut(QKeySequence(Qt.Key.Key_Up),self.fe).activated.connect(lambda: self._on_arrow_key_FUNC("Up"))
        QShortcut(QKeySequence(Qt.Key.Key_Down),self.fe).activated.connect(lambda: self._on_arrow_key_FUNC("Down"))

        
    def setWordBank(self,wordBank):
        self.wordBank = wordBank
    
    def updateFastEntry(self,text):
        self.fe.setText(text)
        

    def fillData(self,text):
        self.fastEnterFrame.fastEntry.setText(text)
    
    def getData(self):
        text = self.fastEnterFrame.fastEntry.text()
        return text
        
        
    """ ------ 按键监听函数 ------ """    
    #SPECIFIC; INPUT nothing; DETECT arrow up and down pressed
    def _on_arrow_key_FUNC(self,event):
        #  ------ 判断 ------
        if self.currentState == InputState.AWAIT_ACTION:
            if event == "Up" and self.fe.getDropdownSelection(): #如果没有选中不能往上
                self.fe.updateDropdown(UserActionType.ARROW_UP)
            elif event == "Down":
                self.fe.updateDropdown(UserActionType.ARROW_DOWN) 
        else:
            return
        return "break"
    
    #SPECIFIC; INPUT key_release event; DETECT key release and solve it
    def _on_key_release_FUNC(self,event):
        eventType = UserActionType.TEXT_INPUT
        
        #  ------ 打包 ------
        userAction = {
            "text":self.fe.text(),
            "eventType": eventType
        }
        
        #  ------ 调用函数修改状态 ------
        self.presentorContact(userAction)
        return
        
    #SPECIFIC; INPUT nothing; DETECT user press on enter and solve it
    def _on_return_key_FUNC(self,event): 
        #  ------ 判断是否是需要的状态 ------
        visible = self.fe.getDropdownVisibility() #是否可以被用户看见
        selected = self.fastEnterFrame.fastEntry.getDropdownSelection() #是否被选中
        
        #  ------ 判断逻辑 ------
        if visible and selected != None:
            eventType = UserActionType.CONFIRM_SELECT 
            index = selected[0]
            selectedVal = self.fe.getDropdownVal(index)
        elif self.currentState == InputState.AWAIT_ACTION_DETAIL:
            eventType = UserActionType.FINAL_SUBMIT
        else:
            return
        
        #  ------ 打包 ------
        userAction = {
            "currentState": self.parsingCurrentState(),
            "text": self.fe.get(),
            "eventType": eventType,
            "selectedVal": selectedVal #打包用户选中的值
        }
        
        #  ------ 调用函数修改状态 ------ 
        self.presentorContact(userAction)
       
        
    def presentorContact(self,userAction):
        #  --- 获取建议 ---
        presenterAdvice = self.presenter.processEvent_API(userAction)
        
        #  --- 赋值 ---
        text = presenterAdvice["fastEntryText"]
        data = presenterAdvice["data"]
        dropdownAction = presenterAdvice["dropdownAction"]
        
        #  --- 实施建议 ---
        if text:
            self.fe.setText(text)
        if dropdownAction:
            self.fe.showFilter(data["action"])
        
        self.fastTextChanged.emit(data)