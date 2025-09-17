from ti.features.capture.model.ITranslator import ITranslator
from ti.features.translation.model.parsers import Parsers
from ti.model.action_unit import ActionUnit


class ConvTranslator(ITranslator):
    @property
    def name(self):
        return "classic_fast_entry"
    
    def trans_au(self, au:ActionUnit):
        if au == None:
            return au
        
        #  ------ START ------
        if au.get("start",None) != None:
            if au.start[:2].isdigit() and au.start.find(":") == 2:
                start = au.start
                if len(start) > 2:
                    start = f'{start[:2]}{start[3:5]}'
            else:
                start = au.start
        
        #  ------ END ------
        if au.get("end",None) is not None:
            end = au.end
            if au.start[:2] == end[:2]:
                end = end[3:]
            else:
                end = end[:2] + end[3:]
        
        #  ------ ACTION_TYPE ------
        if au.get("action_type",None) != None:
            actionType = au.action_type
            if actionType.lower() == "work":
                actionType = "w"
            elif actionType.lower() == "waste":
                actionType = "s"
            elif actionType.lower() == "rest":
                actionType = "r"
            else:
                actionType = ""
        
        #  ------ ACTION ------
        if au.get("action",None) != None:
            action = au.action
        
        #  ------ ACTION_DETAIL ------
        if au.get("action_detail",None) != None:
            action_detail = au.action_detail
        
        #  ------ 最终加和 ------
        for item in (start,end,actionType,action,action_detail):
            if item != None:
                text += item
        
        return text

    
    def trans_other(self,text) -> ActionUnit:
        """
        这个函数用来处理速记语法向actionUnit的转化
        这里可以不使用状态机解析而使用一个parser组合函数
        """
        text = Parsers.
        
    