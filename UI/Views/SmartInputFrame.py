import tkinter as tk

from Core.Definitions import InputState, UserActionType
from Core.logic.stateMachineParser import getAutoCompletion_API, stateMachineParser_API
from Core.translation.fastEnterTranslation import transFastEnter_API
from UI.Views.propertyViewFrame import PropertyViewFrame
from UI.Widgets.Small_widgets.BasicEntry import BasicEntry
from UI.Widgets.Frames.DropdownManager import DropdownManager

actionDataLoc = "Data/actionData.json"

class SmartInputFrame(tk.Frame):
    """  ------- 构造函数初始化 ------ """
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        
        #  ------ 创建entry -----
        self.fastEntry = BasicEntry(self)
        self.fastEntry.pack(side = "top",fill="x", expand=True)
        
        #  ------ 把entry和具体的函数绑定 ------
        self.fastEntry.bind("<Return>",self._on_return_key_FUNC)
        self.fastEntry.bind("<KeyRelease>",self._on_key_release_FUNC)
        self.fastEntry.bind("<Up>",self._on_arrow_key_FUNC)
        self.fastEntry.bind("<Down>",self._on_arrow_key_FUNC)

        #  ------ 存储当前的状态 ------
        self.currentState = InputState.AWAIT_START
                    
        #  ------ 初始化propertyFrame ------
        self.propertyFrame = PropertyViewFrame(self,self._on_property_view_change)
        self.propertyFrame.pack(side = "bottom",fill="x", expand=True)
        
        #  ------ 实例化Dropdown manager ------
        self.dropdownManager = DropdownManager(self)
        

    """  ------ PROCESS EVENT ------ """
    #UNIVERSAL; INPUT dict userAction(state,text,eventType); UPDATE state and property above
    def processEvent_API(self,userAction):
        #  ------ 获取需要的变量 ------
        currentState = userAction["currentState"]
        text = userAction["text"]
        eventType = userAction["eventType"]
        
        #  ---------- 询问状态机，给出建议 ----------
        suggestion = stateMachineParser_API(currentState,text,eventType,userAction)
        
        #  ------ 修改速记提示框的显示 ------
        if eventType == UserActionType.CONFIRM_SELECT:
            #  --- 判断是否action为空 ---
            actionList = getAutoCompletion_API(actionDataLoc)
            action_to_replace = transFastEnter_API(text,actionList).get("data", {}).get("action", "")
        
            # 2. 获取状态机确认“之后”的action是什么
            new_action = suggestion["data"]["action"]

            # 3. 执行替换
            if action_to_replace and new_action: # 只有当之前确实解析出了一个action时才替换
                newText = text.replace(action_to_replace, new_action, 1)
                self.fastEntry.setEntry(newText)
            else: # 如果之前没解析出来，就直接追加
                self.fastEntry.setEntry(self.fastEntry.get() + new_action)

        #  ------ 实施建议 ------
        #  --- GUI ---
        GUIData = suggestion["data"]
        #这里可能出问题
        PropertyViewFrame.updateView_FUNC(self.propertyFrame,GUIData)
        
        #  ---------- 下拉列表替换 ----------
        #  --- 隐藏下拉列表 ---
        self.dropdownManager.hideTopLevel()
        
        #  --- 插入新东西 ---
        if suggestion["suggestList"] != []:
            if self.focus_get() == self.fastEntry:
                self.dropdownManager.showDropdown(self.fastEntry,suggestion["suggestList"])
            elif self.focus_get() == self.propertyFrame.entries["action"]:
                #  --- 获取控件 ---
                actionProperty = self.propertyFrame.entries["action"]
                self.dropdownManager.showDropdown(actionProperty,suggestion["suggestList"])
            
    
    #SPECIFIC; INPUT nothing; OUTPUT currentState
    def parsingCurrentState(self):
        return self.currentState

    def updateFastEntry(self,text):
        self.fastEntry.setEntry(text)

    """ ------ SPECIFIC FUNCTION ------ """
    #SPECIFIC; INPUT key_release event; DETECT key release and solve it
    def _on_key_release_FUNC(self,event):
        #  ------ 判断是否是需要的状态 ------
        if event.keysym == "BackSpace" or len(event.char) == 1:
            eventType = UserActionType.TEXT_INPUT
        else:
            return 
        
        #  ------ 打包 ------
        userAction = {
            "currentState":self.parsingCurrentState(),
            "text":self.fastEntry.get(),
            "eventType": eventType
        }
        
        #  ------ 调用函数修改状态 ------
        self.processEvent_API(userAction)
        
    #SPECIFIC; INPUT nothing; DETECT user press on enter and solve it
    def _on_return_key_FUNC(self,event): #这里的event是否用不到？
        #  ------ 判断是否是需要的状态 ------
        visible = self.dropdownManager.ifDropdownCanBeSeen() #是否可以被用户看见
        selected = self.dropdownManager.getDropdownList() #是否被选中
        
        
        #  ------ 判断逻辑 ------
        if visible and selected != None:
            eventType = UserActionType.CONFIRM_SELECT 
            index = selected[0]
            selectedVal = self.dropdownManager.getDropdownVal(index)
        elif self.currentState == InputState.AWAIT_ACTION_DETAIL:
            eventType = UserActionType.FINAL_SUBMIT
        else:
            return
        
        #  ------ 打包 ------
        userAction = {
            "currentState": self.parsingCurrentState(),
            "text": self.fastEntry.get(),
            "eventType": eventType,
            "selectedVal": selectedVal #打包用户选中的值
        }
        
        #  ------ 调用函数修改状态 ------ 
        self.processEvent_API(userAction)

    #SPECIFIC; INPUT text; UPDATE fast entry
    def _on_property_view_change(self,text):
        if self.fastEntry.get() != text:
            self.fastEntry.setEntry(text)
        
        
    #SPECIFIC; INPUT nothing; DETECT arrow up and down pressed
    def _on_arrow_key_FUNC(self,event):
        #  ------ 判断 ------
        if self.dropdownManager.ifDropdownCanBeSeen():
            if event.keysym == "Up" and self.dropdownManager.getDropdownList(): #如果没有选中不能往上
                self.dropdownManager.updateDropdown(UserActionType.ARROW_UP)
            elif event.keysym == "Down":
                self.dropdownManager.updateDropdown(UserActionType.ARROW_DOWN)
        else:
            return
        return "break"

                
        

