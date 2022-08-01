# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:22:55 2022

@author: [t2]caiera
"""

from tkinter import *
from tkinter import ttk

def log_command():
    import Log_Analyzer
    
def bot_command():
    import gtbot

class ToolBox:
    def __init__(self, main_window):
        main_window.title("The Toolbox")
        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(0, weight=1)
        
        mainframe = ttk.Frame(main_window)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe['padding'] = 5
        
        dc_button = ttk.Button(mainframe, text="Day Checker", command=log_command).grid(column=0, row=0)
        gt_button = ttk.Button(mainframe, text="Geotag Bot", command=bot_command).grid(column=1, row=0)
        
main_window = Tk()
ToolBox(main_window)
main_window.mainloop()

    
    
    
    
    