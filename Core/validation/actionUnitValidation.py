from PyQt6.QtCore import QTime

def actionUnitValidation(actionUnit):
    start = actionUnit["start"]
    end = actionUnit["end"]
    action_type = actionUnit["action_type"]
    
    #  --- check time ---
    if not QTime.fromString(start,"HHMM").isValid():
        return "start"
    if not QTime.fromString(end,"HHMM").isValid():
        return "end"
    if action_type.lower() not in ("work","waste","rest","unknown"):
        return "actionDetail"