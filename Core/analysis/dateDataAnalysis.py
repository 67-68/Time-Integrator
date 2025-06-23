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