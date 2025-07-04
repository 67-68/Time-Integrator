from enum import Enum

class InputState(Enum):
    AWAIT_START = "awaitStart"
    AWAIT_END = "awaitEnd"
    AWAIT_ACTION_TYPE = "awaitActionType"
    AWAIT_ACTION = "awaitAction"
    AWAIT_ACTION_DETAIL = "awaitActionDetail"
    COMPLETE = "complete"

class UserActionType(Enum):
    TEXT_INPUT = "textINPUT"
    ARROW_UP = "arrowUp"
    ARROW_DOWN = "arrowDown"
    CONFIRM_SELECT = "confirmSelect" #虽然他们不是很用得到...但还是不删了，哪怕不再是同一个function用的
    FINAL_SUBMIT = "finalSubmit"

class ActionType(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"
    
class Indicators(Enum):
    LINE_INDICATOR = '\n' #把输入的行分开
    FIRST_INDICATOR = " - " #把输入分成三个基本的模块：两个时间和一个行动
    SECOND_INDICATOR = "-" #在行动内细分
    FIRST_COUNT = 2
    SECOND_COUNT = 2

#应用内基本GUI操作通信协议，相当于PyQT原生信号的enum版本
class RawUserAction(Enum):
    TEXT_CHANGED = "textChanged"
    RETURN_PRESSED = "returnPressed"


#UNIVERSAL; INPUT enum ActionType; OUTPUT list of enum abbreviations
def getEnumAbbriviation(enumClass):
    temp = {
            "w":"work",
            "s":"waste",
            "u":"unknown",
            "r":"rest"
    }
    if enumClass == ActionType:
        return temp
    
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