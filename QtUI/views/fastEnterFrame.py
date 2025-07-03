from Core.Definitions import InputState, UserActionType, RawUserAction
from QtUI.views.rawUI.ui_rawFastEntry import Ui_rawFastEnterFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtGui import QShortcut,QKeySequence

class FastEnterFrame(QFrame):
    #  --- 创建一个信号 ---
    userActionHappen = pyqtSignal(dict) #它用来传递上行的事件
    
    def __init__(self, wordBank = None,parent = None):
        super().__init__(parent)
        
        #  --- 创建ui ---
        self.FE = Ui_rawFastEnterFrame()
        self.FE.setupUi(self)
        
        #  --- 初始化 ---
        self.FE.fastEntry.initialization(wordBank)
        
        #  ------ 上行的事件接收 ------
        self.FE.fastEntry.returnPressed.connect(self._on_return_key_FUNC)
        self.FE.fastEntry.textChanged.connect(self._on_fastEntry_textChanged)
        
        QShortcut(QKeySequence(Qt.Key.Key_Up),self.FE.fastEntry).activated.connect(lambda: self._on_arrow_key_FUNC("Up"))
        QShortcut(QKeySequence(Qt.Key.Key_Down),self.FE.fastEntry).activated.connect(lambda: self._on_arrow_key_FUNC("Down"))

        #  ------ 初始化上行的包 ------
        self.from_FE_To_IEF = {} #我就不初始化了，有问题也好看出来



    """  ------ 智能输入功能 ------ """
    #  ---------- 下行指令处理 ----------
    #  ------ 承接指令 ------
    def setWordBank(self,wordBank):
        self.wordBank = wordBank
    
    #  ------ 传递指令 ------
    def fillData(self,text):
        self.FE.fastEntry.setText(text)
    
    def getData(self):
        text = self.FE.fastEntry.text()
        return text
        
        
        
        
    #  ---------- 上行事件传递 ----------     
    #SPECIFIC; INPUT key_release event; DETECT key release and solve it
    #继续往上送
    def _on_fastEntry_textChanged(self,event):
        #  --- 打包 ---
        self.from_FE_To_IEF = {
            "text":self.FE.fastEntry.text(),
            "rawEventType": RawUserAction.TEXT_CHANGED
        }
        
        # --- 向上传递 ---
        self.userActionHappen.emit(self.from_FE_To_IEF)
    
    
    #继续往上送，它是一个大的功能的一部分，当按下enter，不仅仅是它本体会受到影响
    def _on_return_key_FUNC(self,event): 
        #  ------ 判断是否是需要的状态 ------
        visible = self.FE.fastEntry.getDropdownVisibility() #是否可以被用户看见
        selected = self.FE.fastEntry.getDropdownSelection() #是否被选中
        
        #  ------ 判断逻辑 ------
        eventType = RawUserAction.RETURN_PRESSED  #首先在这里做完一部分判断，剩下需要currentState的留给上级
        
        if visible and selected != None: #如果有，那么加上selectedVal键
            index = selected[0]
            selectedVal = self.FE.fastEntry.getDropdownVal(index)
            self.from_FE_To_IEF["selectedVal"] = selectedVal 
        
        #  ------ 打包 ------
        self.from_FE_To_IEF = {
            "text": self.FE.fastEntry.get(),
            "eventType": eventType,
        }
        
        self.userActionHappen.emit(self.from_FE_To_IEF)
       
        
        
        
    """  ------ 翻页功能 ------ """
    #  --------- 本地处理并发送下行 ---------
    #SPECIFIC; INPUT nothing; DETECT arrow up and down pressed
    def _on_arrow_key_FUNC(self,event):
        #  ------ 判断 ------
        if self.currentState == InputState.AWAIT_ACTION:
            if event == "Up" and self.FE.fastEntry.getDropdownSelection(): #如果没有选中不能往上
                self.FE.fastEntry.updateDropdown(UserActionType.ARROW_UP)
            elif event == "Down":
                self.FE.fastEntry.updateDropdown(UserActionType.ARROW_DOWN) 
        else:
            return
        return "break"