"""
This is a PRESENTER class integrate different function of validation, change input to get different validation
(for now.. i dont think now i should sepearate the functions in the early time)
INPUT 1 actionUnit at a time
OUTPUT True for not wrong, name of key for wrong
"""
from Core.validation.actionUnitValidation import actionUnitValidation


class InputValidation():
    def __init__(self):
        pass
    
    def validation(data,module):
        #  --- 判断是什么服务 ---
        if module == "actionUnit":
            valid = actionUnitValidation(data)
            if valid != True:
                return valid
            
        elif module == "actionUnits":
            for actionUnit in data:
                valid = actionUnitValidation(actionUnit)
                if valid != True:
                    return valid
        
        else:
            return True
    
    