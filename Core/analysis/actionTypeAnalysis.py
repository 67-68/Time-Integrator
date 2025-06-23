#UNIVERSAL; INPUT stats,enum class; OUTPUT switchTime of actions
from Core.Definitions import ActionType, getEnumValue_API


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


#UNIVERSAL; INPUT stats; OUTPUT str average time,total time and action count
def getAverageTime(stats,enumName):
    typeList = getEnumValue_API(enumName)
    output = ""
    
    for type in typeList:
        t = stats[type]
        total = t["totalTime"]
        output += f'{type} [average: {t["averageTime"]} total {total}, count {t["count"]} \n'
    
    return output


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