import tkinter as tk

from Core.dataAccess.dataManager import getData_API

class EditorFrame(tk.Frame):
    def __init__(self, master,date,**kwargs):
        super().__init__(master,**kwargs)
        
        #  ------ 获取data ------
        data = getData_API("Data/dateData.json")
        self.actionUnites = data[date]
        self.actionUnits.sort(key=lambda item: item['start'])
        
        #  ------
        
        