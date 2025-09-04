
from PyQt6.QtCore import pyqtSignal

from ti.model.action_unit import ActionUnit
from ti.view.rawUI.ui_rawCapturePage import Ui_CapturePage
from ti.view.widgets.pages.BasicWidget import BasicWidget



class CapturePage(BasicWidget):
    switchPage_button_clicked = pyqtSignal(str)
    saveData_button_clicked = pyqtSignal(ActionUnit)
    date_selected = pyqtSignal(str)
    list_item_selected = pyqtSignal(ActionUnit) #我好像不得不把它传上去...虽然并不设计数据的重新载入,因此首先本地修改，然后传数据上去？
    new_button_selected = pyqtSignal()
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.CP = Ui_CapturePage()
        self.CP.setupUi(self)
        self.DSF = self.CP.dateSelectionFrameBase
        self.EF = self.CP.editorFrameBase
        self.EMG = self.CP.enterModeGroup
        self.BEF = self.CP.bulkEnterFrameBase
        
        self.BEF_btn = self.CP.bulkEnterFrameButton
        self.EF_btn = self.CP.editorFrameButton
        
        self.CP.stackedWidget.setCurrentWidget(self.EF)
        self.currentPage = self.EF
                
        self.currentAU = None
        
        #  ----- 上行事件接收 ------
        #  --- 切换页面 ---
        self.CP.pageSwitchFrameBase.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        #  --- dateSelection ---
        self.DSF.dateSelected.connect(lambda d: self.date_selected.emit(d))
        self.DSF.list_item_selected.connect(lambda i: self.list_item_selected.emit(i))
        
        self.CP.splitter.setSizes([300, 1000])        # 绝对像素
        
        #  --- EditorFrame ---
        self.EF.actionUnitSelected.connect(lambda i: self._on_changeSelectButton_clicked(i))
        self.EF.saveData_button_clicked.connect(lambda s: self._on_save_button_clicked(s))
        self.EF.new_button_selected.connect(self.new_button_selected.emit)
    
        #  --- 按钮 ---
        self.EMG.buttonClicked.connect(self._on_buttonInGroup_clicked)
        
        self.BEF.saveData_button_clicked.connect(self._on_save_button_clicked)
        
    def _on_buttonInGroup_clicked(self,button):
        self.EF_btn.setChecked(False)
        self.BEF_btn.setChecked(False)
        
        if button == self.EF_btn:
            self.EF_btn.setChecked(True)
            self.CP.stackedWidget.setCurrentWidget(self.EF)
            self.currentPage = self.EF
        else:
            self.BEF_btn.setChecked(True)
            self.CP.stackedWidget.setCurrentWidget(self.BEF)
            self.currentPage = self.BEF
            
        
    #  ------ 保存 ------
    def _on_save_button_clicked(self,data):
        self.currentAU: ActionUnit
        self.currentAU.start = data["start"]
        self.currentAU.end = data["end"]
        self.currentAU.action = data["action"]
        if data.get("action_detail"):
            self.currentAU.action_detail = data["action_detail"]
        self.currentAU.action_type = data["action_type"]
        
        #下面的因为信号问题无法长久保存
        self.saveData_button_clicked.emit(self.currentAU)
        
    
    #  ------ 重新载入editorFrame界面 ------
    #新建/切换记录
    def _on_changeSelectButton_clicked(self,index):
        #首先确认不是新建

        #由于传过来的是一个数字，首先我需要找到当前找到是第几项
        pos = self.DSF.find_current_actionUnit_pos()
        len = self.DSF.get_actionUnit_listLength()
        #然后设置下一项，顺便滚动
        if index is 1:
            if pos + 1 >= len:
                idx = 0
            elif pos == -1:
                idx = 0
            else:
                idx = pos + 1
        elif index is -1:
            if pos == 0:
                idx = len - 1
            elif pos == -1:
                idx = 0
            else:
                idx = pos - 1
        actionUnit = self.DSF.get_actionUnit_fromList(idx)

        self.list_item_selected.emit(actionUnit)
        #创建新页面的意图和切换不同au占据了同样的信号，这是不好的
        
 
    
    def fillData(self,data,au): #理论上来说，对于日历的切换和这个函数，它们的日期数据都应该被传上app类，但现在还没做到这个功能...
        self.DSF.fillData(data) 
        
        if self.currentPage == self.EF:
            if au:
                self.EF.fillData(au)
        elif self.currentPage == self.BEF:
            self.BEF.fillData(data) 
                 
    #  ------ 填充数据 ------
    #只有它被填充了数据才显示，否则隐藏到欢迎界面
    def fillEditorFrame(self,actionUnit):
        if actionUnit:
            self.EF.fillData(actionUnit)
        
    def switchData(self,au):
        self.EF.fillData(au)
        self.currentAU = au # 这个是原本传入的au，下面的PE中是当前的au
        if au["action"] != "":
            self.DSF.switchItem(au)
            
        
        
        
        