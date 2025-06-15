from enum import Enum

from APIs.json_Interaction import saveDataAPI, getDataAPI

class actionCategory(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"

#  ---------- Enum ------------
def getEnumValue(enumClass):
    temp = []
    for item in enumClass:
        temp.append(item.value)
    return temp
    
#  ---------- ActionCategory ----------    
def assignActionCate(actionName,cateName):
    try:
        actions = getDataAPI("action_integration.json") #get the data needed
        cateName = actionCategory(cateName.lower())
        actions[actionName]["exploitation_type"] = cateName.value #Assign the category    
        saveDataAPI(actions,"action_integration.json") #覆盖原本的数据
        return True
    except Exception as e:
        return False
    
#TODO:行动presence check
def actionPresenceCheck(actionName):
    print("action Presence need to be completed in the future...")

#  ------ 输出 ------
#把action及其属性输出为字符串
def getActionDataStr():
    list = getEnumValue(actionCategory)
    temp = ""
    for i in list:
        temp += i 
        temp += "\n"
    actiondict = getDataAPI("action_integration.json") #这个时候它应该是一个大字典{行动{行动细节}}
    for action in actiondict:
        temp += f"{action}:{actiondict[action]['exploitation_type']}\n"
    print("successfully make String data")
    return temp


    

    