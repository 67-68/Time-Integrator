from enum import Enum

from APIs.json_Interaction import saveDataAPI, getDataAPI

class actionCategory(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"

#universal function; INPUT enumClass; OUTPUT a list of value data in this class
def getEnumValue(enumClass):
    temp = []
    for item in enumClass:
        temp.append(item.value)
    return temp
    
    
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
    

    