import tkinter as tk

from Core.dataAccess.dataManager import getData_API
from UI.Widgets.Small_widgets.BasicButton import BasicButton
from UI.Widgets.Small_widgets.BasicEntry import BasicEntry
from UI.Widgets.Small_widgets.BasicLabel import BasicLabel


#CLASS dateSelectionFrame; INPUT date-centric data and judge is user input reasonable
class DateSelectionFrame(tk.Frame):
    def __init__(self,_on_PageSwitch_CallBack,master,**kwargs):
        super().__init__(master,**kwargs)
        
        #  ------ 获取数据 ------
        self.data = getData_API("Data/dateData.json")
        
        #  ------ 创建一个提示 ------
        self.text = BasicLabel(self,"enter the date you want to enter in the entry")
        self.text.grid(row = 0,column =0)
        
        #  ------ 创建一个Entry ------
        self.dateEntry = BasicEntry(self)
        self.dateEntry.grid(row = 1, column=0)
        
        #  ------ 创建按钮 ------
        self.dateButton = BasicButton(self,lambda:self.processUserDate(self.data))
        self.dateButton.grid(row = 1, column=1)
        
        #  ------ 初始化函数 ------
        self._on_PageSwitch_CallBack = _on_PageSwitch_CallBack
        
        
    #SPECIFIC; INPUT data; DETECT whether the date is right
    def processUserDate(self,data):
        userEntry = self.dateEntry.get()
        if userEntry != "":
            #  ------ 开始判断 ------
            for date in data:
                if date == userEntry:
                    #  --- 打包数据 ---
                    userDate = self.dateEntry.get()
                    
                    #  --- 调用函数 ---
                    self._on_PageSwitch_CallBack(userDate)
                    
                    break
                
        else:
            return