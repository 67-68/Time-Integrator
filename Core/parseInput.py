from Core.json_Interaction import saveData_API, getData_API

"""
预计输入类似：
2025-05-10
11:10 - 11:20 - WORK-看书-after virtue 第三章
"""

#在这里，我想达到的效果是“输入一份数据，自动加到第二份数据中
#UNIVERSAL; INPUT DATE-CEN data, ACTION-CEN actionData; OUTPUT dict ACTION-CEN data
def dateToActionCentric_API(data,actionData):
    #  ------ 遍历DATE-CEN数据 ------
    for date in data: #输出每一天
        for action in data[date]: #获取每个行动单元
            
            #  ------ 获取需要的值 ------
            a = action["action"] #行动名字
            timeSpan = action["timeSpan"]
            
            #  ------ 判断+初始化 ------
            if a not in actionData:
                action["date"] = date #赋值
                
                actionData[a] = {
                    "totalTime": timeSpan,
                    "totalCount": 1,
                    "maxTimeSpan": timeSpan,
                    "minTimeSpan": timeSpan,
                    "actionDetail": []
                }
                
            #  ------ 添加进去 ------
            else:
                actionData[a]["totalTime"] += timeSpan
                actionData[a]["totalCount"] += 1
                if timeSpan > actionData[a]["maxTimeSpan"]:
                    actionData[a]["maxTimeSpan"] = timeSpan
                if timeSpan < actionData[a]["minTimeSpan"]:
                    actionData[a]["minTimeSpan"] = timeSpan

            actionData[a]["actionDetail"].append(action)                    
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

#UNIVERSAL; INPUT dict, list; OUTPUT dict filled by list 
def fillDictWithList_API(dict,list):
    for element in list:
        dict[element] = None
    return dict

#UNIVERSAL; INPUT fast-record and state Enum; OUTPUT dict normal record



"""  ---------- 将来功能 ---------- """
#def getTimeSpan_WithRest_API