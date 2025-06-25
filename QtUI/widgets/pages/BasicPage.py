from PyQt6.QtWidgets import QWidget,QGridLayout

from QtUI.widgets.frames import BottomInfoFrame
from QtUI.widgets.frames.CenterMainFrame import CenterMainFrame
from QtUI.widgets.frames.DownPageFrame import DownPageFrame
from QtUI.widgets.frames.LeftToolFrame import LeftToolFrame




class BasicPage(QWidget):
    def __init__(self, master = None,buttons = None, **kwargs):
        super().__init__(master,buttons,**kwargs)
        
        #  ------ 添加分Frame ------
        self.bottomInfoFrame = BottomInfoFrame(self)
        self.leftToolFrame = LeftToolFrame(self)
        self.centerMainFrame = CenterMainFrame(self)
        self.downPageFrame = DownPageFrame(self)
        
        #  ------ 初始化布局器 ------
        #  --- 创建布局器 ---
        self.pageLayout = QGridLayout(self)
        
        #  --- 添加各种控件 ---
        self.pageLayout.addWidget(self.bottomInfoFrame,3,0,1,2) #分别为row, column, rowspan, columnSpan
        self.pageLayout.addWidget(self.leftToolFrame,0,0,2,1)
        self.pageLayout.addWidget(self.centerMainFrame,0,1,2,2)
        self.pageLayout.addWidget(self.downPageFrame,2,0,2,1)
        
        #  --- 设置弹性 ---
        self.pageLayout.setColumnStretch(0, 1)
        self.pageLayout.setColumnStretch(1, 3)
        self.pageLayout.setRowStretch(0, 2)
        self.pageLayout.setRowStretch(1, 1)
        self.pageLayout.setRowStretch(2, 0)
        self.pageLayout.setRowStretch(3, 0)
        
        #  --- 设置最小值 ---
        self.pageLayout.setRowMinimumHeight(3,40)
        self.pageLayout.setColumnMinimumWidth(0,80)
        self.pageLayout.setRowMinimumHeight(2,80)
        
        #  --- 设置layout ---
        self.setLayout(self.pageLayout)

