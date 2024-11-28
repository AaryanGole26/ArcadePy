import sys
from cx_Freeze import setup, Executable

import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tk', 'tk 8.6')

build_exe_options = {"packages": ["pygame"], 'include_files': ["Ball.png","Paddle.png","Paddle2.png","Pong.jpg","bounce.wav","score.ogg","pong.ogg","tcl86t.dll","tk86t.dll"]}

base = None
if sys.platform == "Win32":
    base = "Win32GUI"

setup(
    name="Pong",   
    options={"build_exe": build_exe_options},
    executables = [Executable("Pong.py", base=base)])