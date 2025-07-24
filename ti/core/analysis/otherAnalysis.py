

#UNIVERSAL; INPUT list actionUnits; OUTPUT high quality time ratio
from ti.dataAccess.dataAccess import getData, saveData


def getHighQualityRatio(actionUnits):
        totalTime = 0
        totalHighQuaTime = 0
        for actionUnit in actionUnits:
                timeSpan = actionUnit["timeSpan"]
                if actionUnit["urgency"] and actionUnit["importance"]:
                        totalHighQuaTime += timeSpan
                if actionUnit["importance"]:
                        totalHighQuaTime += timeSpan
                totalTime += timeSpan
                
                if timeSpan != 0:
                        return totalHighQuaTime / timeSpan
                return 0

def getFourRealmRatio(actionUnits):
        totalTime = {
                "total":0,
                "urgency":0,
                "importance":0,
                "urgencyAndImpor":0,
                "notUrgencyAndNotImpor":0
        }
        
        ratio = {
                "urgency":0,
                "importance":0,
                "urgencyAndImpor":0,
                "notUrgencyAndNotImpor":0
        }
        
        for actionUnit in actionUnits:
                timeSpan = actionUnit["timeSpan"]
                
                #  ------ 逻辑判断 ------
                if actionUnit["urgency"] and actionUnit["importance"]:
                        totalTime["urgencyAndImpor"] += timeSpan
                
                elif actionUnit["urgency"] and not actionUnit["importance"]:
                        totalTime["urgency"] += timeSpan
                
                elif not actionUnit["urgency"] and actionUnit["importance"]:
                        totalTime["importance"] += timeSpan
                
                elif not actionUnit["urgency"] and not actionUnit["importance"]:
                        totalTime["notUrgencyAndNotImpor"] += timeSpan
                
                totalTime["total"] += timeSpan
                
                #  ------ 计算 ------
                if totalTime["total"] != 0:        
                        for key in ratio:
                                ratio[key] = totalTime[key] / totalTime["total"]
                return ratio
                
        return

def getExtremeData(actionUnits):
        actionUnit = {
            "start": "",
            "end": "",
            "action": "",
            "action_type": "",
            "actionDetail": "",
            "timeSpan": 0,
            "date": "",
            "urgency": None,
            "importance": None
        }
        
        extremeData = {
                "maxImporAndUrgen":actionUnit,
                "maxImpor":actionUnit,
                "maxNotImporAndNotUrgen":actionUnit,
                "maxUrgen":actionUnit
        }
        for actionUnit in actionUnits:
                maxImporAndUrgen = extremeData["maxImporAndUrgen"]["timeSpan"]
                maxImpor = extremeData["maxImpor"]["timeSpan"]
                maxNotImporAndNotUrgen = extremeData["maxNotImporAndNotUrgen"]["timeSpan"]
                maxUrgen = extremeData["maxUrgen"]["timeSpan"]
                
                impor = actionUnit["importance"]
                urgen = actionUnit["urgency"]
                timeSpan = actionUnit["timeSpan"]
                
                #我想这里可以用一系列的循环和字典,例如[impor]{[impor],[urgen]}来搞定...但我还是老老实实写逻辑好了
                if impor and urgen:
                        if timeSpan > maxImporAndUrgen:
                                extremeData["maxImporAndUrgen"] = actionUnit
                elif impor and not urgen:
                        if timeSpan > maxImpor:
                                extremeData["maxImpor"] = actionUnit
                elif not impor and not urgen:
                        if timeSpan > maxNotImporAndNotUrgen:
                                extremeData["maxNotImporAndNotUrgen"] = actionUnit
                elif urgen and not impor:
                        if timeSpan > maxUrgen:
                                extremeData["maxUrgen"] = actionUnit

        return extremeData

#输入一个au，而不是一个au list
def updateActionList(actionUnit):
        actionList = getData("Data/actionList.json")
        
        if actionUnit["action"] not in actionList:
                actionList.append(actionUnit["action"])
                        
        saveData(actionList,"Data/actionList.json")