
from ti.core.translation.fastEnterTranslation import transFastToProp_API
from ti.core.translation.propertyTranslation import transPropToFast_API
from ti.dataAccess.dataAccess import getData


class Translator:
    def __init__(self):
        pass
    
    def fastToProper(self,data):
        actionList = getData("Data/actionList.json")
        actions = []
        for key in actionList:
            actions.append(key)
        
        data = transFastToProp_API(data,actions) 
        return data
    
    def properToFast(self,data):
        data = transPropToFast_API(data)
        return data