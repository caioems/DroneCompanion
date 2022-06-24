#!/usr/bin/env python
# coding: utf-8

# In[41]:


#GeoTag Bot 
#Import required libraries and set delays

import pyautogui as py
import time
import clipboard
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import pyperclip

t = 45 #t = intervalo para geotag, colocar em 45 para roll out!!!
ti = 3 #ti = intervalo para image locator


# In[42]:


#Directory selection and folder count

root = tk.Tk()
root.withdraw()
folder_name = askdirectory()
pyperclip.copy(folder_name)
list = os.listdir(folder_name)
MissionQuantity = int(len(list))
a = MissionQuantity - 1


# In[43]:


#MISSION PLANNER START UP

py.press('winleft') 
time.sleep(0.5)
py.typewrite('mission')
time.sleep(0.5)
py.press('enter')
time.sleep(15)


# In[44]:


#UPDATE NOW WINDOW KILLER

updatenow = py.locateCenterOnScreen('updatenow.PNG')
if(updatenow != None):
    py.click(updatenow)
    time.sleep(1)


# In[45]:


#BEGINNING GEO TAG

py.hotkey('ctrl','f')
time.sleep(ti)
georeference = py.locateCenterOnScreen('geo ref.PNG')
py.click(georeference)
time.sleep(ti)
browselog = py.locateCenterOnScreen('browselog.PNG')
py.click(browselog)


# In[46]:


#FIND FIRST FOLDER

py.hotkey('shift','tab')
time.sleep(0.5)
py.hotkey('shift','tab')
time.sleep(0.5)
py.hotkey('alt','e')
time.sleep(0.5)
py.hotkey('alt','d')
time.sleep(1)
py.hotkey('ctrl','v')
time.sleep(1)
py.press('enter')
time.sleep(1)
py.press('tab')
time.sleep(4)
py.press('tab')
time.sleep(1)
py.press('tab')
time.sleep(1)
py.press('tab')
time.sleep(0.5)
py.hotkey('ctrl','shift','6')
time.sleep(0.5)
py.press('down')
time.sleep(0.5)
py.press('up')
time.sleep(0.5)
py.press('enter')
time.sleep(1)


# In[47]:


#FIRST MERGE TEST AND EXECUTION

py.hotkey('ctrl','shift','6')
time.sleep(1)
py.press('down')
time.sleep(0.5)
py.press('f2')
time.sleep(0.5)
py.hotkey('ctrl','a')
time.sleep(0.5)
py.hotkey('ctrl','c')
time.sleep(0.5)
py.press('esc')
text = clipboard.paste()
if '.BIN' in text:
    py.press('enter')
    time.sleep(5)
    preprocess = py.locateCenterOnScreen('preprocess.PNG')
    py.click(preprocess)
    time.sleep(t)
else:
    py.press('up')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(5)
    preprocess = py.locateCenterOnScreen('preprocess.PNG')
    py.click(preprocess)
    time.sleep(t)
    browselog = py.locateCenterOnScreen('browselog.PNG')
    py.click(browselog)
    time.sleep(0.5)
    py.hotkey('shift','tab')
    time.sleep(0.5)
    py.press('backspace')
    time.sleep(0.5)
    py.hotkey('ctrl','shift','6')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(ti)
    preprocess = py.locateCenterOnScreen('preprocess.PNG')
    py.click(preprocess)
    time.sleep(t)    


# In[48]:


#3 FLIGHT MERGE TEST AND TRASITION TO LOOP FOLDER

browselog = py.locateCenterOnScreen('browselog.PNG')
py.click(browselog)
time.sleep(0.5)
py.hotkey('shift','tab')
time.sleep(0.5)
py.press('backspace')
time.sleep(0.5)
py.hotkey('ctrl','shift','6')
time.sleep(0.5)
py.press('down')
time.sleep(0.5)
py.press('f2')
time.sleep(0.5)
py.hotkey('ctrl','c')
time.sleep(0.5)
py.press('esc')
time.sleep(0.5)
text = clipboard.paste()
if text == '3':
    py.press('enter')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(ti)
    preprocess = py.locateCenterOnScreen('preprocess.PNG')
    py.click(preprocess)
    time.sleep(t)
    browselog = py.locateCenterOnScreen('browselog.PNG')
    py.click(browselog)
    time.sleep(0.5)
    py.hotkey('shift','tab')
    time.sleep(0.5)
    py.press('backspace')
    time.sleep(0.5)
    py.press('backspace')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(0.5)
