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
    #there is two format for data input,like 10:22 - 写作业 - 45 - 做事 - 11:20. If the time period do not expand to another o'clock, then omit the hour before minutes
    return (afterHour*60 + afterMinutes) - (beforeHour*60 + beforeMinute)
    


# The function is used to discard the space of a string
# Require the input to be a string
# There should not be error, as the data input getting through presense check
#TODO:It can only be suitable for the pure format data
"""
def discardSpace(userData):
    for i in range(1,len(userData)):
        if userData[i-1] == "" and userData[i] == "":
            newData = userData[0,i-1]
    return newData
"""

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


    