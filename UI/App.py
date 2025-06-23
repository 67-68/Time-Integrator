import tkinter as tk

from Core.demoParse import getSimpleDataStr_API
from Core.parseInput import parseLineInput_API, dateToActionCentric_API
from Core.validations import dateValidation_API,isValidTimePeriod_API, isValidTimeStr_API,structureValidation_API
from Core.json_Interaction import getData_API, saveData_API
from Core.actionType import ActionType,getEnumValue_API, getEnumValueDict_API
from UI.Frames import SmartInputFrame,BasicFrame
from UI.Small_widgets import BasicButton, BasicEntry, BasicText #这个label什么情况
from UI.Pages import BasicPage
        
"""  ---------- UNIVERSAL FUNCTIONS ---------- """
"""  ------ Date本位 ------ """
# ---------- 用户输入 ----------
#UNIVERSAL; INPUT tk label and tk text;OUTPUT data from user
def getInput_API(prompt,text):
    prompt.config(text = "paste the data in the biggest text") #提示信息
    orgingalData = text.get('1.0','end-1c') #获取内容
    return orgingalData #这里需要注意，原本的userData不好区分，原始数据一律改成original data


#UNIVERSAL; INPUT str userdata; OUTPUT dict userdata
def parseInput_API(orgingalData):
    data = getData_API("Data/dateData.json") #获取文件
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
    enumVal = getEnumValueDict_API(ActionType)
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

"""  ------ TYPE本位 ------ """
#  ---------- 本位转换 ----------
#UNIVERSAL; INPUT data; OUTPUT statistic about action type
def dateToTypeCentric_API(data):
    
    #  ------ 获取类别 ------
    enum = getEnumValue_API(ActionType) 
    
    #  ------ 初始化 ------
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

    #  ------ 遍历，填充数据 ------
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

    #  ------ 计算，填充数据 ------
    for type in types:
        t = types[type]
        if t["count"] > 0:
            t["averageTime"] = t["totalTime"] / t["count"]
            t["ratio"] = t["totalTime"] / totalForAll if totalForAll else 0

    return types


#  ---------- 处理数据 ----------
#  ------ AVERAGE TIME ------
#UNIVERSAL; INPUT stats; OUTPUT str average time,total time and action count
def getAverageTime(stats,enumName):
    typeList = getEnumValue_API(enumName)
    output = ""
    
    for type in typeList:
        t = stats[type]
        total = t["totalTime"]
        output += f'{type} [average: {t["averageTime"]} total {total}, count {t["count"]} \n'
    
    return output
    
def setAverageTime(dataLoc,enumName,text):
    stats = dateToTypeCentric_API(getData_API(dataLoc))
    stats = getAverageTime(stats,enumName)
    text.setText(stats)


#  ------ FREQUENCY ------ 
#UNIVERSAL; INPUT stats,enum class; OUTPUT switchTime of actions
def getSwitchFrequency(stats,enumName):
    typeList = getEnumValue_API(enumName)
    output = ""
    
    for type in typeList:
        t = stats[type]
        total = t["totalTime"]
        totalHour = total / 60
        switchTime = t["count"] - 1
        switchFrequency = "no Switch"
        minutePerSwitch = "N/a"
        
        if totalHour > 0:
            switchFrequency = switchTime / totalHour
        if switchTime > 0:
            minutePerSwitch = total / switchTime
        output += f'{type}, {switchFrequency} per hour, {minutePerSwitch} per switch \n'
    
    return output

 
def setSwitchFrequency(dataLoc,enumName,text):
    stats = dateToTypeCentric_API(getData_API(dataLoc))
    stats = getSwitchFrequency(stats,enumName)
    text.setText(stats)


"""  ------ ACTION 本位 ------ """
#UNIVERSAL; INPUT str loc of ACTION-CEN actionData and DATE-CEN data; STORE/COVER all data(change to ACTION-CEN) to actionData
def registAllAction_API(dataLoc,actionDataLoc):
    data = getData_API(dataLoc)
    actionData = {}
    actionData = dateToActionCentric_API(data,actionData)
    saveData_API(actionData,actionDataLoc)

#UNIVERSAL; INPUT ACTION-CEN actionData, enumName; OUTPUT str
def getActionTypeRatio_API(actionData,enumVals):
    output = ""
    #  ------ 遍历 ------
    for action in actionData: #每个活动的名字
        enumDict = {eType:0 for eType in enumVals}
        #初始化
        for actionType in enumDict:
            enumDict[actionType] = 0
        totalTime = 0
        
        for actionDetail in actionData[action]["actionDetail"]: #每个活动具体的内容
            #  ------ 获取需要的数据 ------
            actionType = actionDetail["action_type"]
            timeSpan = actionDetail["timeSpan"]
            
            #  ------ 赋值 ------
            enumDict[actionType] += timeSpan 
            totalTime += timeSpan
        
        #  ------ 获取需要的值 ------
        output += f'{action}:' #最开始的行动
        for actionType in enumDict:
            t = enumDict[actionType] #timeSpan for each Enum Type
            if totalTime > 0:
                percentage = round (t / totalTime, 1) * 100
            else:
                percentage = 0
            output += f'{percentage}%,{t} {actionType}'
        output += "\n"
    
    return output
        
def setTypeRatioToText_API(actionLoc,enumName,text):
    enumVal = getEnumValue_API(enumName)
    actionData = getData_API(actionLoc)
    actionData = getActionTypeRatio_API(actionData,enumVal)
    text.setText(actionData)

"""  ---------- SPECIFIC FUNCTIONS ---------- """    
#SPECIFIC; INPUT json dataLoc,text; OUTPUT simple time data 
def showSimpleData(dataLoc,text):
    userData = getData_API(dataLoc)
    data = getSimpleDataStr_API(userData)
    text.setText(text = data)
    print("successfully show data") #这一行在换端的时候可以去掉
    

#SPECIFIC; INPUT text, label; STORE data in Data/dateData.json
def promptInput_FUNC(menuPrompt,menuText,menuFrame):
    #  ------ 获取数据 ------
    originalData = getInput_API(menuPrompt,menuText)
    
    #  ------ 处理数据 ------ 
    userData = parseInput_API(originalData)
    
    #  ------ validation ------
    indicatorValidation = validateIndicator_API(originalData)
    dataValidation = validateData_API(userData)
    if indicatorValidation != True:
        menuFrame.bottomInfoFrame.showError(indicatorValidation)
    if dataValidation != True:
        menuFrame.bottomInfoFrame.showError(dataValidation)
    
    #  ------ 存储进actionData ------
    actionData = getData_API("Data/actionData.json")
    actionData = dateToActionCentric_API(userData,actionData)
    saveData_API(actionData,"Data/actionData.json")
    
    #  ------ 存入文件 ------
    saveData_API(userData,"Data/dateData.json") 


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
