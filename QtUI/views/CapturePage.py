from QtUI.views.rawUI.ui_rawCapturePage import Ui_CapturePage
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class CapturePage(QWidget):
    switchPage_button_clicked = pyqtSignal(str)
    saveData_button_clicked = pyqtSignal(dict)
    date_selected = pyqtSignal(str)
    list_item_selected = pyqtSignal(dict) #我好像不得不把它传上去...虽然并不设计数据的重新载入,因此首先本地修改，然后传数据上去？
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.CP = Ui_CapturePage()
        self.CP.setupUi(self)
        self.DSF = self.CP.dateSelectionFrameBase
        self.EF = self.CP.editorFrameBase
        self.WF = self.CP.welcomeFrame
        self.EMG = self.CP.enterModeGroup
        self.BEF = self.CP.bulkEnterFrameBase
        
        self.BEF_btn = self.CP.bulkEnterFrameButton
        self.EF_btn = self.CP.editorFrameButton
        self.WP_btn = self.CP.welcomePageButton
        
        self.CP.stackedWidget.setCurrentWidget(self.WF)
        self.WP_btn.setChecked(True)
        
        self.currentPage = self.WF
        
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
    
        #  --- 按钮 ---
        self.EMG.buttonClicked.connect(self._on_buttonInGroup_clicked)
        
        self.BEF.saveData_button_clicked.connect(self._on_save_button_clicked)
        
    def _on_buttonInGroup_clicked(self,button):
        self.WP_btn.setChecked(False)
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
        self.saveData_button_clicked.emit(data)
        
    
    #  ------ 重新载入editorFrame界面 ------
    #新建/切换记录
    def _on_changeSelectButton_clicked(self,index):
        #首先确认不是新建
        if index is not 0:
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
        elif index == 0:
            actionUnit = {}
            
        self.list_item_selected.emit(actionUnit)
        
 
    
    def fillData(self,data,au): #理论上来说，对于日历的切换和这个函数，它们的日期数据都应该被传上app类，但现在还没做到这个功能...
        self.DSF.fillData(data) 
        #如果当前没有页面，那么到EF
        if self.currentPage == self.WF:
            self.CP.stackedWidget.setCurrentWidget(self.EF)
            
        elif self.currentPage == self.EF:
            if au:
                self.EF.fillData(au)
            else:
                self.EF.setTutorialLabels()
                
        elif self.currentPage == self.BEF:
            self.BEF.fillData(data) 
                 
    #  ------ 填充数据 ------
    #只有它被填充了数据才显示，否则隐藏到欢迎界面
    def fillEditorFrame(self,actionUnit):
        if actionUnit:
            self.EF.fillData(actionUnit)
        
    def switchData(self,au):
        if au:
            self.DSF.switchItem(au)
            self.EF.fillData(au)
        else:
            self.EF.setTutorialLabels()
        