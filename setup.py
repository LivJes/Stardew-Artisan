
import sys
from cx_Freeze import setup, Executable
import os
import time
import tk_ToolTip

os.environ['TCL_LIBRARY'] = "lib"
os.environ['TK_LIBRARY'] = "lib"

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    executables = [Executable('stardew_artisan.py', base=base)]

build_exe_options = {"include_files": ["Images", "crop_data.txt", "stardew_artisan_log.txt", "keg.ico", "tk_ToolTip.py"],
                    "packages": ["tkinter", "time", "tk_ToolTip"]}



setup(name='Stardew Artisan',
      version='1.0',
      description='Artisan Goods price comparison program',
      executables= [Executable('stardew_artisan.py', base=base)])