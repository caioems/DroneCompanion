# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:22:55 2022

@author: T2
"""

import tkinter as ttk

def log_command():
    import Log_Analyzer
    
def bot_command():
    import gtbot

if __name__ == "__main__":
    main_window = ttk.Tk()
    main_window.title("The Toolbox")
    dc_button = ttk.Button(main_window, text="Day Checker", command=log_command)
    dc_button.grid(column=0, row=0)
    gt_button = ttk.Button(main_window, text="Geotag Bot", command=bot_command)
    gt_button.grid(column=1, row=0)
    
    main_window.mainloop()