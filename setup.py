import cx_Freeze
import sys
import os


os.environ['TCL_LIBRARY'] = "C:/Users/lovely/AppData/Local/Programs/Python/Python35-32/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/lovely/AppData/Local/Programs/Python/Python35-32/tcl/tk8.6"

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("txt-to-json.py", base=base, icon="favicon.ico")]

cx_Freeze.setup(
    name="txt-to-json",
    options = {"build_exe": {"packages":["tkinter", "re", "parser", "os", "sys", "codecs", "json", "urllib.request"], "include_files":["favicon.ico"]}},
    version = "0.1",
    description = 'text to json tool',
    executables = executables
    )

    
      
