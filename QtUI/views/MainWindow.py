from PyQt6.QtWidgets import QMainWindow,QVBoxLayout
from QtUI.views.rawMainWindow import Ui_MainWindow
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
        
        #  ------ 复选框 ------
        #  --- 注册复选框选项 ---
        timeSpanChoices = ["today","this week"] #这一部分在将来应该放进presentor?
        
        #  --- 复选框登记 ---
        self.ui.timeChooser.addItems(timeSpanChoices)
        
        #  ---------- 发送信号 ----------
        self.ui.timeChooser.currentTextChanged.connect(self.timeSpanChoosed)
    
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
        
        
        
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # #  ------ 初始化翻页 ------
        # self.stack = StackedWidget(self)
        # self.setCentralWidget(self.stack)
        
        # #  ------ 注册需要创建的东西 ------
        # #  --- 注册页面 ---
        # self.pages = {}
        # registPage = ["input","menu","demo"]
        # for page in registPage:
        #     self.pages[page] = BasicPage(self.stack)
        #     self.stack.addWidget(self.pages[page])   
        #     self.pages[page].setStyleSheet("background-color: white;")
        
        
        # #  --- 注册切换界面的按钮 ---
        # pageSwitchButtons = {page_name: [] for page_name in registPage}
        
        # for page_name in registPage:
        #     for target_page in registPage:
        #         btn = BasicButton(self.pages[page_name])
        #         btn.setText(f'{target_page} page')
        #         # 注意 lambda 需要绑定默认参数，否则循环变量会闭包污染
        #         btn.clicked.connect(lambda checked=False, p=target_page: self.stack.show_page(p))
        #         self.pages[page_name].layout().addWidget(btn)
        #         pageSwitchButtons[page_name].append(btn)
        
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