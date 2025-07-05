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
        
        #  --- 上行事件 ---
        self.FE.fastEntry.returnPressed.connect(self._on_final_confirm)
        self.FE.fastEntry.textChanged.connect(self._on_fastEntry_textChanged)

        #  --- 初始化上行的包 ---
        self.from_FE_To_IEF = {} #我就不初始化了，有问题也好看出来
        
        

    """  ------ API功能 ------ """
    def setWordBank(self,wordBank):
        self.FE.fastEntry.initialization(wordBank)

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
        eventType = RawUserAction.RETURN_PRESSED

        #  ------ 打包 ------
        self.from_FE_To_IEF = {
            "text": self.FE.fastEntry.get(),
            "eventType": eventType,
        }
        
        self.userActionHappen.emit(self.from_FE_To_IEF)
            
            
    """  ------ dropdown功能 ------ """ 
    #  ------ 承接下行指令 ------ 
    def set_dropdown_prefix(self,key):
        self.FE.fastEntry.setPrefix(key)
        
        
    