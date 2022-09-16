import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os", "pathlib", "pandas", "simplekml", "statistics", "tkinter", "tqdm"],
                     "optimize": 1}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="DayChecker",
    version="0.1",
    description="A tool to analyze BIN dataflash logs, reporting out daily coverage and drone health informations.",
    options={"build_exe": build_exe_options},
    executables=[Executable("Log_Analyzer.py", base=base)],
)