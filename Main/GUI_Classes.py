import tkinter as tk

"""  ---------- CLASS ----------  """
#  ---------- PAGE CLASS ----------
class BasicPage(tk.Frame):
    def __init__(self, root,buttons,**kwargs):
        super().__init__(root) #引用父类方法，创建一个Frame
        #  ------ 使用属性收纳分Frame ------
        self.leftToolFrame = LeftToolFrame(self,buttons)
        self.downPageFrame = DownPageFrame(self)
        self.centerMainFrame = CenterMainFrame(self)
        self.bottomInfoFrame = BottomInfoFrame(self)
        
        #  ------ 初始化 ------
        basicFrameElasity(self)
        
        
#  ------ Frame class ------
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
        
        self.columnconfigure(0,minsize = 80) #设置最小尺寸
        
        #  ------ 开始排版按钮 ------
        for button in buttons: 
            button.pack()

class DownPageFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#C9B49A")
        self.grid(
            row = 2,
            column = 0,
            columnspan = 2,
            sticky='nsew',
            padx = 2.5,
            pady = 0
        )
        self.rowconfigure(2,minsize = 80)

class CenterMainFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#F4F4F4")
        self.grid(
            row = 0,
            column = 1,
            columnspan = 2,
            rowspan = 2,
            sticky='nsew', 
            padx=5, 
            pady=5
        )

class BottomInfoFrame(tk.Frame):
    def __init__(self, fatherFrame):
        super().__init__(fatherFrame)
        self.config(bg = "#F4F4F4")
        self.grid(
            row = 3,
            column = 0,
            columnspan = 2,
            sticky='nsew', 
            padx=0, 
            pady=0
        )
        self.rowconfigure(3,minsize = 40)
        
        #错误信息封装
        self.infoLabel = tk.Label(self,text = "error will show in here")
        self.infoLabel.grid(row=0, column=0, sticky="nsew")
    
    def showError(self,errorText):
        self.infoLabel.config(text = errorText)
    
        
#  ------ button class ------ 
#需要传入的参数：父容器，需要执行的命令，面板root
class BasicButton(tk.Button):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.config(        
            bg = "#F4F4F4",
            activebackground="#F4F4F4",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            width = 15,
            pady = 6,
            #text 和 command 属性没写，需要外部传入
        )

# class SwitchPageButton(tk.Button):
# 想了一下，没必要写也不太好写专门界面切换的按钮，就先拿基本的功能栏位按钮代替

#  ------ TEXT CLASS ------
class BasicText(tk.Text):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self = tk.Text(master,width = 40, height = 10)
    
    def setText(self,text):
        self.config(state = "normal")
        self.delete('1.0','end')
        self.insert('1.0',text)
        self.config(state = "disabled")

class BasicEntry(tk.Entry):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self = tk.Entry(master,width = 20)
    
    def setEntry(self,text):
        self.delete(0,'end')
        self.insert(0,text)

#  ------ LABEL CLASS ------
class BasicLabel(tk.Label):
    def __init__(self, master,text,**kwargs):
        super().__init__(master,text = text,**kwargs)
        text = text
        
        
"""  ---------- FUNCTIONS ---------- """
def basicFrameElasity(frame):
    #调整leftFrame的弹性
    frame.grid_rowconfigure(0, weight=2)
    
    #调整inputFrame的弹性
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=0)
    
    #底部栏位的弹性    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)
    
    #最底部
    frame.grid_rowconfigure(3, weight=0)