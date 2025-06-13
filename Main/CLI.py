from validations import formatValidation, rangeValidation
from parseInput import completeActions, inputTimespan, parseDataIntoList
from save_and_load import getData, saveData

def promptInput():
    #input the data
    userData = input("input your data")
    date = input("what date is it today? please enter in the form of 2025/6/10")
    
    #TODO:presence check
    
    #TODO:use strip to delete spaces
    
    #TODO:change it into discard redundant space in data
    
    #change the format of the data, in order to save into json
    userData = userData.split(" - ")
    
    #put data into the list
    actions = parseDataIntoList(userData)
    
    #Format check and change the format
    for i in range (len(actions)):
        actions[i]["end"] = formatValidation(actions[i]["start"],actions[i]["end"])
    
    #validate whether they are reasonable
    if rangeValidation(actions) == True:
        print("pass range validation correctly")
    
    #输入timespan
    inputTimespan(actions)
    
    #把actions包裹进一个新的dictionary
    data = {date : actions}
    
    #输入data
    data = getData("data.json")
    data[date] = actions
    saveData(data,"data.json")
 
def mainMenu():
    while True:
        choice = input("enter input to input, quit to quit, show to enter next menu")
        if (choice == "input"):
            promptInput()
        elif choice == "quit":
            break
        elif choice == "show":
            choice = input("enter show for show all the data, enter tidy for re-input each actions in data")
            if choice == "show":
                demonstration()
            if choice == "tidy":
                completeActions(getData("data.json"))

#新建一个活动为大分类的字典，遍历整个字典，整理活动
def demonstration():
    #获取基本的数据
    data = getData("data.json")
    
    #新建需要的变量
    actions = {}
    totalTime = 0
    
    #输出模块
    for date in data: #输出每一天
        for action_dict in data[date]: #遍历每一天的每个字典,输出类似a{"A":1,"B":2}
            action_str = action_dict["action"] #这里的action_dict是每个行动的集合
            #但是按理来说，这里为什么可以遍历每个行动呢？明明action_dict按理来说只会被遍历到一次啊？那么action_str也只应该有一个值？
            if action_str not in actions:
                actions[action_str] = 0 #暂时先把它当作总时长，不管细节
            actions[action_str] += action_dict["timespan"]
            totalTime += action_dict["timespan"]
    
    for action_str in actions:
        print(f"action:{action_str} timespan:{actions[action_str]} {(actions[action_str]/totalTime)*100}% of total time")


    
