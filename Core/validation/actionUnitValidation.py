from PyQt6.QtCore import QTime

def actionUnitValidation(actionUnit):
    start = actionUnit["start"]
    end = actionUnit["end"]
    action_type = actionUnit["action_type"]
    
    # 支持 10:46 这种带冒号格式
    startTime = QTime.fromString(start, "HH:mm")
    endTime = QTime.fromString(end, "HH:mm")
    
    if not startTime.isValid():
        return "start"
    if not endTime.isValid():
        return "end"
    if action_type.lower() not in ("work","waste","rest","unknown"):
        return "actionDetail"
    if not startTime < endTime:
        return "time span"
    
    return True