import uuid

from ti.dataAccess.dataAccess import getData, saveData
from ti.core.definitions import YESTERDAY

"""
这个文件用来存储数据相关的操作，作为
"""
class DataService:
    def __init__(self):
        self.data = getData("Data/dateData.json")
    
    def createNewData(self):
        return {
            "id":str(uuid.uuid4()),
            "date":"",
            "action":"",
            "start":"",
            "end":"",
            "action_type":"",
            "actionDetail":"",
            "timeSpan":""
            }
    
    def get_yesterday_AU(self):
        return self.data[YESTERDAY]
    
    def add_actionUnit(self,au):
        date = au["date"]
        
        if date not in self.data:
            self.data[date] = []
            
            
        assign = None
        curData = self.data[date]
        #这里是针对一般数据的修改模块
        for i in range (len(curData)):
            if curData[i]["id"] == au["id"]:
                curData[i] = au
                assign = True
                break
        if assign != True:
            curData.append(au)
        
        self.data[date] = curData
        
        saveData(self.data,"Data/dateData")
        
    def get_date_data(self,date):
        return self.data[date] if date in self.data else {}
    
    def get_data(self):
        return self.data
    