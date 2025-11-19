READ ME FIRST

Welcome to CRT Buddy! If you previously saw garbled characters, the docs have been cleaned to UTF-8.
- README.md: overview, install, run
- USAGE.md: usage and workflows
- QUICKSTART.txt: quick steps

How to run (any of these):
- python start.py    # runs a dependency self-check
- python CRT_Buddy.py
- run/double-click run_app.bat  # one-click on Windows

If you see ModuleNotFoundError:
- Ensure VS Code uses the workspace .venv interpreter and install deps:
  pip install PyQt6 Pillow numpy opencv-python pygame pywin32 requests

To package:
- pip install pyinstaller
- python build_exe.py  # builds dist/CRT_Buddy.exe

For more help, see README.md → Troubleshooting, or open an Issue.
