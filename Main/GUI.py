import tkinter as tk

from CLI import completeActions, demonstration
from APIs.parseInput import inputTimespan, parseDataIntoList, parseLineInput_API
from APIs.validations import dateValidation_API, formatValidation, isValidTimePeriod_API, isValidTimeStr_API, rangeValidation, structureValidation_API
from APIs.json_Interaction import getData_API, saveData_API
from APIs.actionCategories import actionCategory, assignActionCateAPI, getActionDataStr_API, getCateTime_FUNC, getEnumValueDict_API
"""  ------ GLOBAL VARIABLES ----- """
infoMenuLabel = None
infoDemoLabel = None

"""  ---------- CLASS ----------  """
#  ------ Frame class ------
class LeftToolFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame) #引用父类方法，创建一个Frame
        self.config(bg = "#A9B0B3") #修改颜色
        
        #开始排版
        self.grid(
            row = 0,
            column = 0,
            rowspan = 2,
            sticky='nsew', 
            padx=2.5,
            pady=2.5
        )
        
        self.columnconfigure(0,minsize = 80) #设置最小尺寸

class DownPageFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#C9B49A")
        self.grid(
            row = 2,
            column = 0,
            columnspan = 2,
            sticky='nsew',
            padx = 2.5,
            pady = 0
        )
        self.rowconfigure(2,minsize = 80)

class CenterMainFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#F4F4F4")
        self.grid(
            row = 0,
            column = 1,
            columnspan = 2,
            rowspan = 2,
            sticky='nsew', 
            padx=5, 
            pady=5
        )

class BottomInfoFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#F4F4F4")
        self.grid(
            row = 3,
            column = 0,
            columnspan = 2,
            sticky='nsew', 
            padx=0, 
            pady=0
        )
        self.rowconfigure(3,minsize = 40)
        
#  ------ button class ------ 
#需要传入的参数：父容器，需要执行的命令，面板root
class LeftToolButton(tk.Button):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.config(        
            bg = "#F4F4F4",
            activebackground="#F4F4F4",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            width = 15,
            pady = 6,
            #text 和 command 属性没写，需要外部传入
        )

# class SwitchPageButton(tk.Button):
# 想了一下，没必要写也不太好写专门界面切换的按钮，就先拿基本的功能栏位按钮代替

#  ------ TEXT CLASS ------
class BasicText(tk.Text):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self = tk.Text(master,width = 40, height = 10)
    
    def setText(self,text):
        self.config(state = "normal")
        self.delete('1.0','end')
        self.insert('1.0',text)
        self.config(state = "disabled")

class BasicEntry(tk.Entry):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self = tk.Entry(master,width = 20)
    
    def setEntry(self,text):
        self.delete(0,'end')
        self.insert(0,text)

#  ------ LABEL CLASS ------
class BasicLabel(tk.Label):
    def __init__(self, master,text,**kwargs):
        super().__init__(master,text,**kwargs)
        text = text
        
"""  ---------- UNIVERSAL FUNCTIONS ---------- """

def showError(errorText):
    infoDemoLabel.config(text = errorText)
    infoMenuLabel.config(text = errorText)
    #未来可以修改为调用字典对象，目前先手动修改label
    

"""  ---------- SPECIFIC FUNCTIONS ---------- """
#SPECIFIC; INPUT text, label; STORE data in data.json
#这个specific其实写得也不是很好，还需传入menuPrompt
#注意parseLineInput函数，出问题就找它
def promptInput_FUNC(menuPrompt,menuText):
    #  ------ 初始化需要的变量 ------
    menuPrompt.config(text = "paste the data in the biggest text") #提示信息
    userData = menuText.get('1.0','end-1c') #获取内容
    save = True
    
    #  ------ 处理数据 ------
    data = getData_API("data.json") #获取文件
    data = parseLineInput_API(userData,data) #处理输入
    
    #  ------ validation ------
    #检查格式
    if structureValidation_API(userData) == False: 
        showError("there's something wrong in the structure of the data! please check")
        save = False
    
    #检查时间
    for date in data:
        if dateValidation_API(date) == False:
            showError("wrong in date")
            save = False
        for actionInfo in data[date]:
            if isValidTimePeriod_API(actionInfo["start"],actionInfo["end"]) == False:
                showError("wrong in time period")
                save = False
            if isValidTimeStr_API(actionInfo["start"]) == False or isValidTimeStr_API(actionInfo["end"]) == False:
                showError("wrong in time")
                save = False
            enumVal = getEnumValueDict_API(actionCategory)
            if actionInfo["exploitation_type"] not in enumVal:
                showError("wrong in action type")
                save = False
    #  ------ 最终赋值 ------
    if save == True:
        saveData_API(data,"data.json") #存入文件

#这里删除了promptInput函数

