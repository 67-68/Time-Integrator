import tkinter as tk

from CLI import completeActions, demonstration, promptInput
from parseInput import inputTimespan, parseDataIntoList
from validations import formatValidation, rangeValidation
from save_and_load import getData, saveData
#TODO:先不用类封装控件，直接宣布为global

"""
对于CLI转到GUI,需要修改的是
- input info
- output info
另外，这并不是一个univeral function, 因此不用专门指定
由于这个是用CLI版本改的，看起来可能有点不协调
"""

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
    data = getData("data.json")
    data[date] = actions
    saveData(data,"data.json")

def menuGUI():
    #创建一个最基本的窗口
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #设置大小
    root.geometry("800x600")
    
    #主界面创建
    menuFrame = tk.Frame(root,bg = 'white')
    demonFrame = tk.Frame(root,bg = 'white')
    
    #主界面切换
    for f in(menuFrame,demonFrame):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
    
    #  ------ 调整各栏位的弹性 ------
    menuFrameElasity(menuFrame)
    
    #  ------ 创建menuFrame中的分frame ------
    down_MenuFrame = downMenuFrameCreation(menuFrame) #底部灰色栏
    left_MenuFrame = leftMenuFrameCreation(menuFrame) #左侧工具栏
    input_MenuFrame = inputMenuFrameCreation(menuFrame) #输入栏
    
    #TODO：这里我需要单独去创建一个输入的界面，然后把主界面作为菜单吗？还是直接在主界面提示东西
        
    #主界面提升最顶端
    menuFrame.tkraise()
    
    #创建entry & text
    menuText = inputFrame_MenuText(input_MenuFrame)
    dateEntry = inputFrame_DateEntry
    
    #创建一条展示label
    menuPrompt = tk.Label(input_MenuFrame,text = "welcome, click button to start")
    menuPrompt.pack() 
    demoPrompt = tk.Label(input_MenuFrame,text = "this is demonstration page")
    demoPrompt.pack() 
    
    #添加基本的几个大功能的按钮
    inputButton = tk.Button(
        left_MenuFrame,
        text = "input",
        bg= "#F4F4F4",
        activebackground="#F4F4F4",
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        width = 15,
        pady = 6,
        command = lambda: promptInputGUI(menuPrompt,menuText,dateEntry))
    inputButton.pack()
    
    quitButton = tk.Button(
        left_MenuFrame,
        text = "quit",
        bg = "#F4F4F4",
        activebackground="#F4F4F4",
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        width = 15,
        pady = 6,
        command = lambda: root.destroy())
    quitButton.pack()
    
    #切换界面的button
    demonMenuButton = tk.Button(
        down_MenuFrame,
        text="enter demonstration manu",
        bg="#C9B49A",
        activebackground="#C9B49A",
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        height = 5,
        command = lambda: demonFrame.tkraise())
    demonMenuButton.pack()
    
    #这里进入下一级界面
    showButton = tk.Button(demonFrame,text = "show data",command = demonstration)
    showButton.pack()
    countActionButton = tk.Button(demonFrame,text = "count actions",command = lambda: completeActions(getData("data.json")) )
    countActionButton.pack()
    
    #事件循环开始
    root.mainloop()


def menuFrameElasity(menuFrame):
    #调整leftFrame的弹性
    menuFrame.grid_rowconfigure(0, weight=2)
    
    #调整inputFrame的弹性
    menuFrame.grid_rowconfigure(1, weight=1)
    menuFrame.grid_rowconfigure(2, weight=0)
    
    #底部栏位的弹性    
    menuFrame.grid_columnconfigure(0, weight=1)
    menuFrame.grid_columnconfigure(1, weight=3)

def downMenuFrameCreation(menuFrame):
    #创建
    down_MenuFrame = tk.Frame(menuFrame,bg = "#C9B49A")
    down_MenuFrame.grid(
        row = 2,
        column = 0,
        columnspan = 2,
        sticky='nsew',
        padx = 2.5,
        pady = 0)
    
    #调整最小高度
    menuFrame.rowconfigure(2,minsize = 80)
    
    return down_MenuFrame

def leftMenuFrameCreation(menuFrame):
    left_MenuFrame = tk.Frame(menuFrame,bg = "#A9B0B3")
    left_MenuFrame.grid(
        row = 0,
        column = 0,
        rowspan = 2,
        sticky='nsew', 
        padx=2.5,
        pady=2.5)
    
    #修改最小size
    menuFrame.columnconfigure(0,minsize = 80)
    
    return left_MenuFrame

def inputMenuFrameCreation(menuFrame):
    input_MenuFrame = tk.Frame(menuFrame,bg = "#F4F4F4")
    input_MenuFrame.grid(
        row = 0,
        column = 1,
        columnspan = 2,
        rowspan = 2,
        sticky='nsew', 
        padx=5, 
        pady=5)
    
    return input_MenuFrame

def inputFrame_MenuText(input_MenuFrame):
    menuText = tk.Text(input_MenuFrame,width = 40, height = 10)
    menuText.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    return menuText
    
def inputFrame_DateEntry(input_MenuFrame):
    dateEntry = tk.Entry(input_MenuFrame,width = 20)
    dateEntry.pack(side="top", fill="x", expand=True, padx=0, pady=(12, 0))
    return dateEntry



        