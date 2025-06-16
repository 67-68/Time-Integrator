from APIs.json_Interaction import saveData_API, getData_API

def inputFormatChange(userData):
    index = 0
    temp = userData
    while index<len(userData):
        try:
            if len(temp[index+1]) == 2 and index % 2 != 0 :
                temp[index+1] = temp[index-1].split(":")[1] + ":" + temp[index+1]
                index += 1
        except Exception as e:
            print("there's something wrong in the input...please check it!")
            return -1
    return temp
            

def timeCompare(beforeHour,beforeMinute,afterHour,afterMinutes):
    return (afterHour*60 + afterMinutes) - (beforeHour*60 + beforeMinute)

def inputTimespan(actions):
        for i in range(len(actions)):
            temp = actions[i]
            pre_h = int(temp["start"][0:2])
            pre_m = int(temp["start"][3:])
            post_h = int(temp["end"][0:2])
            post_m = int(temp["end"][3:])
            timespan = timeCompare(pre_h,pre_m,post_h,post_m)
            actions[i]["timespan"] = timespan

#行动补全函数：提取数据，查找和加入没有在里面的行动        
def completeActions(data):
    a = getData_API("action_integration.json")
    if a == []:
        a = {}
    for date in data: #输出每一天
        for action_dict in data[date]: #遍历每一天的每个字典,输出类似a{"A":1,"B":2}
            action_str = action_dict["action"]
            if action_str not in a:
                a[action_str] = {
                    "totalTime" : 0,
                    "eachTimePeriod" : [],
                    "exploitation_type" : "unknown"
                }
    saveData_API(a,"action_integration.json")

"""
预计输入类似：
2025-05-10
11:10 - 11:20 - WORK-看书-after virtue 第三章
在第一行可能有日期
首先，我需要确认指示输入部分的几个关键符号，只要他们存在这一段输入就是可以被解析的
然后（如果需要做validation)检查在符号拆开之后是否符合数据类型等等
其实这个符号也可以用json让用户自定义然后存储，但是我这里还是先建个变量假装可以自定义了
"""

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
        
        #重新赋值
        newData.append({
            "start": start,
            "end":end,
            "action":action,
            "exploitation_type":actionType.lower(),
            "actionDetail":actionDetail
        })
        
    data[date] = newData
    return data

#UNIVERSAL; INPUT: str time; OUTPUT; total minutes
def getTotalTime_API(time):
    total = 0
    time = time.split(":")
    time[0] = int(time[0])
    time[1] = int(time[1])
    total += time[0]*60 + time[1]
    return total