from Core.Definitions import InputState, UserActionType, RawUserAction
from QtUI.views.rawUI.ui_rawFastEntry import Ui_rawFastEnterFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal,Qt,QSignalBlocker
from PyQt6.QtGui import QShortcut,QKeySequence

class FastEnterFrame(QFrame):
    #  --- 创建一个信号 ---
    userActionHappen = pyqtSignal(dict) #它用来传递上行的事件
    
    def __init__(self, parent = None):
        #  ------ 初始化 ------
        super().__init__(parent)
        
        #  --- 创建ui ---
        self.FE = Ui_rawFastEnterFrame()
        self.FE.setupUi(self)
        
        self.visibility = None
        self.selection = None
        
        #  --- 上行事件 ---
        self.FE.fastEntry.returnPressed.connect(self._on_return_key)
        self.FE.fastEntry.textChanged.connect(self._on_fastEntry_textChanged)
        
        QShortcut(QKeySequence(Qt.Key.Key_Up),self.FE.fastEntry).activated.connect(lambda: self._on_arrow_key("Up"))
        QShortcut(QKeySequence(Qt.Key.Key_Down),self.FE.fastEntry).activated.connect(lambda: self._on_arrow_key("Down"))

        #  --- 初始化上行的包 ---
        self.from_FE_To_IEF = {} #我就不初始化了，有问题也好看出来
        
        

    """  ------ API功能 ------ """
    def updateVisAndSel(self):
        self.visibility = self.FE.fastEntry.getDropdownVisibility()
        self.selection = self.FE.fastEntry.getDropdownSelection()

    def setWordBank(self,wordBank):
        self.FE.fastEntry.initialization(wordBank)

    """  ------ 区分功能 ------ """
    #继续往上送，它是一个大的功能的一部分，当按下enter，不仅仅是它本体会受到影响
    def _on_return_key(self,event): 
        #  ------ 第一道检测：是否是dropdown相关 ------
        self.updateVisAndSel()
        
        if self.visibility and self.selection != None: #如果有，那么加上selectedVal键
            self._on_dropdown_confirm()
            
        #  ------ 第二道检测：（放在上面）是否符合提交的条件 ------
        else:
            self._on_final_confirm()


    """  ------ 快速输入同步/快捷键功能 ------ """
    #  ---------- 下行指令处理 ----------
    #  ------ 传递指令 ------
    def fillData(self,text):
        self.FE.fastEntry.setText(text)
        
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
    
    def _on_final_confirm(self):
        eventType = RawUserAction.RETURN_PRESSED  #首先在这里做完一部分判断，剩下需要currentState的留给上级

        #  ------ 打包 ------
        self.from_FE_To_IEF = {
            "text": self.FE.fastEntry.get(),
            "eventType": eventType,
        }
        
        self.userActionHappen.emit(self.from_FE_To_IEF)
            
            
    """  ------ dropdown功能 ------ """
    #  ------ 本地逻辑处理(并发送下行) ------
    #SPECIFIC; INPUT nothing; DETECT arrow up and down pressed
    def _on_arrow_key(self,event):
        #  --- 判断是否可见 ---
        if self.visibility: #这里不用判定，因为如果visible 就说明了dropdown已经被“激活”了..说到这里，我要给dropdown写个激活的函数...但究竟是它自己解析文本激活自己还是inputEnterFrame呢？我想是前者
            if event == "Down":
                actionState = UserActionType.ARROW_DOWN
            elif event == "Up":
                actionState = UserActionType.ARROW_UP

            self.FE.fastEntry.updateDropdown(actionState)
            
            return "break"
    
    #确认，最终修改文本框
    def _on_dropdown_confirm(self):
        index = self.selection[0]
        selectedVal = self.FE.fastEntry.getDropdownVal(index)
        key = self.FE.fastEntry.getDropdownKey()
        text = self.FE.fastEntry.text()
        
        newText = text.replace(key,selectedVal) 
        
        with QSignalBlocker(self.FE):
            self.FE.fastEntry.setText(newText)
            
            
    #  ------ 承接下行指令 ------ 
    def set_dropdown_prefix(self,key):
        self.FE.fastEntry.set_dropdown_prefix(key)
        
        
    