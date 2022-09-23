# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:22:55 2022

@author: [t2]caiera
"""
from log_analyzer import *
from tkinter import *
from tkinter import ttk
import sys
import subprocess
import threading 

#Functions
def bot_command():
    import gtbot
    
def run():
    threading.Thread(target=test).start()

def test():
    print("Thread: start")

    p = subprocess.Popen("ping -c 4 stackoverflow.com".split(), stdout=subprocess.PIPE, bufsize=1, text=True)
    while p.poll() is None:
        msg = p.stdout.readline().strip() # read a line from the process output
        if msg:
            print(msg)

    print("Thread: end")

#Classes
class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see("end")  # autoscroll

class ToolBox:
    def __init__(self, main_window):
        main_window.title("c3Toolbox")
        main_window.columnconfigure(0, weight=1)
        main_window.rowconfigure(0, weight=1)
        
        mainframe = ttk.Frame(main_window)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe['padding'] = 5        
        
        dc_button = ttk.Button(mainframe, text="Day Checker", command=day_checker).grid(column=0, row=0)
        gt_button = ttk.Button(mainframe, text="Geotag Bot", command=bot_command).grid(column=1, row=0)

        text = Text(main_window)
#Running ToolBox...        
main_window = Tk()
tb = ToolBox(main_window)

#https://stackoverflow.com/questions/62335989/redirect-terminal-output-to-tkinter
#old_stdout = sys.stdout    
#sys.stdout = Redirect(tb.text)

main_window.mainloop()

#sys.stdout = old_stdout

    
    
    
    
    