from Core.dataAccess.dataManager import getData_API
from Core.translation.propertyTranslation import transPropToFast_API
from Core.translation.fastEnterTranslation import transFastToProp_API

class Translator:
    def __init__(self):
        pass
    
    def fastToProper(self,data):
        actionData = getData_API("Data/actionData.json")
        actions = []
        for key in actionData:
            actions.append(key)
        
        data = transFastToProp_API(data,actions) 
        return data
    
    def properToFast(self,data):
        data = transPropToFast_API(data)
        return data