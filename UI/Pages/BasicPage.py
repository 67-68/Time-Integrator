from UI.Frames import BottomInfoFrame, CenterMainFrame, DownPageFrame, LeftToolFrame
import tkinter as tk

class BasicPage(tk.Frame):
    def __init__(self, root,buttons,**kwargs):
        super().__init__(root) #引用父类方法，创建一个Frame
        #  ------ 使用属性收纳分Frame ------
        self.leftToolFrame = LeftToolFrame(self,buttons)
        self.downPageFrame = DownPageFrame(self)
        self.centerMainFrame = CenterMainFrame(self)
        self.bottomInfoFrame = BottomInfoFrame(self)
        
        #  ------ 初始化 ------
        self.basicFrameElasity(self)
    
        
    def basicFrameElasity(self):
        #调整leftFrame的弹性
        self.grid_rowconfigure(0, weight=2)
        
        #调整inputFrame的弹性
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        #底部栏位的弹性    
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        #最底部
        self.grid_rowconfigure(3, weight=0)