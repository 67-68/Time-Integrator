from APIs.json_Interaction import saveData_API, getData_API

"""
预计输入类似：
2025-05-10
11:10 - 11:20 - WORK-看书-after virtue 第三章
"""

#UNIVERSAL; INPUT data; OUTPUT dict data registrations
def getNewActionRegister(data,actionData):
    for date in data: #输出每一天
        for action_dict in data[date]: #遍历每一天的每个字典,输出类似a{"A":1,"B":2}
            action_str = action_dict["action"]
            if action_str not in actionData:
                actionData[action_str] = {
                    "timeSpan" : {
                        "total": 0
                        #然后下面是每个enum的time
                    },
                    "actionCount": {
                        "total": 0 
                        #然后下面是每个enum的count    
                    },
                    "eachTimePeriod" : {
                        #放每天的日期{实际时间段}    
                    },
                }
    return actionData


#UNIVERSAl; INPUT line of userdata; OUTPUT time, action, type and detail in file
def parseLineInput_API(userData,data,lineIndicator,firstIndicator,secondIndicator):
    userData = userData.split(lineIndicator) 
    
    date = userData.pop(0)
    #这里就不写date validation了，我把它放到外面搞
    
    newData = []
    
    for item in userData:    
        #分割
        item = item.split(firstIndicator)
        actionData = item[2].split(secondIndicator) 
        
        #获取需要的变量
        start = item[0]
        end = item[1] #这里的validation就不写了
        actionType = actionData[0]
        action = actionData[1]
        actionDetail = actionData[2]
        
        #计算timeSpan
        timeSpan = getTimeSpan_API(start,end)
        
        #重新赋值
        newData.append({
            "start": start,
            "end":end,
            "action":action,
            "action_type":actionType.lower(), 
            "actionDetail":actionDetail,
            "timeSpan": timeSpan 
        })
        
    data[date] = newData
    return data

#UNIVERSAL; INPUT: str time; OUTPUT: int total time
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


"""  ---------- 将来功能 ---------- """
#def getTimeSpan_WithRest_API