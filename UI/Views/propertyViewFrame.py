import tkinter as tk

from Core.analysis.APITools import getAutoCompleteWithKey_API, getAutoCompletion_API
from Core.translation.propertyTranslation import transPropToFast_API
from UI.Widgets.Small_widgets.BasicEntry import BasicEntry
from UI.Widgets.Small_widgets.BasicLabel import BasicLabel
from UI.Widgets.Frames.DropdownManager import DropdownManager

actionDataLoc = "Data/actionData.json"

class PropertyViewFrame(tk.Frame):
    """  ------- 构造函数初始化 ------ """
    def __init__(self, master,_on_change_callback = None,**kwargs):
        super().__init__(master,**kwargs)
        
        #  ------ 初始化回调函数 ------
        self._on_change_callback = _on_change_callback
    
        #  ------ 初始化属性 ------
        properties = {
            "start":4,
            "end":4,
            "action_type":6,
            "actionDetail":20,
            "action":10
        }
        
        #  ------ 初始化属性entry ------
        self.entries = {}
        
        for property in properties:
            self.entries[property] = BasicEntry(self,width = properties[property])
        
        self.entries["start"].grid (row = 1,column = 0,padx = 5)
        self.entries["end"].grid(row = 1,column = 1,padx = 5)
        self.entries["action_type"].grid(row = 1, column = 2,padx = 5)
        self.entries["action"].grid(row = 1, column = 3,padx = 5)
        self.entries["actionDetail"].grid(row = 1,column = 4,padx = 5)
        
        #  ------ 初始化属性label ------
        self.startLabel = BasicLabel(self,"start time")
        self.endLabel = BasicLabel(self,"end time")
        self.typeLabel = BasicLabel(self,"type of action")
        self.actionLabel = BasicLabel(self,"name of action")
        self.detailLabel = BasicLabel(self,"detail of action")
        self.startLabel.grid (row = 0,column = 0,padx = 5)
        self.endLabel.grid(row = 0,column = 1,padx = 5)
        self.typeLabel.grid(row = 0, column = 2,padx = 5)
        self.actionLabel.grid(row = 0, column = 3,padx = 5)
        self.detailLabel.grid(row = 0,column = 4,padx = 5)

        #  ------ 初始化属性entry绑定函数 ------
        for property in properties:
            self.entries[property].bind("<KeyRelease>",self._on_Release_Key)
        
        #  ------ 初始化下拉列表 ------
        self.dropdown = DropdownManager(self)
        
            
    #SPECIFIC; INPUT dict; UPDATE entries
    def updateView_FUNC(self,data):
        for item in data:
            self.entries[item].setEntry(data[item])
    
    #SPECIFIC; INPUT event <FocusOut>; UPDATE fastEntry
    def _on_Release_Key(self,event):
        properties = {}
        for widget in self.entries:
            properties[widget] = self.entries[widget].get()
        #  --- 翻译 ---
        text = transPropToFast_API(properties)
        
        #  --- 同步 ---
        self._on_change_callback(text)
        
        #  --- 判断是否是action ---        
        focus = self.focus_get()
        if focus == self.entries["action"]:
            #获取ActionList
            actionList = getAutoCompletion_API(actionDataLoc)
            keyList = getAutoCompleteWithKey_API(properties["action"],actionList)
            
            #设置dropdown
            self.dropdown.showDropdown(self.entries["action"],keyList)
            
        else:
            #默认隐藏dropdown
            self.dropdown.hideTopLevel()
            
        