from PyQt6.QtWidgets import QMainWindow

from Core.Definitions import ActionType
from Core.analysis.APITools import allAddToLayout
from QtUI.views.StackedWidget import StackedWidget
from QtUI.widgets.other.BasicButton import BasicButton
from QtUI.widgets.other.BasicEntry import BasicEntry
from QtUI.widgets.other.BasicLabel import BasicLabel
from QtUI.widgets.other.BasicText import BasicText
from QtUI.widgets.pages.BasicPage import BasicPage

#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        #  ------ 初始化大小 ------
        self.resize(800, 600)
        
        
        #  ------ 初始化翻页 ------
        self.stack = StackedWidget(self)
        self.setCentralWidget(self.stack)
        
        #  ------ 注册需要创建的东西 ------
        #  --- 注册页面 ---
        self.pages = {}
        registPage = ["input","menu","demo"]
        for page in registPage:
            self.pages[page] = BasicPage(self.stack)
            self.stack.addWidget(self.pages[page])   
            self.pages[page].setStyleSheet("background-color: white;")
        
        
        #  --- 注册切换界面的按钮 ---
        pageSwitchButtons = {page_name: [] for page_name in registPage}
        
        for page_name in registPage:
            for target_page in registPage:
                btn = BasicButton(self.pages[page_name])
                btn.setText(f'{target_page} page')
                # 注意 lambda 需要绑定默认参数，否则循环变量会闭包污染
                btn.clicked.connect(lambda checked=False, p=target_page: self.stack.show_page(p))
                self.pages[page_name].layout().addWidget(btn)
                pageSwitchButtons[page_name].append(btn)
                
        self.stack.setCurrentWidget(self.pages["menu"])
        
        #  ------ 创建控件 ------
        #  --- 主界面 ---
        menuPage = self.pages["menu"]
        
        
        menuLabel = BasicLabel(menuPage.centerMainFrame,"test")
        menuText = BasicText(menuPage.centerMainFrame)
        dateEntry = BasicEntry(menuPage.centerMainFrame)
        widgets = [menuLabel,menuText,dateEntry]
        
        allAddToLayout(menuPage,widgets)
        
        
        #  --- 展示界面 ---
        demoPage = self.pages["demo"]
        
        demonText = BasicText(demoPage.centerMainFrame)    

        demonEntryAction = BasicEntry(demoPage.centerMainFrame)
        demonEntryAction.setEntry("enter action in this box")
            
        demonEntryCate = BasicEntry(demoPage.centerMainFrame)
        demonEntryCate.setEntry("enter Category to change in this box")
        
        widgets = [demonEntryAction,demonText,demonEntryCate]
        allAddToLayout(demoPage,widgets)
        
        #  ------ INPUT PAGE ------
        layout = self.pages["input"].layout
        
        #layout.setRowStretch(0, 1)
        #layout.setRowStretch(1, 1)
        #layout.setColumnStretch(0, 1)
        
        #  ------ 按钮 ------
        buttons = {}
        
        #  --- 主菜单按钮 ---
        buttons["menu"] = [
            {"text":'input', "clicked":lambda: promptInput_FUNC(menuLabel,menuText,menuPage)}
        ]
        
        self.pages["menu"].leftToolFrame.coverToolButtons(buttons["menu"])
        
        #  --- 展示界面按钮 ---
        buttons["demo"] = [
                {"text":'DATE - simple data', "clicked":lambda: showSimpleData('Data/dateData.json',demonText)},
                {"text":'TYPE - action frequency', "clicked":lambda: setSwitchFrequency('Data/dateData.json',ActionType,demonText)},
                {"text":'TYPE - average time', "clicked":lambda: setAverageTime('Data/dateData.json',ActionType,demonText)},
                {"text":'ACTION - regist actions', "clicked":lambda: registAllAction_API('Data/dateData.json','Data/actionData.json')},
                {"text":'ACTION - show Ratio', "clicked":lambda: setTypeRatioToText_API('Data/actionData.json',ActionType,demonText)}
        ]
        self.pages["demo"].leftToolFrame.coverToolButtons(buttons["demo"])
        
        