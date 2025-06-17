from enum import Enum

from APIs.json_Interaction import saveData_API, getData_API

"""
那么我现在应该是有三个“本位”的数据库了
根据不同的大分类排布
一个是原始的data
一个是action作为分类的
最后一个就是现在我做的这个东西

我想把下面的这些分类改成根据处理的数据类型分类，而不是“输出”这样的
"""

#  ---------- 类 ----------
class actionCategory(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"

#  ---------- 函数 ----------
def assignActionCateAPI(actionName,cateName):
    try:
        actions = getData_API("action_integration.json") #get the data needed
        cateName = actionCategory(cateName.lower())
        actions[actionName]["action_type"] = cateName.value #Assign the category    
        saveData_API(actions,"action_integration.json") #覆盖原本的数据
        return True
    except Exception as e:
        return False
    
#TODO:行动presence check
def actionPresenceCheck(actionName):
    print("action Presence need to be completed in the future...")

#  ------ 输出 ------
# 输出Enum的value
def getEnumValue_API(enumClass):
    temp = []
    for item in enumClass:
        temp.append(item.value)
    return temp

def getEnumValueDict_API(enumClass):
    temp = {}
    for item in enumClass:
        temp[item.value] = {"timeSpan":0}
    return temp

#把action及其属性输出为字符串
def getActionDataStr_API():
    list = getEnumValue_API(actionCategory)
    temp = ""
    for i in list:
        temp += i 
        temp += "\n"
    actiondict = getData_API("action_integration.json") #这个时候它应该是一个大字典{行动{行动细节}}
    for action in actiondict:
        temp += f"{action}:{actiondict[action]['action_type']}\n"
    print("successfully make String data")
    return temp

"""
- 首先，我需要一个输出类型的函数
- 然后，我需要一个可以从行动获取类型的函数
- 之后,我需要遍历data
	- 在这个过程中，把时间加入行动
- 最后，制作 GUI 控件，输出它
"""

#  ------ 查找 ------
#UNIVERSAL; INPUT str action; OUTPUT str actionCategory
def getCateFromAction_API(action):
    data = getData_API("action_integration.json")
    try:
        category = data[action]["action_type"]
        return category
    except Exception as e:
        print ("error in get action type")
        return "unknown"

#UNIVERSAL; INPUT: dict data,dict actionCate; OUTPUT timeSpan for each Cate
def getCateTimeFromAct_API(data,cateDict): 
    for date in data:
        for action in data[date]: #这里已经进入了每一段这样的东西 {action =, time =}
            #这个时候，actionCate会是这样 work{time:},waste{time:},...
            timeSpan = action["timeSpan"] #获取时间
            actionCate = getCateFromAction_API(action["action"]) #获取行动类别
            cateDict[actionCate]["timeSpan"] += timeSpan #找到行动类别的时间属性，加上去

#UNIVERSAL; INPUT cateDict; OUTPUT str
def getStrCateTime_FUNC(cateDict):
    temp = ""
    totalTime = 0
    for item in cateDict:
        totalTime += cateDict[item]["timeSpan"]
    for item in cateDict:
        time = cateDict[item]["timeSpan"]
        if totalTime != 0:
            temp += f"{item}:{time}, take {time/totalTime*100} account of total time \n"
        else:
            temp += f"{item}:{time}, take N/a account of total time \n"
    return temp
    
#SPECIFIC/INTEGRATION; output str of data, abou the time distribution in each type of action
def getCateTime_FUNC():
    cateDict = getEnumValueDict_API(actionCategory) #获取类型字典
    data = getData_API("data.json") #获取原始数据
    getCateTimeFromAct_API(data,cateDict) #获取每个行动的时间数据
    temp = getStrCateTime_FUNC(cateDict) #把它整理为字符串
    return temp


    
    
        
        


    

    