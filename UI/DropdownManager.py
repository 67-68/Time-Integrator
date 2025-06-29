import tkinter as tk
from Core.Definitions import UserActionType

#MANAGE a dropdown and a toplevel(like frame) to accomodate it
class DropdownManager:
    def __init__(self, master):
        self.master = master
        #  ------ 创建TopLevel ------
        self.topLevel = tk.Toplevel(self.master)
        self.topLevel.withdraw()  # 初始时隐藏
        self.topLevel.overrideredirect(True)  # 无边框
        self.topLevel.attributes("-topmost", True)  # 置顶
        
        #  ------ 创建Dropdown ------
        self.dropdown = tk.Listbox(self.topLevel)
        self.dropdown.pack()
        
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
        self.topLevel.geometry(f"{width}x100+{x}+{y}")  # 100 是高度，可调
        self.topLevel.deiconify()
        
    #UNIVERSAL; INPUT tk dropdown and int index; UPDATE dropdown
    def switchDropdown(self,index):
            self.dropdown.selection_clear(0, tk.END)  # 清除所有选中
            self.dropdown.selection_set(index)        # 设置选中 index
            self.dropdown.activate(index)             # 设置焦点
            self.dropdown.see(index)                  # 滚动到该项
            
    
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

        self.switchDropdown(new_index)
    
    def hideTopLevel(self):
        self.topLevel.withdraw()
    
    def ifDropdownCanBeSeen(self):
        return self.dropdown.winfo_ismapped()
    
    def getDropdownList(self):
        return self.dropdown.curselection()
    
    def getDropdownVal(self,index):
        return self.dropdown.get(index)