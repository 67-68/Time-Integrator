from enum import Enum

from save_and_load import saveData, getData

class actionCategory(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"
    
"""
首先，如果我想要去做一个用户自主修改actionCate的东西，我需要什么呢？
肯定不能借用CLI 或者 GUI的output and input, 那么这一部分就需要作为参数传入
我需要用户给出action的名字，然后我去查找修改
TODO:这里，我可能得返回去完善一下输出action和type的函数(GUI)
"""
def assignActionCate(actionName,cateName):
    #get the data needed
    actions = getData("action_integration.json")
    
    #presence check
    actionPresenceCheck(actionName)
    
    #  ------ process the data ------
    #Search and assignment
    actions[actionName]["exploitation_type"] = actionCategory(cateName.lower())
    
    #覆盖原本的数据
    saveData(actions,"action_integration.json")
    

#TODO:行动presence check
def actionPresenceCheck(actionName):
    print("action Presence need to be completed in the future...")
    

    