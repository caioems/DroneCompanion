# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:22:55 2022

@author: T2
"""
from Log_Analyzer import *
from tkinter import *

main_window = Tk()
main_window.title("The Toolbox")
dc_button = Button(main_window, text="Day Checker", command=day_check)
dc_button.grid(column=0, row=0)

main_window.mainloop()