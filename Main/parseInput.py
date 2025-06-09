def inputFormatChange(userData):
    index = 0
    temp = userData
    while index<len(userData):
        try:
            if len(temp[index+1]) == 2 and index % 2 != 0 :
                temp = temp[index-1].split(":")[1] + ":" + temp[index+1]
        except Exception as e:
            print("there's something wrong in the input...please check it!")
            return -1
            

def timeCompare(beforeHour,beforeMinute,afterHour,afterMinutes):
    #there is two format for data input,like 10:22 - 写作业 - 45 - 做事 - 11:20. If the time period do not expand to another o'clock, then omit the hour before minutes
    if beforeHour < afterHour:
        total = (afterHour - beforeHour)*60
    else:
        #if someone do something from 23:00 to 1:00...
        total = (24 - beforeHour + afterHour)*60
    if beforeMinute > afterMinutes:
        return 60 - beforeMinute + afterMinutes + total
    else:
        return afterMinutes - beforeMinute + total


# The function is used to discard the space of a string
# Require the input to be a string
def discardSpace(userData):
    # There should not be error, as the data input getting through presense check
    #TODO:It can only be suitable for the pure format data
    for i in range(len(1,userData)):
        if userData[i-1] == "" and userData[i] == "":
            newData = userData[0,i-1]
    return newData

def parseDataIntoList(userData):
    actions = []
    for i in range (1,len(userData)-2,2):
        start = userData[i-1]
        end = userData[i+1]
        action = userData[i]
        actions.append({
            "start":start,
            "action":action,
            "end":end
        })
    return actions
        


    