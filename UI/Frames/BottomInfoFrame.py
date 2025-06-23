import tkinter as tk

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