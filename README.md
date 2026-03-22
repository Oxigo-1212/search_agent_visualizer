# 8-Puzzle Solver

This repository contains a small 8-puzzle solver library and a desktop GUI built with Tkinter.

Features:
- Puzzle state and problem abstractions
- Breadth-first search (BFS) solver
- Desktop GUI to edit initial/goal states, shuffle, and animate the solution

Quickstart
1. Install dependencies: python -m pip install -e .
2. Run the GUI: python -m src.puzzle.gui

Ubuntu (uv) - install & build tutorial (concise)

This minimal tutorial covers Ubuntu using the "uv" Python manager to simplify
environment management. uv creates and manages virtual environments and Python
versions for you; it can be used instead of manually creating venvs.

1) Install uv (one-line installer)

   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"  # or restart your shell

2) Create a virtual environment and install PyInstaller

   # create a venv using uv (example requests Python 3.12)
   uv venv --python 3.12
   # install PyInstaller and the package into the uv-managed venv
   uv pip install --upgrade pip
   uv pip install -e .

3) Build the single-file executable with PyInstaller

   uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py

   The produced binary will be at: ./dist/8-puzzle_solver


Using uv on a clean machine (Ubuntu / Arch)

Ubuntu (minimal steps)

  # install uv (one-line installer)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"  # or restart your shell

  # create a uv-managed venv, install dependencies, and build
  uv venv --python 3.14
  uv pip install --upgrade pip
  uv pip install -e .
  uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py

Arch Linux (minimal steps)

  # install uv (AUR) or use the installer above; example with yay:
  yay -S --noconfirm uv
  export PATH="$HOME/.local/bin:$PATH"  # ensure uv is on PATH

  # create a uv-managed venv, install dependencies, and build
  uv venv --python 3.14
  uv pip install --upgrade pip
  uv pip install -e .
  uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py

Notes

- If your Python version does not meet pyproject.toml's requires-python constraint
  (>=3.14), install a compatible Python or relax the constraint locally for
  testing. For a local build, installing PyInstaller and the package in a
  supported Python environment is usually sufficient.
- If PyInstaller misses modules, ensure the package is installed in the venv
  (pip install -e .) and use --paths src so PyInstaller finds source modules.

Windows (uv-based, untested)

This short, untested guide shows how to produce a Windows executable (.exe)
using the uv manager. On Windows it's easiest to install uv via pipx and then
use uv to create and manage a virtual environment.

PowerShell (recommended):

  # install pipx (if not installed)
  python -m pip install --user pipx
  python -m pipx ensurepath
  # restart your shell or open a new PowerShell window now

  # install uv via pipx
  pipx install uv

  # create a uv-managed venv and install deps
  uv venv --python 3.14
  uv pip install --upgrade pip
  uv pip install -e .

  # build (outputs .exe in dist\)
  uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src\main.py

Command Prompt (cmd.exe):

  python -m pip install --user pipx
  python -m pipx ensurepath
  # restart cmd/PowerShell so pipx is on PATH
  pipx install uv
  uv venv --python 3.14
  uv pip install --upgrade pip
  uv pip install -e .
  uv run pyinstaller --onefile --name 8-puzzle_solver --paths src\main.py

The produced artifact will be at: .\dist\8-puzzle_solver.exe

Notes for Windows builds:
- If your project or dependencies include C extensions, you may need the
  Microsoft Visual C++ Build Tools installed (Visual Studio Build Tools).
- This Windows guide is untested in this repository; please report back any
  failures and I can help iterate on the steps.
