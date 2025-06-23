#UNIVERSAL; INPUT a set of property; OUTPUT fast entry str
def transPropToFast_API(properties):
    text = ""
    
    #  ------ START ------
    if properties["start"][:2].isdigit() and properties["start"].find(":") == 2:
        start = properties["start"]
        if len(start) > 2:
            start = f'{start[:2]}{start[3:5]}'
    
    #  ------ END ------
    end = properties["end"]
    if properties["start"][:2] == end[:2]:
        end = end[3:]
    else:
        end = end[:2] + end[3:]
    
    #  ------ ACTION_TYPE ------
    actionType = properties["action_type"]
    if actionType.lower() == "work":
        actionType = "w"
    elif actionType.lower() == "waste":
        actionType = "s"
    elif actionType.lower() == "rest":
        actionType = "r"
    else:
        actionType = ""
    
    #  ------ ACTION ------
    action = properties.get("action","") 
    
    #  ------ ACTION_DETAIL ------
    actionDetail = properties["actionDetail"]
    
    #  ------ 最终加和 ------
    for item in (start,end,actionType,action,actionDetail):
        if item != None:
            text += item
    

    
    return text
