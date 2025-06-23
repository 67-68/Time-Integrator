import tkinter as tk

from Core.Definitions import InputState, UserActionType
from Core.logic.stateMachineParser import getAutoCompletion, stateMachineParser_API
from Core.translation.fastEnter import transFastEnter_API
from UI.Views.propertyViewFrame import PropertyViewFrame
from UI.Widgets.Small_widgets.BasicEntry import BasicEntry




actionDataLoc = "Data/actionData.json"

#这里应该放到新的dropdown class里面
#UNIVERSAL; INPUT tk dropdown and int index; UPDATE dropdown
def switchDropdown(dropdown,index):
        dropdown.selection_clear(0, tk.END)  # 清除所有选中
        dropdown.selection_set(index)        # 设置选中 index
        dropdown.activate(index)             # 设置焦点
        dropdown.see(index)                  # 滚动到该项

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
        
        #  ------ 初始化dropDownTopLevel ------
        self.dropdownTop = tk.Toplevel(self)
        self.dropdownTop.withdraw()  # 初始时隐藏
        self.dropdownTop.overrideredirect(True)  # 无边框
        self.dropdownTop.attributes("-topmost", True)  # 置顶
        
        
        #  ------ 初始化dropdown ------
        self.dropdown = tk.Listbox(self.dropdownTop)
        self.dropdown.pack()
        
        #  ------ 初始化propertyFrame ------
        self.propertyFrame = PropertyViewFrame(self)
        self.propertyFrame.pack(side = "bottom",fill="x", expand=True)
        
    
    #SPECIFIC; INPUT widget and str[] item; UPDATE dropdown
    def showDropdown(self,widget,items):
        #  ------ 删除并插入 ------ 
        self.dropdown.delete(0,tk.END)
        for item in items:
            self.dropdown.insert(tk.END,item)
        
        #  ------ 获取放置数据 ------
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height()
        width=widget.winfo_width()
        
        #  ------ 放置TopLevel ------
        self.dropdownTop.geometry(f"{width}x100+{x}+{y}")  # 100 是高度，可调
        self.dropdownTop.deiconify()
        

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
            currentText = self.fastEntry.get()

            #  --- 判断是否action为空 ---
            actionList = getAutoCompletion(actionDataLoc)
            action_to_replace = transFastEnter_API(text,actionList).get("data", {}).get("action", "")
        
            # 2. 获取状态机确认“之后”的action是什么
            new_action = suggestion["data"]["action"]

            # 3. 执行替换
            if action_to_replace: # 只有当之前确实解析出了一个action时才替换
                newText = text.replace(action_to_replace, new_action, 1)
                self.fastEntry.setEntry(newText)
            else: # 如果之前没解析出来，就直接追加
                self.fastEntry.insert('end', new_action)

        #  ------ 实施建议 ------
        #  --- GUI ---
        GUIData = suggestion["data"]
        #这里可能出问题
        PropertyViewFrame.updateView_FUNC(self.propertyFrame,GUIData)
        
        #  ---------- 下拉列表替换 ----------
        #  --- 隐藏下拉列表 ---
        self.dropdownTop.withdraw()
        
        #  --- 插入新东西 ---
        if suggestion["suggestList"] != []:
            if self.focus_get() == self.fastEntry:
                SmartInputFrame.showDropdown(self,self.fastEntry,suggestion["suggestList"])
            elif self.focus_get() == self.propertyFrame.entries["action"]:
                #  --- 获取控件 ---
                actionProperty = self.propertyFrame.entries["action"]
                SmartInputFrame.showDropdown(self,actionProperty,suggestion["suggestList"])
            
    
    #SPECIFIC; INPUT nothing; OUTPUT currentState
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
                SmartInputFrame.updateDropdown(self,UserActionType.ARROW_UP)
            elif event.keysym == "Down":
                SmartInputFrame.updateDropdown(self,UserActionType.ARROW_DOWN)
        else:
            return
        return "break"
    
    #SPECIFIC; INPUT actionState; UPDATE dropdown
    def updateDropdown(self, actionState):
        selected = self.dropdown.curselection()
        index = selected[0] if selected else -1

        if actionState == UserActionType.ARROW_UP:
            new_index = max(index - 1, 0)

        elif actionState == UserActionType.ARROW_DOWN:
            size = self.dropdown.size()
            if index + 1 >= size:
                new_index = 0 
            else:
                new_index = index + 1
        else:
            return

        switchDropdown(self.dropdown, new_index)
                
        

