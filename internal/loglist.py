import pathlib
from tkinter import Tk
from tkinter.filedialog import askdirectory

import internal.config as cfg

class LogList:
    def __init__(self):
      self.root_folder = self.get_root_folder()
      self.bin_list = self.create_bin_list(self.root_folder)
      self.gnss_list = self.create_gnss_list(self.root_folder)
      
    def get_root_folder(self):
      root = Tk()
      root.withdraw()
      path = askdirectory(title='Select the root folder:')
      root.destroy()
      return path
    
    def create_bin_list(self, root_folder):
        pattern = "**/*.BIN"
        return list(pathlib.Path(root_folder).rglob(pattern))
      
    def create_gnss_list(self, root_folder):
      pattern = f"**/{cfg.RAW_GNSS_LOG_NAME}.TXT"
      return list(pathlib.Path(root_folder).rglob(pattern))
    
    