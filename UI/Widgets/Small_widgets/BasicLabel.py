import tkinter as tk

class BasicLabel(tk.Label):
    def __init__(self, master,text,**kwargs):
        super().__init__(master,text = text,**kwargs)
        text = text