# 8-Puzzle Solver

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A modern 8-puzzle solver with a clean desktop GUI. Built with Python and Tkinter, featuring BFS search and interactive puzzle visualization.

## ✨ Features

- **Core Solver**: Breadth-first search (BFS) algorithm for optimal solutions
- **Desktop GUI**: Interactive Tkinter interface for puzzle manipulation
- **Visual Tools**: Edit initial/goal states, shuffle puzzles, and animate solutions
- **Cross-Platform**: Build native executables for Linux, macOS, and Windows

## 🚀 Quick Start

### Development Mode

```bash
# Install dependencies
python -m pip install -e .

# Run the GUI
python -m src.puzzle.gui
# Alternatively, run directly (for development)
python src/puzzle/gui.py
```

## 🏗️ Building Executables

We use [uv](https://github.com/astral-sh/uv) for fast, reliable Python environment management and [PyInstaller](https://pyinstaller.org/) for creating standalone executables.

### Ubuntu / Debian

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create environment and build
uv venv --python 3.14
uv pip install --upgrade pip
uv pip install -e .
uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py
```

**Output**: `./dist/8-puzzle_solver`

### Arch Linux

```bash
# Install uv (AUR)
yay -S --noconfirm uv
export PATH="$HOME/.local/bin:$PATH"

# Create environment and build
uv venv --python 3.14
uv pip install --upgrade pip
uv pip install -e .
uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py
```

**Output**: `./dist/8-puzzle_solver`

### Windows (PowerShell)

```powershell
# Install pipx and uv
python -m pip install --user pipx
python -m pipx ensurepath
# Restart shell
pipx install uv

# Create environment and build
uv venv --python 3.14
uv pip install --upgrade pip
uv pip install -e .
uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src\main.py
```

**Output**: `.\dist\8-puzzle_solver.exe`

### Windows (Command Prompt)

```cmd
python -m pip install --user pipx
python -m pipx ensurepath
REM Restart shell
pipx install uv
uv venv --python 3.14
uv pip install --upgrade pip
uv pip install -e .
uv run pyinstaller --onefile --name 8-puzzle_solver --paths src\main.py
```

**Output**: `.\dist\8-puzzle_solver.exe`

## 📋 Requirements

- **Python**: 3.14 or higher
- **System Dependencies**:
  - Ubuntu/Debian: `python3`, `python3-venv`, `python3-pip`
  - Arch Linux: `python`, `python-virtualenv`, `base-devel`
  - Windows: Python 3.14+ from [python.org](https://www.python.org/downloads/)
- **Build Tools** (for C extensions):
  - Linux: `build-essential` / `base-devel`
  - Windows: [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

## 🔧 Troubleshooting

### Python Version Issues

If `pip` refuses to install due to the `requires-python` constraint (>=3.14):

- Install a compatible Python version, or
- Edit `pyproject.toml` to relax the constraint for local testing

### PyInstaller Missing Modules

If PyInstaller fails to find modules:

```bash
# Ensure package is installed in the venv
uv pip install -e .

# Use --paths to include source directory
uv run pyinstaller --onefile --name 8-puzzle_solver --paths src src/main.py
```

### Windows Build Issues

- Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) for C extension support
- Run PowerShell as Administrator if needed
- The Windows build guide is untested—please report issues

## 📦 Project Structure

```
8-puzzle_solver/
├── src/
│   ├── puzzle/
│   │   ├── gui.py          # Desktop GUI
│   │   ├── state.py        # Puzzle state representation
│   │   ├── problem.py      # Problem definition
│   │   ├── utils.py        # Utility functions (e.g., solvability check)
│   │   └── search_agents/  # Search algorithms
│   │       ├── algorithm.py
│   │       ├── node.py
│   │       └── __init__.py
│   ├── main.py             # Entry point
│   └── __init__.py
├── tests/
│   └── ...                 # Test files
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License.

---

**Note**: The Windows build instructions are untested. If you encounter issues, please report them so we can improve the documentation.
