import tkinter as tk

class BasicText(tk.Text):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self = tk.Text(master,width = 40, height = 10)
    
    def setText(self,text):
        self.config(state = "normal")
        self.delete('1.0','end')
        self.insert('1.0',text)
        self.config(state = "disabled")