from PyQt6.QtWidgets import QMainWindow,QVBoxLayout
from QtUI.views.CapturePage import CapturePage
from QtUI.views.rawUI.ui_rawMainWindow import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg


#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 定义元类变量 ----------
    timeSpanChoosed = pyqtSignal(str)
    
    #  ---------- 开始初始化 ----------
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #  ------ 菜单栏图表 ------
        self.fourRealmChart = pg.PlotWidget(self.ui.fourRealmFrame)
        chart = self.fourRealmChart
        
        #  --- 它的排版 ---
        self.ui.fourRealmFrame.layout = QVBoxLayout()
        self.ui.fourRealmFrame.layout.addWidget(self.fourRealmChart)
        
        #  --- 初始化设置 ---
        chart.setBackground("#f8f9fa")
        chart.setFixedHeight(250)
        chart.setFixedWidth(300)
        
        # 隐藏坐标轴，让它看起来更像一个纯粹的图示
        self.fourRealmChart.getPlotItem().hideAxis('left')
        self.fourRealmChart.getPlotItem().hideAxis('bottom')
        
        #  ------ 按钮 ------
        self.ui.menuButton.clicked.connect(self._on_menu_button_clicked)
        self.ui.menuButton_2.clicked.connect(self._on_input_button_clicked)
        
        #  ------ 复选框 ------
        #  --- 注册复选框选项 ---
        timeSpanChoices = ["today","this week"] #这一部分在将来应该放进presentor?
        
        #  --- 复选框登记 ---
        self.ui.timeChooser.addItems(timeSpanChoices)
        
        #  ---------- 信号 ----------
        #  ------ 发送 ------
        self.ui.timeChooser.currentTextChanged.connect(self.timeSpanChoosed)
        
        #  ------ 接收 ------
        self.connectSignal()
        
    def updateMenu(self,timeUseRate,fourRealmRatio,extremeData):
        self.ui.bigNumLabel.setText(str(timeUseRate))
        self.ui.extremeDataText.setText(extremeData)
        self.updateMenuChart(fourRealmRatio)
    
    #SPECIFIC; INPUT data; UPDATE menu chart
    def updateMenuChart(self,data):
        colors = ['#FF6347', '#4CAF50', '#FFC107', '#9E9E9E']
        value = []
        for item in data:
            value.append(data[item])
        x = list(range(len(value))) 
        bars = pg.BarGraphItem(x = x,height = value,width = 0.6,colors = colors)
        self.fourRealmChart.addItem(bars)
    
    def connectSignal(self):
        self.ui.InputPageBase.menuButtonClicked.connect(self._on_menu_button_clicked)
        self.ui.InputPageBase.inputButtonClicked.connect(self._on_input_button_clicked)
    
    def _on_menu_button_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.stackMenuPage)
    
    def _on_input_button_clicked(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.InputPageBase)
    
    

        
        # #  ------ 按钮 ------
        # buttons = {}
        
        # #  --- 主菜单按钮 ---
        # buttons["menu"] = [
        #     {"text":'input', "clicked":lambda: promptInput_FUNC(menuLabel,menuText,menuPage)}
        # ]
        
        # self.pages["menu"].leftToolFrame.coverToolButtons(buttons["menu"])
        
        # #  --- 展示界面按钮 ---
        # buttons["demo"] = [
        #         {"text":'DATE - simple data', "clicked":lambda: showSimpleData('Data/dateData.json',demonText)},
        #         {"text":'TYPE - action frequency', "clicked":lambda: setSwitchFrequency('Data/dateData.json',ActionType,demonText)},
        #         {"text":'TYPE - average time', "clicked":lambda: setAverageTime('Data/dateData.json',ActionType,demonText)},
        #         {"text":'ACTION - regist actions', "clicked":lambda: registAllAction_API('Data/dateData.json','Data/actionData.json')},
        #         {"text":'ACTION - show Ratio', "clicked":lambda: setTypeRatioToText_API('Data/actionData.json',ActionType,demonText)}
        # ]
        # self.pages["demo"].leftToolFrame.coverToolButtons(buttons["demo"])