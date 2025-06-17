import tkinter as tk

from APIs.parseInput import parseLineInput_API, getActionRegister
from APIs.validations import dateValidation_API,isValidTimePeriod_API, isValidTimeStr_API,structureValidation_API
from APIs.json_Interaction import getData_API, saveData_API
from APIs.actionCategories import actionCategory, getActionDataStr_API, getCateTime_FUNC, getEnumValue_API, getEnumValueDict_API

"""
首先，我现在需要考虑展示数据的内容
我觉得应该先从数据本位出发，考虑需要展示什么
我的数据本位是
date{
    actions{
        action
        timespan
        actiontype
        start
        end
        detail
        
    }
}
对于我的三个新功能，我需要把他们分为数据处理/展示两个层级
"""

"""  ------ GLOBAL VARIABLES ----- """
infoMenuLabel = None
infoDemoLabel = None
lineIndicator = '\n' #把输入的行分开
firstIndicator = " - " #把输入分成三个基本的模块：两个时间和一个行动
secondIndicator = "-" #在行动内细分
firstCount = 2
secondCount = 2

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
        super().__init__(master,text = text,**kwargs)
        text = text
        
"""  ---------- UNIVERSAL FUNCTIONS ---------- """
#  ---------- 报错相关 ----------
def showError(errorText):
    infoDemoLabel.config(text = errorText)
    infoMenuLabel.config(text = errorText)
    #未来可以修改为调用字典对象，目前先手动修改label

# ---------- 用户输入 ----------
#UNIVERSAL; INPUT tk label and tk text;OUTPUT data from user
def getInput_API(prompt,text):
    prompt.config(text = "paste the data in the biggest text") #提示信息
    orgingalData = text.get('1.0','end-1c') #获取内容
    return orgingalData #这里需要注意，原本的userData不好区分，原始数据一律改成original data


#UNIVERSAL; INPUT str userdata; OUTPUT dict userdata
def parseInput_API(orgingalData):
    data = getData_API("data.json") #获取文件
    userData = parseLineInput_API(orgingalData,data,lineIndicator,firstIndicator,secondIndicator) #处理输入
    return userData


#UNIVERSAL; input str originval data; VALIDATE+OUTPUT indicators
def validateIndicator_API(orgingalData):
    #检查每一行的indicator
    lines = orgingalData.split('\n')
    del lines[0]
    for item in lines:
        if structureValidation_API(item, firstIndicator, secondIndicator, firstCount, secondCount) == False: 
            return("there's something wrong in the structure of the data! please check")
    return True
    
    
#UNIVERSAL; INPUT indicator(maybe user setting list in the future) and dict data; Validate/OUTPUT error message 
def validateData_API(userData):
    enumVal = getEnumValueDict_API(actionCategory)
    #检查时间
    for date in userData:
        if dateValidation_API(date) == False:
            return("wrong in date")
        for actionInfo in userData[date]:
            if isValidTimePeriod_API(actionInfo["start"],actionInfo["end"]) == False:
                return("wrong in time period")
            if isValidTimeStr_API(actionInfo["start"]) == False or isValidTimeStr_API(actionInfo["end"]) == False:
                return("wrong in time")
            if actionInfo["action_type"].lower() not in enumVal:
                return("wrong in action type")
    return True


#  ---------- 处理本地数据，输出内容 ----------
#UNIVERSAL; INPUT userData; OUTPUT string as the demonstration of simple data
def getSimpleDataStr_API(userData):
    sum = ""
    data = ""
    totalTime = 0
    totalAction = 0
    for date in userData:
        data += f"In {date}, \n"
        for actions in userData[date]:
            #赋值
            action = actions["action"]
            start = actions["start"]
            end = actions["end"]
            timeSpan = actions["timeSpan"]
            detail = actions["actionDetail"]
            type = actions["action_type"].upper()
            
            #计算总结需要的数据
            totalTime += timeSpan
            totalAction += 1
            
            #输出
            data += f"you do {type}:{action} in {start} - {end}, total {timeSpan} minutes ({detail}) \n"
    sum = f"SUMMARY: {totalAction} actions and {totalTime} minutes in your data \n"
    return sum + data

#  ---------- 本位转换 ----------
#UNIVERSAL; INPUT data; OUTPUT statistic about action type
#date-centric data -> action-type-centric statistics

"""
actionDetail{ #作为key, 存储list类型的dict(每一次行动，即date本位下的action), 如果需要获取count就遍历，也可以查找在不在
    "total":{
        time
        ...
    }
} 
ratio #占总时长的ratio
maxTime 
minTime 
averageTime
用户自定义（先不管）
"""

