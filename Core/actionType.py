from Core.json_Interaction import getData_API
from Core.definitions import ActionType

#  ------ 输出 ------
# 输出Enum的value
def getEnumValue_API(enumClass):
    temp = []
    for item in enumClass:
        temp.append(item.value)
    return temp

def getEnumValueDict_API(enumClass):
    temp = {}
    for item in enumClass:
        temp[item.value] = {"timeSpan":0}
    return temp

#把action及其属性输出为字符串
def getActionDataStr_API():
    list = getEnumValue_API(ActionType)
    temp = ""
    for i in list:
        temp += i 
        temp += "\n"
    actiondict = getData_API("action_integration.json") #这个时候它应该是一个大字典{行动{行动细节}}
    for action in actiondict:
        temp += f"{action}:{actiondict[action]['action_type']}\n"
    print("successfully make String data")
    return temp

#  ------ 查找 ------ 
#UNIVERSAL; INPUT cateDict; OUTPUT str
def getStrCateTime_FUNC(cateDict):
    temp = ""
    totalTime = 0
    for item in cateDict:
        totalTime += cateDict[item]["timeSpan"]
    for item in cateDict:
        time = cateDict[item]["timeSpan"]
        if totalTime != 0:
            temp += f"{item}:{time}, take {time/totalTime*100} account of total time \n"
        else:
            temp += f"{item}:{time}, take N/a account of total time \n"
    return temp

#UNIVERSAL; INPUT enumName,dict; OUTPUT dict with enum name as key
def fillDictEnum_API(dict,enum):
    enum = getEnumValue_API(enum)
    for element in enum:
        dict[element] = None
    
    
        
        


    

    