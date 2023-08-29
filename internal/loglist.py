import pathlib
from tkinter import Tk
from tkinter.filedialog import askdirectory

class LogList:
    def __init__(self):
      self.root_folder = self.get_root_folder()
      self.log_list = self.create_log_list(self.root_folder)
      
    def get_root_folder(self):
      root = Tk()
      root.withdraw()
      path = askdirectory(title='Select the root folder:')
      root.destroy()
      return path
    
    def create_log_list(self, root_folder):
        return list(pathlib.Path(root_folder).glob(r"**\*.BIN"))
    
    