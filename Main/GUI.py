import tkinter as tk

from CLI import completeActions, demonstration
from APIs.parseInput import inputTimespan, parseDataIntoList
from APIs.validations import formatValidation, rangeValidation
from APIs.json_Interaction import getDataAPI, saveDataAPI

"""  ---------- Classes ----------  """
#  ------ Frame class ------
class LeftToolFrame(tk.Frame):
    def __init__(self, fatherFrame):
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

        
#  ------ button class ------ 
#需要传入的参数：父容器，需要执行的命令，面板root
class LeftToolButton(tk.Button):
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

        
        
def promptInputGUI(manuPrompt,manuText,dateEntry):
    #input the data
    manuPrompt.config(text = "enter the data and date respectively, in the top and bottom")
    userData = manuText.get('1.0','end-1c')
    date = dateEntry.get()
    
    #TODO:presence check
    
    #TODO:use strip to delete spaces
    
    #TODO:change it into discard redundant space in data
    
    #change the format of the data, in order to save into json
    userData = userData.split(" - ")
    
    #put data into the list
    actions = parseDataIntoList(userData)
    
    #Format check and change the format
    for i in range (len(actions)):
        actions[i]["end"] = formatValidation(actions[i]["start"],actions[i]["end"])
    
    #validate whether they are reasonable
    if rangeValidation(actions) == True:
        manuPrompt.config(text = "pass range validation correctly")
    
    #输入timespan
    inputTimespan(actions)
    
    #把actions包裹进一个新的dictionary
    data = {date : actions}
    
    #输入data
    data = getDataAPI("data.json")
    data[date] = actions
    saveDataAPI(data,"data.json")

def menuGUI():
    #  ---------- 窗口和页面 ----------
    #  ------ 创建root和frame ------
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #主界面创建
    menuFrame = tk.Frame(root,bg = 'white')
    demonFrame = tk.Frame(root,bg = 'white')
    
    #  ------ 初始化窗口和界面 ------
    #设置大小
    root.geometry("800x600")
    
    #主界面提升最顶端
    menuFrame.tkraise()
    
    #主界面切换
    for f in(menuFrame,demonFrame):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    #调整弹性
    basicFrameElasity(menuFrame)
    basicFrameElasity(demonFrame)
    
    #  ---------- 页面内分栏 ----------
    #MenuFrame
    down_MenuFrame = DownPageFrame(menuFrame) #底部灰色栏
    left_MenuFrame = LeftToolFrame(menuFrame) #创建左边工具栏
    main_MenuFrame = CenterMainFrame(menuFrame) #输入栏
    
    #DemonFrame
    down_DemoFrame = DownPageFrame(demonFrame)
    left_DemoFrame = LeftToolFrame(demonFrame)
    main_DemoFrame = CenterMainFrame(demonFrame)
    
    #TODO：这里我需要单独去创建一个输入的界面，然后把主界面作为菜单吗？还是直接在主界面提示东西

    #  ---------- 文本框和文本 ----------
    #  ------ 文本框 ------
    menuText = inputFrame_MenuText(main_MenuFrame)
    dateEntry = inputFrame_DateEntry(main_MenuFrame)
    
    # ------ 展示文本 ------
    menuPrompt = tk.Label(main_MenuFrame,text = "welcome, click button to start")
    menuPrompt.pack() 
    demoPrompt = tk.Label(main_MenuFrame,text = "this is demonstration page")
    demoPrompt.pack() 
    
    #  ---------- 按钮 ----------
    #  ------ 主界面 ------
    #功能性按钮
    inputButton = LeftToolButton(left_MenuFrame, text = "input", command = lambda: promptInputGUI(menuPrompt,menuText,dateEntry))
    inputButton.pack()
    
    quitButton = LeftToolButton(left_MenuFrame, text = "quit", command = lambda: root.destroy())
    quitButton.pack()

    #切换界面
    for i in (down_DemoFrame,down_MenuFrame):
        demonMenuButton = LeftToolButton(i,text="enter demonstration menu", height = 5, command = lambda: demonFrame.tkraise())
        demonMenuButton.pack()
        menuSwitchButton = LeftToolButton(i,text="enter main menu", height = 5, command = lambda: menuFrame.tkraise())
        menuSwitchButton.pack()
    
    #  ------ 展示界面 ------ 
    showButton = LeftToolButton(left_DemoFrame,text = "show data",command = demonstration)
    showButton.pack()
    countActionButton = LeftToolButton(left_DemoFrame,text = "count actions",command = lambda: completeActions(getDataAPI("data.json")) )
    countActionButton.pack()
    
    #  ---------- 事件循环开始 ----------
    root.mainloop()

""" ---------- 各种工厂函数 ---------- """
# 后面可能会改造成类
def basicFrameElasity(frame):
    #调整leftFrame的弹性
    frame.grid_rowconfigure(0, weight=2)
    
    #调整inputFrame的弹性
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=0)
    
    #底部栏位的弹性    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)


def inputFrame_MenuText(input_MenuFrame):
    menuText = tk.Text(input_MenuFrame,width = 40, height = 10)
    menuText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    return menuText
    
def inputFrame_DateEntry(input_MenuFrame):
    dateEntry = tk.Entry(input_MenuFrame,width = 20)
    dateEntry.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    return dateEntry



        