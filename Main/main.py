"""
This gadget should have two input for now: the text that is the schedule of the user, and the choice of user.
This function aim to popularize a dictionary called actions use the user input
The function is designed to use many times, therefore it should first find the actions
"""
import json
from Main.parseInput import inputFormatChange, timeCompare
from Main.save_and_load import saveData
import Main.inputData as inputData
from validations import timeValidation





#Main function start
print("welcome to the time-integrater, it is a gadget that helps you to analyze your time distribusion")

#input the data, I put the function of transform it to normal data in the inputData. I also put the validation of data in it
userData = inputData()

for i in range(1,len(userData),2):
    #这里，写个东西把数据输入到timespan里面，然后写个东西给savedata也输进去
    timespan = timeCompare(beforeHour,beforeMinute,afterHour,afterMunite)
    saveData(before,after,userData[index],timespan)



