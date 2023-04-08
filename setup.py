import sys
from cx_Freeze import setup, Executable

packages = []

build_exe_options = {"packages": packages, "excludes": []}

base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(script="lab.py", base=base)

setup(
    name="Lab2",
    version="1.0",
    description="Laboratory work No.2 from system analysis",
    options={"build_exe": build_exe_options},
    executables=[exe],
)