def getActionTypeStats(data):
    # 获取所有类别
    enum = getEnumValue_API(actionCategory)
    # 初始化
    types = {}
    for cate in enum:
        types[cate] = {
            "actionDetail": {},
            "totalTime": 0,
            "count": 0,
            "maxTime": None,
            "minTime": None,
            "averageTime": 0,
            "ratio": 0
        }
    
    totalForAll = 0

    # 填充数据
    for date in data:
        for action in data[date]:
            timeSpan = action["timeSpan"]
            actionName = action["action"]
            actionType = action["action_type"]
            typeDict = types[actionType]
            
            # 记录 detail
            if actionName not in typeDict["actionDetail"]:
                typeDict["actionDetail"][actionName] = []
            typeDict["actionDetail"][actionName].append(action)

            # 累加
            typeDict["totalTime"] += timeSpan
            typeDict["count"] += 1
            totalForAll += timeSpan

            # max/min
            if typeDict["maxTime"] is None or timeSpan > typeDict["maxTime"]:
                typeDict["maxTime"] = timeSpan
            if typeDict["minTime"] is None or timeSpan < typeDict["minTime"]:
                typeDict["minTime"] = timeSpan

    # 平均数和占比
    for type in types:
        t = types[type]
        if t["count"] > 0:
            t["averageTime"] = t["totalTime"] / t["count"]
            t["ratio"] = t["totalTime"] / totalForAll if totalForAll else 0

    return types
            

#UNIVERSAL; INPUT dict, list; OUTPUT dict filled by list 
def fillDictWithList(dict,list):
    for element in list:
        dict[element] = None
    return dict


"""  ---------- SPECIFIC FUNCTIONS ---------- """
#SPECIFIC; INPUT json dataLoc,text; OUTPUT simple time data 
def showSimpleData(dataLoc,text):
    userData = getData_API(dataLoc)
    data = getSimpleDataStr_API(userData)
    text.setText(text = data)
    print("successfully show data") #这一行在换端的时候可以去掉
    

#SPECIFIC; INPUT text, label; STORE data in data.json
def promptInput_FUNC(menuPrompt,menuText):
    #  ------ 获取数据 ------
    originalData = getInput_API(menuPrompt,menuText)
    
    #  ------ 处理数据 ------ 
    userData = parseInput_API(originalData)
    
    #  ------ validation ------
    indicatorValidation = validateIndicator_API(originalData)
    dataValidation = validateData_API(userData)
    if indicatorValidation != True:
        showError(indicatorValidation)
    if dataValidation != True:
        showError(dataValidation)
    
    #  ------ 存储进actionData ------
    actionData = getData_API("actionData.json")
    actionData = getActionRegister(userData,actionData)
    saveData_API(actionData,"actionData.json")
    
    #  ------ 存入文件 ------
    saveData_API(userData,"data.json") 


def menuGUI():
    #  ---------- 窗口和页面 ----------
    #  ------ 创建root和frame ------
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #主界面创建
    menuFrame = tk.Frame(root,bg = 'white')
    demoFrame = tk.Frame(root,bg = 'white')
    
    #  ------ 初始化窗口和界面 ------
    #设置大小
    root.geometry("800x600")
    
    #主界面提升最顶端
    menuFrame.tkraise()
    
    #主界面切换
    for f in(menuFrame,demoFrame):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    #调整弹性
    basicFrameElasity(menuFrame)
    basicFrameElasity(demoFrame)
    
    #  ---------- 页面内分栏 ----------
    #  ------ MenuFrame ------
    down_MenuFrame = DownPageFrame(menuFrame) #底部灰色栏
    left_MenuFrame = LeftToolFrame(menuFrame) #创建左边工具栏
    main_MenuFrame = CenterMainFrame(menuFrame) #输入栏
    bottom_MenuFrame = BottomInfoFrame(menuFrame)
    
    #  ------ DemonFrame ------
    down_DemoFrame = DownPageFrame(demoFrame)
    left_DemoFrame = LeftToolFrame(demoFrame)
    main_DemoFrame = CenterMainFrame(demoFrame)
    bottom_DemoFrame = BottomInfoFrame(demoFrame)
    
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
        demonMenuButton = LeftToolButton(i,text="enter demonstration menu", height = 5, command = lambda: demoFrame.tkraise())
        demonMenuButton.pack()
        menuSwitchButton = LeftToolButton(i,text="enter main menu", height = 5, command = lambda: menuFrame.tkraise())
        menuSwitchButton.pack()
    
    #  ------ 展示界面 ------ 
    showSimDataButton = LeftToolButton(left_DemoFrame,text = "show simple data",command = lambda: showSimpleData("data.json",demonText))
    showSimDataButton.pack()
    showActionButton = LeftToolButton(left_DemoFrame,text = "show action data",command = lambda: demonText.setText(getActionDataStr_API()))
    showActionButton.pack()
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
      