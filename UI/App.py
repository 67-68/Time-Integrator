import tkinter as tk

from Core.Definitions import ActionType
from Core.dataAccess.dataManager import registAllAction_API
from UI.Views.SmartInputFrame import SmartInputFrame
from UI.Widgets.Frames.BasicFrame import BasicFrame
from UI.Widgets.Pages.BasicPage import BasicPage
from UI.Widgets.Small_widgets.BasicButton import BasicButton
from UI.Widgets.Small_widgets.BasicEntry import BasicEntry
from UI.Widgets.Small_widgets.BasicLabel import BasicLabel
from UI.Widgets.Small_widgets.BasicText import BasicText
from UI.presentors.presentor import promptInput_FUNC, setAverageTime, setSwitchFrequency, showSimpleData




"""  ---------- SPECIFIC FUNCTIONS ---------- """
def menuGUI():
    #  ---------- 按钮 ----------
    #  ------ 主界面 ------
    #功能性按钮
    menuButtons = [
        ('input', lambda: promptInput_FUNC(menuLabel,menuText,menuPage)),
        ('quit', lambda: root.destroy())
        ]
    
    
    #  ------ 展示界面 ------ 
    demoButtons = [
            ('DATE - simple data', lambda: showSimpleData('Data/dateData.json',demonText)),
            ('TYPE - action frequency', lambda: setSwitchFrequency('Data/dateData.json',ActionType,demonText)),
            ('TYPE - average time', lambda: setAverageTime('Data/dateData.json',ActionType,demonText)),
            ('ACTION - regist actions', lambda: registAllAction_API('Data/dateData.json','Data/actionData.json')),
            ('ACTION - show Ratio', lambda: setTypeRatioToText_API('Data/actionData.json',ActionType,demonText))  
            ]
    
    #  ------ 输入界面 ------
    inputButtons = []
    
    #  ---------- 窗口和页面 ----------
    #  ------ 创建root和frame ------
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #主界面创建
    menuPage = BasicPage(root,menuButtons,bg = 'white',)
    demoPage = BasicPage(root,demoButtons,bg = 'white',)
    inputPage = BasicPage(root,inputButtons,bg = 'white')

    #  ------ 初始化窗口和界面 ------
    #设置大小
    root.geometry("800x600")
    
    #主界面提升最顶端
    menuPage.tkraise()
    
    #主界面切换
    for f in(menuPage,demoPage,inputPage):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    #  ------ 输入PAGE的FRAME ------
    upFastFrame = SmartInputFrame(inputPage.centerMainFrame,bg = "#F4F7F9")
    upFastFrame.grid(row = 0, column = 0,sticky='nsew')
    #五个属性栏放进propertyViewFrame的实例了

    bottomToolFrame = BasicFrame(inputPage.centerMainFrame,bg = "#E8EDF2")
    bottomToolFrame.grid(row = 2,column=0,sticky='nsew',)
    
    # 弹性
    inputPage.centerMainFrame.rowconfigure(0, weight=1)
    inputPage.centerMainFrame.rowconfigure(1, weight=1)
    inputPage.centerMainFrame.columnconfigure(0, weight=1)
    
    #  ---------- 文本框和文本 ----------
    #  ------ 主界面 ------
    menuText = BasicText(menuPage.centerMainFrame)
    menuText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    dateEntry = BasicEntry(menuPage.centerMainFrame)
    dateEntry.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    
    menuLabel = BasicLabel(menuPage.centerMainFrame,text = "welcome, click button to start")
    menuLabel.pack() 
    demoLabel = BasicLabel(menuPage.centerMainFrame,text = "this is demonstration page")
    demoLabel.pack() 
    
    
    # ------ 展示界面 ------
    demonText = BasicText(demoPage.centerMainFrame)
    demonText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    
    demonEntryAction = BasicEntry(demoPage.centerMainFrame)
    demonEntryAction.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    demonEntryAction.setEntry("enter action in this box")
        
    demonEntryCate = BasicEntry(demoPage.centerMainFrame)
    demonEntryCate.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    demonEntryCate.setEntry("enter Category to change in this box")
    
    #  ------ 输入界面 ------
    
    #切换界面
    for i in (demoPage.downPageFrame,menuPage.downPageFrame,inputPage.downPageFrame):
        demoSwitchButton = BasicButton(i,text="enter demonstration menu", height = 5, command = lambda: demoPage.tkraise())
        demoSwitchButton.pack(side="left", expand=True, fill="both")
        menuSwitchButton = BasicButton(i,text="enter main menu", height = 5, command = lambda: menuPage.tkraise())
        menuSwitchButton.pack(side="left", expand=True, fill="both") #先不管这个按钮的打包了，两波要放在不同位置有点麻烦
        inputSwitchButton = BasicButton(i,text="enter input page", height = 5, command = lambda: inputPage.tkraise()) 
        inputSwitchButton.pack(side="left", expand=True, fill="both")
    
    #  ---------- 事件循环开始 ----------
    root.mainloop()
