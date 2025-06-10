from validations import formatValidation, rangeValidation
from parseInput import inputTimespan, parseDataIntoList
from save_and_load import firstSaveData, getData, saveData

def promptInput():
    # use a while loop, rather than a function to prompt input
    while True:
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
        
        #检测是否data为空，然后选择不同的输入function
        temp = getData()
        if not temp:
            firstSaveData(data)
        else:
            saveData(date,actions)