from enum import Enum

#  ---------- ENUM CLASSES ----------
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
    CONFIRM_SELECT = "confirmSelect"
    FINAL_SUBMIT = "finalSubmit"

class ActionType(Enum):
    WORK = "work"
    REST = "rest"
    WASTE = "waste"
    UNKNOWN = "unknown"
    
    

#  ---------- 
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