import tkinter as tk

class BasicFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.config(bg = "#F4F4F4")