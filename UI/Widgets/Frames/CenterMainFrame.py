import tkinter as tk

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