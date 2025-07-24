from Core.Definitions import ActionType, Indicators, getEnumValueDict_API
from Core.analysis.APITools import getTotalTime_API


lineIndicator = Indicators.LINE_INDICATOR.value
firstIndicator = Indicators.FIRST_INDICATOR.value
secondIndicator = Indicators.SECOND_INDICATOR.value
firstCount = Indicators.FIRST_COUNT.value
secondCount = Indicators.SECOND_COUNT.value

def dateValidation_API(date):
    try:
        parts = date.split("-")
        if len(parts) != 3:
            return False
        year, month, day = parts
        if not (year.isdigit() and len(year) == 4):
            return False
        if not (month.isdigit() and len(month) == 2 and 1 <= int(month) <= 12):
            return False
        if not (day.isdigit() and len(day) == 2 and 1 <= int(day) <= 31):
            return False
        return True
    except Exception:
        return False

    
#UNIVERSAL; INPUT str time, start and end; VALIDATE if the time period reasonable    
def isValidTimePeriod_API(start,end):
    start = getTotalTime_API(start)
    end = getTotalTime_API(end)
    if end < start:
        return False
    return True

#UNIVERSAL; INPUT str time; VALIDATE if reasonable
def isValidTimeStr_API(time):
    parts = time.split(":")
    if len(parts) != 2:
        return False
    hour, minute = parts
    if not (hour.isdigit() and minute.isdigit()):
        return False
    hour = int(hour)
    minute = int(minute)
    if hour < 0 or hour >= 24:
        return False
    if minute < 0 or minute >= 60:
        return False
    return True


#UNIVERSAL; INPUT: str data,str symbol, int time; VALIDATE: the time of symbol match the symbol in data
def validate_Symbol_Count_API(data,symbol,expectedCount):
    return data.count(symbol) == expectedCount
        
    
#UNIVERSAL; INPUT: data and two symbol and their count; VALIDATE:是否有{firstIndicator}两个和{secondIndicator}两个
def structureValidation_API(data,firstIndicator,secondIndicator,firstCount,SecondCount):
    if validate_Symbol_Count_API(data,firstIndicator,firstCount) == False:
        return False
    #这里由于没有减去firstIndicator的 - 导致错误
    #我的测试数据是11:10 - 11:20 - WORK-看书-after virtue 第三章
    if validate_Symbol_Count_API(data.split(" - ")[2],secondIndicator,SecondCount) == False:
        return False
    return True


#UNIVERSAL; input str originval data; VALIDATE+OUTPUT indicators
def validateIndicator_API(orgingalData):
    #检查每一行的indicator
    lines = orgingalData.split('\n')
    del lines[0]
    for item in lines:
        if structureValidation_API(item, firstIndicator, secondIndicator, firstCount, secondCount) == False: 
            return("there's something wrong in the structure of the data! please check")
    return True
    
    
#UNIVERSAL; INPUT indicator(maybe user setting list in the future) and dict data; Validate/OUTPUT error message 
def validateData_API(userData):
    enumVal = getEnumValueDict_API(ActionType)
    #检查时间
    for date in userData:
        if dateValidation_API(date) == False:
            return("wrong in date")
        for actionInfo in userData[date]:
            if isValidTimePeriod_API(actionInfo["start"],actionInfo["end"]) == False:
                return("wrong in time period")
            if isValidTimeStr_API(actionInfo["start"]) == False or isValidTimeStr_API(actionInfo["end"]) == False:
                return("wrong in time")
            if actionInfo["action_type"].lower() not in enumVal:
                return("wrong in action type")
    return True
        
        
        
        
        
