"""
我暂时的思路就是在其他的py文件里面存universal的function，至于把它们运用起来就放在main，也就是说validation也要在main
首先使用while输入数据,把它转换为通用的json格式
然后validate,如果validate = true 就存进里面
由于是按天数存放的，不可能出现两天一样的情况

额外信息：可能需要在每一步加上debug信息，但那是后面的事情了
"""
import json
from validations import formatValidation, rangeValidation
from parseInput import inputTimespan, parseDataIntoList
from save_and_load import firstSaveData, getData, saveData

#Main function start
print("welcome to the time-integrater, it is a gadget that helps you to analyze your time distribusion")

# use a while loop, rather than a function to prompt input
while True:
    #input the data
    userData = input("input your data")
    date = input("what date is it today? please enter in the form of 2025/6/10")
    
    #TODO:presence check
    
    #TODO:use strip to delete spaces
    
    #TODO:change it into discard redundant space in data
    #userData = discardSpace(userData)
    
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
    
    #检测是否data为空，输入
    temp = getData()
    if not temp:
        firstSaveData(data)
    else:
        saveData(date,actions)
    
    