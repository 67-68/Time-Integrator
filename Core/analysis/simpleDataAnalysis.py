#UNIVERSAL; INPUT userData; OUTPUT string as the demonstration of simple data
def getSimpleDataStr_API(userData):
    sum = ""
    data = ""
    totalTime = 0
    totalAction = 0
    for date in userData:
        data += f"In {date}, \n"
        for actions in userData[date]:
            #赋值
            action = actions["action"]
            start = actions["start"]
            end = actions["end"]
            timeSpan = actions["timeSpan"]
            detail = actions["actionDetail"]
            type = actions["action_type"].upper()
            
            #计算总结需要的数据
            totalTime += timeSpan
            totalAction += 1
            
            #输出
            data += f"you do {type}:{action} in {start} - {end}, total {timeSpan} minutes ({detail}) \n"
    sum = f"SUMMARY: {totalAction} actions and {totalTime} minutes in your data \n"
    return sum + data