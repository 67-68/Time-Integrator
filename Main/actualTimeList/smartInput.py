import tkinter as tk
from GUI_Classes import BasicEntry,BasicLabel
from actualTimeList.stateMachineParser import UserActionType,InputState,stateMachineParser_API

actionDataLoc = "actionData.json"

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
        
        #  ------ 初始化dropdown ------
        self.dropdown = tk.Listbox(self)
        self.dropdown.place_forget()
        
        #  ------ 初始化propertyFrame ------
        self.propertyFrame = PropertyViewFrame(self)
        self.propertyFrame.pack(side = "bottom",fill="x", expand=True)
        
        
    
    """ ------ UNIVERSAL FUNCTION ----- """
    #UNIVERSAL; INPUT dict userAction(state,text,eventType); UPDATE state and property above
    def processEvent_API(self,userAction):
        #  ------ 获取需要的变量 ------
        currentState = userAction["currentState"]
        text = userAction["text"]
        eventType = userAction["eventType"]
        
        #  ------ 询问状态机，给出建议 ------
        suggestion = stateMachineParser_API(currentState,text,eventType,userAction)
        
        #  ------ 修补:修改速记提示框的显示 ------
        if eventType == UserActionType.CONFIRM_SELECT:
            currentText = self.fastEntry.get()
            currentText -= suggestion["previousAction"]
            currentText += suggestion["data"]["action"]
            self.fastEntry.setEntry(currentText)
            #这里可能出问题，我对函数不熟悉
        
        #  ------ 实施建议 ------
        #  --- GUI ---
        GUIData = suggestion["data"]
        #这里可能出问题
        PropertyViewFrame.updateView_FUNC(self.propertyFrame,GUIData)
    
    #UNIVERSAL; INPUT nothing; OUTPUT currentState
    def parsingCurrentState(self):
        return self.currentState
    
    
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
        visible = self.dropdown.winfo_ismapped() #是否可以被用户看见
        selected = self.dropdown.curselection() #是否被选中
        
        
        #  ------ 判断逻辑 ------
        if visible and selected != None:
            eventType = UserActionType.CONFIRM_SELECT 
            selectedVal = self.dropdown.get(selected[0])
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

    #SPECIFIC; INPUT nothing; DETECT arrow up and down pressed
    def _on_arrow_key_FUNC(self,event):
        #  ------ 判断 ------
        if self.dropdown.winfo_ismapped():
            if event.keysym == "Up" and self.dropdown.curselection(): #如果没有选中不能往上
                eventType = UserActionType.ARROW_UP
            elif event.keysym == "Down":
                eventType = UserActionType.ARROW_DOWN
        else:
            return
        
        #  ------ 打包 ------
        userAction = {
            "currentState": self.parsingCurrentState(),
            "text": self.fastEntry.get(),
            "eventType": eventType
        }
        
        #  ------ 调用函数修改状态 ------ 
        self.processEvent_API(userAction)
        return "break"
    

"""  ---------- 新建属性栏类 ---------- """
class PropertyViewFrame(tk.Frame):
    """  ------- 构造函数初始化 ------ """
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)

        properties = {
            "start":4,
            "end":4,
            "action_type":6,
            "actionDetail":20,
            "action":10
        }
        
        self.entries = {}
        
        for property in properties:
            self.entries[property] = BasicEntry(self,width = properties[property])
        
        self.entries["start"].grid (row = 1,column = 0,padx = 5)
        self.entries["end"].grid(row = 1,column = 1,padx = 5)
        self.entries["action_type"].grid(row = 1, column = 2,padx = 5)
        self.entries["action"].grid(row = 1, column = 3,padx = 5)
        self.entries["actionDetail"].grid(row = 1,column = 4,padx = 5)
        
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

    #SPECIFIC; INPUT dict; UPDATE entries
    def updateView_FUNC(self,data):
        for item in data:
            self.entries[item].setEntry(data[item])
        
