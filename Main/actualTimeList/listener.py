import tkinter as tk
from GUI_Classes import BasicEntry
from actualTimeList.stateMachineParser import UserActionType,InputState,stateMachineParser_API

actionDataLoc = "actionData.json"

class InputFrame(tk.Frame):
    """  ------- 构造函数初始化 ------ """
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        
        #  ------ 创建entry ------
        self.fastEntry = BasicEntry(self)
        self.fastEntry.pack(side = "bottom",fill="x", expand=True)
        
        #  ------ 把entry和具体的函数绑定 ------
        self.fastEntry.bind("<return>",self._on_return_key_FUNC)
        self.fastEntry.bind("<KeyRelease>",self._on_key_release_FUNC)
        self.fastEntry.bind("<Up>",self._on_arrow_key_FUNC)
        self.fastEntry.bind("<Down>",self._on_arrow_key_FUNC)

        #  ------ 存储当前的状态 ------
        self.currentState = InputState.AWAIT_START
        
        #  ------ 初始化dropdown ------
        self.dropdown = tk.Listbox(self)
        self.dropdown.place_forget()
        
        
    
    """ ------ UNIVERSAL FUNCTION ----- """
    #UNIVERSAL; INPUT dict userAction(state,text,eventType); UPDATE state and property above
    def processEvent_API(self,userAction):
        #  ------ 获取需要的变量 ------
        currentState = userAction["currentState"]
        text = userAction["text"]
        eventType = userAction["eventType"]
        
        userAction = stateMachineParser_API(currentState,text,eventType,actionDataLoc)
    
    #UNIVERSAL; INPUT nothing; OUTPUT currentState
    def parsingCurrentState(self):
        return self.currentState
    
    
    """ ------ SPECIFIC FUNCTION ------ """
    #SPECIFIC; INPUT key_release event; DETECT key release and solve it
    def _on_key_release_FUNC(self,event):
        #  ------ 判断是否是需要的状态 ------
        if event.keysym == "<BackSpace>" or len(event.char) == 1:
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
        if visible and selected:
            eventType = UserActionType.CONFIRM_SELECT 
        elif self.currentState == InputState.AWAIT_ACTION_DETAIL:
            eventType = UserActionType.FINAL_SUBMIT
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
        

    
