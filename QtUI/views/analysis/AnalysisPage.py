from QtUI.rawUI.ui_rawAnalysisPage import Ui_analysisPage
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal
from QtUI.presentors.dailyTrendPresenter import DailyTrendReportPresenter

class AnalysisPage(QFrame):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.AP = Ui_analysisPage()
        self.AP.setupUi()
        
        self.AP.pageSwitchFrameBase.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        self.CA = self.AP.cardsArea
        
    def initialization(self,data = None):
        """_summary_
        这个函数会传递子控件所需要的依赖项
        """
        self.dailyTrend_initialization(data)
    
    def dailyTrend_initialization(self,data):
        """_summary_
        这个函数初始化daily trend功能
        传递依赖项给它并调用presenter完成计算
        最终获取theme展示数据（把它单独放出来是因为未来可能会独立出去）然后展示
        我还没有想好是要点击daily trend按钮之后才初始化，或者一开始就初始化
        暂时先堆在一起
        """
        self.presenter = DailyTrendReportPresenter(data)
        
        #  ------ 获取文本数据 ------
        textReport = self.presenter.createTodayReport() #这里需要把data转换成report

        
        #  ------ 获取UI数据 ------
        
        
        #  ------ 创建类，生成卡片 ------
         
        
        