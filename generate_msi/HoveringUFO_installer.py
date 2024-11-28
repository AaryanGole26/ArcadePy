import sys
from cx_Freeze import setup, Executable

import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tk', 'tk 8.6')

build_exe_options = {"packages": ["pygame"], 'include_files': ['gallery/','tcl86t.dll','tk86t.dll']}
base = None
if sys.platform == "Win32":
    base = "Win32GUI"

setup(
    name="Hovering UFO",
    options={"build_exe": build_exe_options},
    executables = [Executable("Hovering UFO.py", base=base)])