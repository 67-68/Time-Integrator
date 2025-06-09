def timeValidation(hour,minutes):
    if hour < 0 or hour > 24:
        return False
    else:
        if minutes < 0 or minutes > 60:
            return False
    return True

#The function is aim to fix the format
#It receive start as example, and return the end
def formatValidation(start,end):
    if len(end) == 2:
        end = start[0:2] + ":" + end
    return end 

def rangeValidation(actions):
    for i in range (len(actions)):
        pre = actions[i]["start"]
        post = actions[i]["end"]
        #validate the time
        if not timeValidation(pre[0:2],pre[2]) and not timeValidation(post[0:2],post[2]):
            return False
        
        #validate ascending
        if int(pre[0:2]) > int(post[0:2]):
            return False
        if int(pre[0:2]) == int(post[0:2]) and int(pre[2]) > int(post[2]):
            return False
    return True
        