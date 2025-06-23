#UNIVERSAl; INPUT line of userdata; OUTPUT time, action, type and detail in file
from Core.analysis.APITools import getTimeSpan_API


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