def menuGUI():
    #  ---------- 窗口和页面 ----------
    #  ------ 创建root和frame ------
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #主界面创建
    menuFrame = tk.Frame(root,bg = 'white')
    demonFrame = tk.Frame(root,bg = 'white')
    
    #  ------ 初始化窗口和界面 ------
    #设置大小
    root.geometry("800x600")
    
    #主界面提升最顶端
    menuFrame.tkraise()
    
    #主界面切换
    for f in(menuFrame,demonFrame):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    #调整弹性
    basicFrameElasity(menuFrame)
    basicFrameElasity(demonFrame)
    
    #  ---------- 页面内分栏 ----------
    #  ------ MenuFrame ------
    down_MenuFrame = DownPageFrame(menuFrame) #底部灰色栏
    left_MenuFrame = LeftToolFrame(menuFrame) #创建左边工具栏
    main_MenuFrame = CenterMainFrame(menuFrame) #输入栏
    bottom_MenuFrame = BottomInfoFrame(menuFrame)
    
    #  ------ DemonFrame ------
    down_DemoFrame = DownPageFrame(demonFrame)
    left_DemoFrame = LeftToolFrame(demonFrame)
    main_DemoFrame = CenterMainFrame(demonFrame)
    bottom_DemoFrame = BottomInfoFrame(menuFrame)
    
    #TODO：这里我需要单独去创建一个输入的界面，然后把主界面作为菜单吗？还是直接在主界面提示东西

    #  ---------- 文本框和文本 ----------
    #  ------ 主界面 ------
    menuText = BasicText(main_MenuFrame)
    menuText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    dateEntry = BasicEntry(main_MenuFrame)
    dateEntry.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    
    menuLabel = BasicLabel(main_MenuFrame,text = "welcome, click button to start")
    menuLabel.pack() 
    demoLabel = BasicLabel(main_MenuFrame,text = "this is demonstration page")
    demoLabel.pack() 
    
    global infoMenuLabel #错误信息
    infoMenuLabel = BasicLabel(bottom_MenuFrame,text = "error will show in here")
    infoMenuLabel.pack()
    
    # ------ 展示界面 ------
    demonText = BasicText(main_DemoFrame)
    demonText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    
    demonEntryAction = BasicEntry(main_DemoFrame)
    demonEntryAction.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    demonEntryAction.setEntry("enter action in this box")
    
    demonEntryCate = BasicEntry(main_DemoFrame)
    demonEntryCate.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    demonEntryCate.setEntry("enter Category to change in this box")
    
    global infoDemoLabel #错误信息
    infoDemoLabel = tk.Label(bottom_DemoFrame,text = "error will show in here")
    infoDemoLabel.pack()
    
    #  ---------- 按钮 ----------
    #  ------ 主界面 ------
    #功能性按钮
    inputButton = LeftToolButton(left_MenuFrame, text = "input", command = lambda: promptInput_FUNC(menuLabel,menuText))
    inputButton.pack()
    
    quitButton = LeftToolButton(left_MenuFrame, text = "quit", command = lambda: root.destroy())
    quitButton.pack()

    #切换界面
    for i in (down_DemoFrame,down_MenuFrame):
        demonMenuButton = LeftToolButton(i,text="enter demonstration menu", height = 5, command = lambda: demonFrame.tkraise())
        demonMenuButton.pack()
        menuSwitchButton = LeftToolButton(i,text="enter main menu", height = 5, command = lambda: menuFrame.tkraise())
        menuSwitchButton.pack()
    
    #  ------ 展示界面 ------ 
    showTimeDistButton = LeftToolButton(left_DemoFrame,text = "show time data",command = demonstration)
    showTimeDistButton.pack()
    countActionButton = LeftToolButton(left_DemoFrame,text = "count actions",command = lambda: completeActions(getData_API("data.json")) )
    countActionButton.pack()
    showActionButton = LeftToolButton(left_DemoFrame,text = "show action data",command = lambda: demonText.setText(getActionDataStr_API()))
    showActionButton.pack()
    assignActionButton = LeftToolButton(left_DemoFrame,text = "assignment",command = lambda: assignActionCateAPI(demonEntryAction.get(),demonEntryCate.get()))
    assignActionButton.pack()
    showCateTimeButton = LeftToolButton(left_DemoFrame,text = "show category time",command = lambda: demonText.setText(getCateTime_FUNC()))
    showCateTimeButton.pack()
    
    #  ---------- 事件循环开始 ----------
    root.mainloop()

""" ---------- 各种工厂函数 ---------- """
# 后面可能会改造成类
def basicFrameElasity(frame):
    #调整leftFrame的弹性
    frame.grid_rowconfigure(0, weight=2)
    
    #调整inputFrame的弹性
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=0)
    
    #底部栏位的弹性    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)
    
    #最底部
    frame.grid_rowconfigure(3, weight=0)
      