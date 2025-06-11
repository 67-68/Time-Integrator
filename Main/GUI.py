import tkinter as tk

from CLI import completeActions, demonstration, promptInput
from save_and_load import getData

"""
关于GUI,我打算大体上维持CLI的设定
把它的function复制过来但是加一点GUI的东西    
但是while true 要加在哪，退出要怎么搞
"""

def menuGUI():
    #创建一个基本的窗口
    root = tk.Tk()
    root.title("Time-integrator Menu")

    #创建一个frame,用于承载不同的面板
    manuFrame = tk.Frame(root,bg = 'white')
    manuFrame.pack()
    demonFrame = tk.Frame(root,bg = 'white')
    demonFrame.pack()
    
    #创建一条展示label
    prompt = tk.Label(manuFrame,text = "welcome, click button to start")
    prompt.pack()
    
    #添加基本的几个大功能的按钮
    inputButton = tk.Button(manuFrame,text = "input",command = promptInput)
    inputButton.pack()
    quitButton = tk.Button(manuFrame,text = "quit",command = lambda: root.destroy())
    quitButton.pack()
    demonMenuButton = tk.Button(manuFrame,text="enter demonstration manu",command = lambda: demonFrame.tkraise())
    #这里进入下一级界面
    showButton = tk.Button(demonFrame,text = "show data",command = demonstration)
    showButton.pack()
    countActionButton = tk.Button(demonFrame,text = "count actions",command = lambda: completeActions(getData("data.json")) )
    countActionButton.pack()
    
    manuFrame.tkraise()  # 默认显示主菜单
    root.mainloop()
