from APIs.parseInput import getTotalTime_API


def timeValidation(hour,minutes):
    if int(hour) < 0 or int(hour) > 24:
        return False
    else:
        if int(minutes) < 0 or int(minutes) > 60:
            return False
    return True

#The function is aim to fix the format
#It receive start as example, and return the end
def formatValidation(start,end):
    if len(end) == 2:
        end = start[0:2] + ":" + end
    return end 

#狗屎一样的代码，为什么不写成universal? 这下没法复用了
def rangeValidation(actions):
    for i in range (len(actions)):
        pre = actions[i]["start"]
        post = actions[i]["end"]
        #validate the time
        if not timeValidation(pre[0:2],pre[3]) and not timeValidation(post[0:2],post[3]):
            return False
        
        #validate ascending
        if int(pre[0:2]) > int(post[0:2]):
            return False
        if int(pre[0:2]) == int(post[0:2]) and int(pre[3]) > int(post[3]):
            return False
    return True


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
    if validate_Symbol_Count_API(data,secondIndicator,SecondCount) == False:
        return False
    return True
        
        
        
        
        
        
        
