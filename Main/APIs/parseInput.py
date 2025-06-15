from APIs.json_Interaction import saveDataAPI, getData_API

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
    #there is two format for data input,like 10:22 - 写作业 - 10:45 - 做事 - 11:20. If the time period do not expand to another o'clock, then omit the hour before minutes
    return (afterHour*60 + afterMinutes) - (beforeHour*60 + beforeMinute)


#这个function会把原始的data输入进dictionary
def parseDataIntoList(userData):
    actions = []
    for i in range (1,len(userData)-1,2):
        start = userData[i-1]
        end = userData[i+1]
        action = userData[i]
        actions.append({
            "start":start,
            "action":action,
            "end":end
        })
    return actions


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
    saveDataAPI(a,"action_integration.json")
    
