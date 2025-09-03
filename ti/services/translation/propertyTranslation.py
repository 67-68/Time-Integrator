#UNIVERSAL; INPUT a set of property; OUTPUT fast entry str
def transPropToFast_API(properties):
    text = ""
    start = None
    end = None
    action = None
    actionDetail = None
    actionType = None
    
    if properties is None:
        return ""
    
    #  ------ START ------
    if properties["start"] != None:
        if properties["start"][:2].isdigit() and properties["start"].find(":") == 2:
            start = properties["start"]
            if len(start) > 2:
                start = f'{start[:2]}{start[3:5]}'
        else:
            start = properties["start"]
    
    #  ------ END ------
    if properties["end"] is not None:
        end = properties["end"]
        if properties["start"][:2] == end[:2]:
            end = end[3:]
        else:
            end = end[:2] + end[3:]
    
    #  ------ ACTION_TYPE ------
    if properties["action_type"] is not None:
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
    if properties["action"] is not None:
        action = properties.get("action","") 
    
    #  ------ ACTION_DETAIL ------
    if properties["actionDetail"] is not None:
        actionDetail = properties["actionDetail"]
    
    #  ------ 最终加和 ------
    for item in (start,end,actionType,action,actionDetail):
        if item != None:
            text += item
    

    
    return text
