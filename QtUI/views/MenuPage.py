from QtUI.views.rawUI.ui_rawMenuPage import Ui_MenuPage
from PyQt6.QtWidgets import QWidget,QVBoxLayout
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg


class MenuPage(QWidget):
    switchPageSignal = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.MP = Ui_MenuPage()
        self.MP.setupUi(self)
        
        #  ------ 菜单栏图表 ------
        self.fourRealmChart = pg.PlotWidget(self.MP.fourRealmFrame)
        chart = self.fourRealmChart
        
        #  --- 它的排版 ---
        self.MP.fourRealmFrame.layout = QVBoxLayout()
        self.MP.fourRealmFrame.layout.addWidget(self.fourRealmChart)
        
        #  --- 初始化设置 ---
        chart.setBackground("#f8f9fa")
        chart.setFixedHeight(250)
        chart.setFixedWidth(300)
        
        # 隐藏坐标轴，让它看起来更像一个纯粹的图示
        self.fourRealmChart.getPlotItem().hideAxis('left')
        self.fourRealmChart.getPlotItem().hideAxis('bottom')
        
        #  ------ 按钮 ------
        self.MP.menuButton.clicked.connect(lambda: self.switchPageSignal.emit("menu"))
        self.MP.menuButton_2.clicked.connect(lambda: self.switchPageSignal.emit("capture"))
        
        #  ------ 复选框 ------
        #  --- 注册复选框选项 ---
        timeSpanChoices = ["today","this week"] #这一部分在将来应该放进presentor?
        
        #  --- 复选框登记 ---
        self.MP.timeChooser.addItems(timeSpanChoices)
        
        #  ------ 发送 ------
        #self.MP.timeChooser.currentTextChanged.connect(self.timeSpanChoosed) #TODO:修改一下这一坨不知道在干什么的东西
        
        
    def updateMenu(self,timeUseRate,fourRealmRatio,extremeData):
        self.MP.bigNumLabel.setText(str(timeUseRate))
        self.MP.extremeDataText.setText(extremeData)
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