from Core.dataAccess.dataManager import getData_API, saveData_API
from QtUI.views.rawUI.ui_rawEditorFrame import Ui_editorFrame
from PyQt6.QtWidgets import QWidget
from QtUI.views.inputEnterFrame import InputEnterFrame
from PyQt6.QtCore import pyqtSignal
from QtUI.presentors.inputValidationPresentor import InputValidation

class EditorFrame(QWidget):    
    
    confirmSignal = pyqtSignal()
    
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.editorFrame = Ui_editorFrame()
        self.editorFrame.setupUi(self)

        #  --- 记录日期 ---
        
        self.date = ""
        self.pages = {}
        
        #  --- 关联回调函数 ---
        self.editorFrame.leftSwitchButton.clicked.connect(self._on_leftArrowButton_clicked)
        self.editorFrame.rightSwitchButton.clicked.connect(self._on_rightArrowButton_Clicked)
        self.editorFrame.confirmButton.clicked.connect(self._on_confirmButton_clicked)
        self.editorFrame.createNewButton.clicked.connect(self._on_new_button_clicked)
        
        #  --- 创建检验对象 ---
        self.validation = InputValidation()
        
        
    def _on_leftArrowButton_clicked(self):
        valid = self.getCurrentValidity
        if not valid:
            return
        
        index = self.editorFrame.stackedWidget.currentIndex()
        if index - 1 < 0: 
            index = self.editorFrame.stackedWidget.count()
        self.editorFrame.stackedWidget.setCurrentIndex(index - 1)
    
    def _on_rightArrowButton_Clicked(self):
        valid = self.getCurrentValidity
        if not valid:
            return
        
        index = self.editorFrame.stackedWidget.currentIndex()
        if index + 1 >= self.editorFrame.stackedWidget.count(): 
            index = -1
        self.editorFrame.stackedWidget.setCurrentIndex(index + 1)
    
    #SPECIFIC; CREATE new page in the end of the stackWidget
    def _on_new_button_clicked(self):
        valid = self.getCurrentValidity
        if not valid:
            return
        
        count = self.editorFrame.stackedWidget.count()
        self.pages[count] = InputEnterFrame(self)
        self.editorFrame.stackedWidget.addWidget(self.pages[count])   

        # 3. switch to the new page
        
        self.editorFrame.stackedWidget.setCurrentIndex(count)
        
        
        
        
    #SPECIFIC; DETECT confirmButton; VALIDATE, COLLECT data and EMIT a signal to presentor
    def _on_confirmButton_clicked(self):
        #  --- collect Data ---
        actionUnits = self.collectData()
        
        #  --- 登记数据到action ---
        #  TODO!!需要创建一个新的presentor来用core的逻辑
        #  TODO:以及，加一个timeSpan计算！！
        
        #  --- save Data ---
        data = getData_API("Data/dateData.json")
        data[self.date] = actionUnits
        saveData_API(data,"Data/dateData.json")
    
        #  --- 删除页面 ---
        for i in range(len(self.pages)):
            self.editorFrame.stackedWidget.removeWidget(self.pages[i])
        
        #  --- 回到日期选择界面 ---
        self.confirmSignal.emit()
        
        
    #SPECIFIC; Collect data from stackedwidget, OUTPUT them as list of actionUnit
    def collectData(self):
        actionUnits = []
        count = self.editorFrame.stackedWidget.count()
        for i in range(count):
            actionUnits.append(self.pages[i].getData())
        
        return actionUnits
    
    def getCurrentValidity(self):
        actionUnit = {}
        index = self.editorFrame.stackedWidget.currentIndex()
        actionUnit = self.pages[index].getData()
        
        valid = self.validation(actionUnit,"actionUnits")
        if valid != True:
            self.pages[index].showError(valid)
            return False
        
        return True
    
    #SPECIFIC; INPUT date and data; UPDATE data into editorFrame
    def fillData(self,date,data):
        #  ------ 获取actionUnits ------
        actionUnits = []
        self.date = date
        
        if date in data:
            actionUnits = data[date]    
        
        #  ------ 页面 ------     在这里，直接填充，如果没有也可以使用
        #  --- 获取页面数量 ---
        pagesNum = len(actionUnits)
        
        #  --- 删除原本的页面 ---
        self.editorFrame.stackedWidget.removeWidget(self.editorFrame.mainFramePage)
        self.editorFrame.stackedWidget.removeWidget(self.editorFrame.page_2)
        
        #  --- 新建页面和popularize ---
        #  --- 先写popularize的逻辑 ---
        if pagesNum != 0:
            for i in range(pagesNum):
                #  --- 先填充完毕 ---
                actionUnit = actionUnits[i]
                self.pages[i] = InputEnterFrame(self)
                self.pages[i].fillData(actionUnit)

                #  --- 然后加到widget里面 ---
                self.editorFrame.stackedWidget.addWidget(self.pages[i])
        
        #  --- 然后写原本就没有记录的逻辑 ---
        #  好像其实我不用写啊
        
            
        
            
            
        