

from ti.services.dataAccess.dataAccess import getData
from ti.services.translation.fastEnterTranslation import transFastToProp_API
from ti.services.translation.propertyTranslation import transPropToFast_API


class Translator:
    def __init__(self):
        pass
    
    def fastToProper(self,data):
        actionList = getData("model/data/actionList.json")
        actions = []
        for key in actionList:
            actions.append(key)
        
        data = transFastToProp_API(data,actions) 
        
        return data
    
    def properToFast(self,data):
        data = transPropToFast_API(data)
        return data
    
    