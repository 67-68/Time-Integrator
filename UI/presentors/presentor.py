#把action及其属性输出为字符串
from Core.Definitions import ActionType, Indicators, getEnumValue_API
from Core.analysis.actionTypeAnalysis import dateToTypeCentric_API, getAverageTime, getSwitchFrequency
from Core.analysis.dateDataAnalysis import dateToActionCentric_API
from Core.analysis.simpleDataAnalysis import getSimpleDataStr_API
from Core.dataAccess.dataManager import getData_API, saveData_API
from Core.translation.dataInput import parseLineInput_API
from Core.validation.validations import validateData_API, validateIndicator_API


lineIndicator = Indicators.LINE_INDICATOR
firstIndicator = Indicators.FIRST_INDICATOR
secondIndicator = Indicators.SECOND_INDICATOR
firstCount = Indicators.FIRST_COUNT
secondCount = Indicators.SECOND_COUNT


def getActionDataStr_API():
    list = getEnumValue_API(ActionType)
    temp = ""
    for i in list:
        temp += i 
        temp += "\n"
    actiondict = getData_API("action_integration.json") #这个时候它应该是一个大字典{行动{行动细节}}
    for action in actiondict:
        temp += f"{action}:{actiondict[action]['action_type']}\n"
    print("successfully make String data")
    return temp

def setSwitchFrequency(dataLoc,enumName,text):
    stats = dateToTypeCentric_API(getData_API(dataLoc))
    stats = getSwitchFrequency(stats,enumName)
    text.setText(stats)
    

#SPECIFIC; INPUT json dataLoc,text; OUTPUT simple time data 
def showSimpleData(dataLoc,text):
    userData = getData_API(dataLoc)
    data = getSimpleDataStr_API(userData)
    text.setText(text = data)
    print("successfully show data") 
    

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

def setAverageTime(dataLoc,enumName,text):
    stats = dateToTypeCentric_API(getData_API(dataLoc))
    stats = getAverageTime(stats,enumName)
    text.setText(stats)

