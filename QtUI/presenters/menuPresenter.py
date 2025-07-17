from Core.analysis.otherAnalysis import getExtremeData, getFourRealmRatio, getHighQualityRatio
class MenuPresenter():
    def __init__(self):
        pass
    
    def processData(self,actionUnits):
        #  --- 然后调用函数处理actionUnit ---
        timeUseRate = getHighQualityRatio(actionUnits)
        fourRealmRatio = getFourRealmRatio(actionUnits)
        extremeData = getExtremeData(actionUnits)
        
        timeUseRateStr = self.organizeTimeRate(timeUseRate)
        fourRealmRatioStr = self.organizeRealmRatio(fourRealmRatio)
        extremeDataStr = self.organizeExtremeData(extremeData)
        
        return timeUseRateStr,fourRealmRatioStr,extremeDataStr
    
    #UNIVERSAL; INPUT time ratio data; OUTPUT str
    def organizeTimeRate(self,data):
        return int(data) * 100
    
    def organizeRealmRatio(self,ratios):
        for key in ratios:
            ratios[key] = (ratios[key]*100)
        return ratios
    
    def organizeExtremeData(self,extremeData):
        output = ""
        for key in extremeData:
            data = extremeData[key]
            #我很奇怪为什么有些数据有date有些没有...无论如何我得想另一个办法找到date...我还是给所有数据都popularize date好了
            date = data["date"]
            start = data["start"]
            end = data["end"]
            important = "important"
            if not data["importance"]:
                important = "not " + important
            urgent = "urgent"
            if not data["urgency"]:
                urgent = "not " + urgent
            
            output += f'in {date},{start}-{end},you do the longest time of {important} and {urgent} things \n'
            
        return output
    
