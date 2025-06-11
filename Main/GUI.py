import tkinter as tk

from CLI import completeActions, demonstration, promptInput
from parseInput import inputTimespan, parseDataIntoList
from validations import formatValidation, rangeValidation
from save_and_load import firstSaveData, getData, saveData
#TODO:先不用类封装控件，直接宣布为global

"""
对于CLI转到GUI,需要修改的是
- input info
- output info
另外，这并不是一个univeral function, 因此不用专门指定
由于这个是用CLI版本改的，看起来可能有点不协调
"""

def promptInputGUI(manuPrompt,manuText):
    #input the data
    manuPrompt.config(text = "enter the data")
    userData = manuText.get('1.0','end-1c')
    #停下来，输入
    manuPrompt.config(text = "enter the date")
    date = manuText.get('1.0','end-1c')
    
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
    
    #检测是否data为空，然后选择不同的输入function
    temp = getData("data.json")
    if not temp:
        firstSaveData(data)
    else:
        saveData(date,actions)

def menuGUI():
    #创建一个基本的窗口
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #创建一个frame,用于承载不同的面板
    manuFrame = tk.Frame(root,bg = 'white')
    demonFrame = tk.Frame(root,bg = 'white')
    
    #不能用pack排布，而切换到place排布，否则无法实现预定的效果
    for f in(manuFrame,demonFrame):
        f.place(relx=0,rely=0,relwidth=1,relheight=1)
        
    #主界面提升最顶端
    manuFrame.tkraise()
    
    #创建一些entry
    manuText = tk.Text(manuFrame,width = 40, height = 10)
    manuText.pack()
    
    #创建一条展示label
    menuPrompt = tk.Label(manuFrame,text = "welcome, click button to start")
    menuPrompt.pack()
    demoPrompt = tk.Label(demonFrame,text = "this is demonstration page")
    demoPrompt.pack()
    
    #添加基本的几个大功能的按钮
    inputButton = tk.Button(manuFrame,text = "input",command = lambda: promptInputGUI(menuPrompt,manuText))
    inputButton.pack()
    quitButton = tk.Button(manuFrame,text = "quit",command = lambda: root.destroy())
    quitButton.pack()
    demonMenuButton = tk.Button(manuFrame,text="enter demonstration manu",command = lambda: demonFrame.tkraise())
    demonMenuButton.pack()
    
    #这里进入下一级界面
    showButton = tk.Button(demonFrame,text = "show data",command = demonstration)
    showButton.pack()
    countActionButton = tk.Button(demonFrame,text = "count actions",command = lambda: completeActions(getData("data.json")) )
    countActionButton.pack()
    
    #事件循环开始
    root.mainloop()
