import uuid

from ti.dataAccess.dataAccess import getData
from ti.core.definitions import YESTERDAY

"""
这个文件用来存储数据相关的操作，作为
"""
class DataService:
    def __init__(self):
        self.allData = getData("Data/dateData")
    
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
        return self.allData[YESTERDAY]
    
    