import tkinter as tk

from UI.Small_widgets.BasicButton import BasicButton

class LeftToolFrame(tk.Frame):
    def __init__(self, fatherFrame,buttons):
        super().__init__(fatherFrame) #引用父类方法，创建一个Frame
        self.config(bg = "#A9B0B3") #修改颜色
        
        #开始排版
        self.grid(
            row = 0,
            column = 0,
            rowspan = 2,
            sticky='nsew', 
            padx=2.5,
            pady=2.5
        )
        self.buttons = []
        self.columnconfigure(0,minsize = 80) #设置最小尺寸
        
        #  ------ 开始排版按钮 ------
        for label, cmd in buttons:
            btn = BasicButton(self, text=label, command=cmd)
            btn.pack(pady=3, fill='x')
            self.buttons.append(btn)