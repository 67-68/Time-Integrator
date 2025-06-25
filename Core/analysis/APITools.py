#UNIVERSAL; INPUT: str time; OUTPUT: int total time
from Core.dataAccess.dataManager import getData_API


def getTotalTime_API(time):
    total = 0
    time = time.split(":")
    time[0] = int(time[0])
    time[1] = int(time[1])
    total += time[0]*60 + time[1]
    return total

#UNIVERSAL; INPUT: str start,str end; OUTPUT int timeSpan
def getTimeSpan_API(start,end):
    timeSpan = getTotalTime_API(end) - getTotalTime_API(start)
    return timeSpan


#  ---------- 处理获取列表 ----------
#UNIVERSAL; INPUT currentState; OUTPUT actionList
def getAutoCompletion_API(actionDataLoc):
    # ------ 获取行动list ------
    actionData = getData_API(actionDataLoc)
    return list(actionData.keys())
 
#UNIVERSAL; INPUT str key and list; OUTPUT list of item with key
def getAutoCompleteWithKey_API(key,list):
    newList = []
    for item in list:
        if item.find(key) >= 0:
            newList.append(item)
    if newList == []:
        newList.append("nothing match")

    return newList

#UNIVERSAL; PyQt; INPUT widget and lowerstage widget; ADD widget to layout
def addToLayout(layoutWidget,widget):
    try:
        layoutWidget.layout().addWidget(widget)
    except Exception as e:
        print(e)
        print(f"something wrong when add {widget} into {layoutWidget}")
        
def allAddToLayout(layoutWidget,widgets):
    for widget in widgets:
        try:
            layoutWidget.layout().addWidget(widget)
        except Exception as e:
            print(e)
            print(f"something wrong when add {widget} into {layoutWidget}")