elif text == '2':
    py.press('backspace')
    time.sleep(0.5)
    py.press('down')
    time.sleep(0.5)
    py.press('enter')
    time.sleep(0.5)
else:
    py.press('enter')
    time.sleep(0.5)


# In[49]:


#LOOP 

count = 0
while count < a:
    time.sleep(0.5)
    py.hotkey('ctrl','shift','6')
    time.sleep(1)
    py.press('down')
    time.sleep(0.5)
    py.press('f2')
    time.sleep(0.5)
    py.hotkey('ctrl','a')
    time.sleep(0.5)
    py.hotkey('ctrl','c')
    time.sleep(0.5)
    py.press('esc')
    text = clipboard.paste()
    if '.BIN' in text:
        py.press('enter')
        time.sleep(ti)
        preprocess = py.locateCenterOnScreen('preprocess.PNG')
        py.click(preprocess)
        time.sleep(t)
        browselog = py.locateCenterOnScreen('browselog.PNG')
        py.click(browselog)
        time.sleep(0.5)
        py.hotkey('shift','tab')
        time.sleep(0.5)
        py.press('backspace')
        time.sleep(0.5)
        py.press('down')
        time.sleep(0.5)
        py.press('enter')
        time.sleep(0.5)
    else:
        py.press('up')
        time.sleep(0.5)
        py.press('enter')
        time.sleep(0.5)
        py.press('down')
        time.sleep(0.5)
        py.press('enter')
        time.sleep(ti)
        preprocess = py.locateCenterOnScreen('preprocess.PNG')
        py.click(preprocess)
        time.sleep(t)
        browselog = py.locateCenterOnScreen('browselog.PNG')
        py.click(browselog)
        time.sleep(0.5)
        py.hotkey('shift','tab')
        time.sleep(0.5)
        py.press('backspace')
        time.sleep(0.5)
        py.hotkey('ctrl','shift','6')
        time.sleep(0.5)
        py.press('down')
        time.sleep(0.5)
        py.press('enter')
        time.sleep(0.5)
        py.press('down')
        time.sleep(0.5)
        py.press('enter')
        time.sleep(ti)
        preprocess = py.locateCenterOnScreen('preprocess.PNG')
        py.click(preprocess)
        time.sleep(t)
        browselog = py.locateCenterOnScreen('browselog.PNG')
        py.click(browselog)
        time.sleep(0.5)
        py.hotkey('shift','tab')
        time.sleep(0.5)
        py.press('backspace')
        time.sleep(0.5)
        py.hotkey('ctrl','shift','6')
        time.sleep(0.5)
        py.press('down')
        time.sleep(0.5)
        py.press('f2')
        time.sleep(0.5)
        py.hotkey('ctrl','c')
        time.sleep(0.5)
        py.press('esc')
        time.sleep(0.5)
        text = clipboard.paste()
        if text == '3':
            py.press('enter')
            time.sleep(0.5)
            py.press('down')
            time.sleep(0.5)
            py.press('enter')
            time.sleep(ti)
            preprocess = py.locateCenterOnScreen('preprocess.PNG')
            py.click(preprocess)
            time.sleep(t)
            browselog = py.locateCenterOnScreen('browselog.PNG')
            py.click(browselog)
            time.sleep(0.5)
            py.hotkey('shift','tab')
            time.sleep(0.5)
            py.press('backspace')
            time.sleep(0.5)
            py.press('backspace')
            time.sleep(0.5)
            py.press('down')
            time.sleep(0.5)
            py.press('enter')
            time.sleep(0.5)
        elif text == '2':
            py.press('backspace')
            time.sleep(0.5)
            py.press('down')
            time.sleep(0.5)
            py.press('enter')
            time.sleep(0.5)
        else:
            py.press('enter')
            time.sleep(0.5)
    count += 1


# In[50]:


# FINALIZE PROCESS

py.hotkey('alt','f4')
time.sleep(1)
py.hotkey('alt','f4')
time.sleep(1)
py.hotkey('alt','f4')
time.sleep(1)
py.hotkey('alt','f4')
time.sleep(1)
print('Geo Tag completed!')

