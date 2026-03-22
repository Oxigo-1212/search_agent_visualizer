from __future__ import annotations

import time
import tracemalloc
import tkinter as tk
from tkinter import messagebox, ttk

from .state import PuzzleState
from .problem import PuzzleProblem
from .search_agents.algorithm import bfs
from .utils import action_extractor


class PuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Solver")
        self.geometry("1040x720")
        self.resizable(False, False)
        self.configure(bg="#0f172a")

        self.colors = {
            "bg": "#0f172a",
            "panel": "#111827",
            "card": "#1f2937",
            "card_alt": "#243244",
            "text": "#f8fafc",
            "muted": "#cbd5e1",
            "accent": "#38bdf8",
            "accent_hover": "#0ea5e9",
            "success": "#22c55e",
            "success_hover": "#16a34a",
            "warning": "#f59e0b",
            "warning_hover": "#d97706",
            "tile": "#e2e8f0",
            "tile_alt": "#dbe4ee",
            "tile_blank": "#64748b",
            "tile_selected": "#60a5fa",
        }

        self.title_font = ("Segoe UI", 24, "bold")
        self.subtitle_font = ("Segoe UI", 11)
        self.section_font = ("Segoe UI", 12, "bold")
        self.tile_font = ("Segoe UI", 28, "bold")
        self.body_font = ("Segoe UI", 11)
        self.mono_font = ("Cascadia Mono", 11)

        self._setup_style()

        # Initial and Goal states
        self.goal_state = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))
        # Example initial solvable state
        self.current_state = PuzzleState((1, 2, 3, 4, 0, 5, 7, 8, 6))

        self.current_buttons = []
        self.goal_buttons = []
        self.is_solving = False
        self.current_swap_selection: int | None = None  # For initial tile swap mode
        self.goal_swap_selection: int | None = None  # For goal tile swap mode

        self.create_widgets()
        self.update_current_grid()
        self.update_goal_grid()

    def create_widgets(self):
        shell = ttk.Frame(self, style="App.TFrame", padding=24)
        shell.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(shell, style="App.TFrame")
        header.pack(fill=tk.X, pady=(0, 18))

        title_lbl = ttk.Label(header, text="8-Puzzle Solver", style="Title.TLabel")
        title_lbl.pack(anchor=tk.W)

        subtitle = ttk.Label(
            header,
            text="Edit the initial and goal states, then solve and watch the animation.",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor=tk.W, pady=(4, 0))

        boards_frame = ttk.Frame(shell, style="App.TFrame")
        boards_frame.pack(pady=(8, 16))

        # Initial/current board (editable via tile swap)
        current_frame = ttk.LabelFrame(
            boards_frame,
            text="Initial State (Click two tiles to swap)",
            style="Card.TLabelframe",
            padding=16,
        )
        current_frame.grid(row=0, column=0, padx=(0, 18))

        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(
                    current_frame,
                    text="",
                    font=self.tile_font,
                    width=3,
                    height=1,
                    bg=self.colors["tile"],
                    fg="#0f172a",
                    activebackground=self.colors["tile_selected"],
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    command=lambda r=r, c=c: self.current_tile_click(r, c),
                )
                btn.grid(row=r, column=c, padx=6, pady=6, ipadx=3, ipady=4)
                row_buttons.append(btn)
            self.current_buttons.append(row_buttons)

        # Goal board (editable via tile swap)
        goal_frame = ttk.LabelFrame(
            boards_frame,
            text="Goal State (Click two tiles to swap)",
            style="Card.TLabelframe",
            padding=16,
        )
        goal_frame.grid(row=0, column=1, padx=(18, 0))

        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(
                    goal_frame,
                    text="",
                    font=self.tile_font,
                    width=3,
                    height=1,
                    bg=self.colors["tile_alt"],
                    fg="#0f172a",
                    activebackground=self.colors["tile_selected"],
                    activeforeground="#ffffff",
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    command=lambda r=r, c=c: self.goal_tile_click(r, c),
                )
                btn.grid(row=r, column=c, padx=6, pady=6, ipadx=3, ipady=4)
                row_buttons.append(btn)
            self.goal_buttons.append(row_buttons)

        # Controls Frame
        self.control_frame = ttk.Frame(shell, style="App.TFrame")
        self.control_frame.pack(pady=(0, 16))

        self.btn_shuffle = ttk.Button(
            self.control_frame,
            text="Shuffle Initial",
            command=self.shuffle_board,
            style="Warning.TButton",
        )
        self.btn_shuffle.grid(row=0, column=0, padx=10, ipadx=6, ipady=4)

        self.btn_solve = ttk.Button(
            self.control_frame,
            text="Solve (BFS)",
            command=self.solve_puzzle,
            style="Success.TButton",
        )
        self.btn_solve.grid(row=0, column=1, padx=10, ipadx=6, ipady=4)

        # Benchmark results Frame
        stats_frame = ttk.LabelFrame(
            shell,
            text="Benchmark Results",
            style="Card.TLabelframe",
            padding=14,
        )
        stats_frame.pack(fill=tk.X)

        self.stats_var = tk.StringVar()
        self.stats_var.set(
            "Time: N/A\nMemory: N/A\nNodes Expanded: N/A\nPath Length: N/A"
        )

        self.stats_label = ttk.Label(
            stats_frame,
            textvariable=self.stats_var,
            justify=tk.LEFT,
            style="Stats.TLabel",
            padding=10,
        )
        self.stats_label.pack(anchor=tk.W)

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure(
            "Card.TLabelframe",
            background=self.colors["card"],
            foreground=self.colors["text"],
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.colors["card"],
            foreground=self.colors["muted"],
            font=self.section_font,
        )
        style.configure(
            "Title.TLabel",
            background=self.colors["bg"],
            foreground=self.colors["text"],
            font=self.title_font,
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.colors["bg"],
            foreground=self.colors["muted"],
            font=self.subtitle_font,
        )
        style.configure(
            "Stats.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=self.mono_font,
        )
        style.configure("TButton", font=self.body_font, padding=(16, 10), relief="flat")
        style.map(
            "Warning.TButton",
            background=[
                ("active", self.colors["warning_hover"]),
                ("!disabled", self.colors["warning"]),
            ],
            foreground=[("!disabled", "white")],
        )
        style.map(
            "Success.TButton",
            background=[
                ("active", self.colors["success_hover"]),
                ("!disabled", self.colors["success"]),
            ],
            foreground=[("!disabled", "white")],
        )

    def current_tile_click(self, r: int, c: int):
        """Handle click on initial/current board tile for swap mode."""
        if self.is_solving:
            return

        idx = r * 3 + c

        if self.current_swap_selection is None:
            # First selection
            self.current_swap_selection = idx
            self.update_current_grid()
        else:
            # Second selection - perform swap
            first_idx = self.current_swap_selection
            self.current_swap_selection = None

            if first_idx == idx:
                # Same tile clicked, deselect
                self.update_current_grid()
                return

            tiles = list(self.current_state.tiles)
            tiles[first_idx], tiles[idx] = tiles[idx], tiles[first_idx]
            self.current_state = PuzzleState(tuple(tiles))
            self.update_current_grid()
            self.stats_var.set(
                "Time: N/A\nMemory: N/A\nNodes Expanded: N/A\nPath Length: N/A"
            )

    def update_current_grid(self):
        tiles = self.current_state.tiles
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                val = tiles[idx]
                bg_color = "#95a5a6" if val == 0 else "#ecf0f1"
                # Highlight selected tile for swap
                if self.current_swap_selection == idx:
                    bg_color = "#74b9ff"
                self.current_buttons[r][c].config(
                    text="" if val == 0 else str(val),
                    bg=bg_color,
                )

    def update_goal_grid(self):
        tiles = self.goal_state.tiles
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                val = tiles[idx]
                bg_color = "#95a5a6" if val == 0 else "#dfe6e9"
                # Highlight selected tile for swap
                if self.goal_swap_selection == idx:
                    bg_color = "#74b9ff"
                self.goal_buttons[r][c].config(
                    text="" if val == 0 else str(val),
                    bg=bg_color,
                )

    def goal_tile_click(self, r: int, c: int):
        """Handle click on goal board tile for swap mode."""
        if self.is_solving:
            return

        idx = r * 3 + c

        if self.goal_swap_selection is None:
            # First selection
            self.goal_swap_selection = idx
            self.update_goal_grid()
        else:
            # Second selection - perform swap
            first_idx = self.goal_swap_selection
            self.goal_swap_selection = None

            if first_idx == idx:
                # Same tile clicked, deselect
                self.update_goal_grid()
                return

            tiles = list(self.goal_state.tiles)
            tiles[first_idx], tiles[idx] = tiles[idx], tiles[first_idx]
            self.goal_state = PuzzleState(tuple(tiles))
            self.update_goal_grid()
            self.stats_var.set(
                "Time: N/A\nMemory: N/A\nNodes Expanded: N/A\nPath Length: N/A"
            )

    def shuffle_board(self):
        if self.is_solving:
            return

        import random

        # Perform random valid moves from the current state
        state = self.current_state
        problem = PuzzleProblem(state, self.goal_state)
        # 50 random walks to shuffle
        for _ in range(50):
            neighbors = problem.get_neighbors(state)
            state = random.choice(neighbors)
        self.current_state = state
        self.update_current_grid()
        self.stats_var.set(
            "Time: N/A\nMemory: N/A\nNodes Expanded: N/A\nPath Length: N/A"
        )

    def solve_puzzle(self):
        if self.is_solving:
            return

        self.is_solving = True
        self.btn_solve.config(state=tk.DISABLED, text="Solving...")
        self.btn_shuffle.config(state=tk.DISABLED)
        self.update()  # Force UI update before heavy computation

        problem = PuzzleProblem(self.current_state, self.goal_state)

        tracemalloc.start()
        start_time = time.perf_counter()

        result = bfs(
            problem,
            self.current_state,
            action_extractor,
            return_nodes_expanded=True,
        )

        solution_node, nodes_expanded = result

        end_time = time.perf_counter()
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        time_taken = end_time - start_time
        peak_mem_mb = peak_mem / (1024 * 1024)

        if solution_node:
            solution_path = [node.state for node in solution_node.path()]
            path_len = len(solution_path) - 1

            self.stats_var.set(
                f"Time: {time_taken:.4f} seconds\n"
                f"Memory Peak: {peak_mem_mb:.4f} MB\n"
                f"Nodes Expanded: {nodes_expanded}\n"
                f"Path Length: {path_len} steps"
            )

            self.animate_solution(solution_path)
        else:
            self.stats_var.set(
                f"Time: {time_taken:.4f} seconds\n"
                f"Memory Peak: {peak_mem_mb:.4f} MB\n"
                f"Nodes Expanded: {nodes_expanded}\n"
                f"Path Length: No solution"
            )
            messagebox.showinfo("Result", "No solution found.")
            self.reset_buttons()

    def animate_solution(self, path):
        # path is a list of PuzzleState
        def step(idx):
            if idx < len(path):
                self.current_state = path[idx]
                self.update_current_grid()
                self.after(300, step, idx + 1)
            else:
                self.reset_buttons()

        step(0)

    def reset_buttons(self):
        self.is_solving = False
        self.btn_solve.config(state=tk.NORMAL, text="Solve (BFS)")
        self.btn_shuffle.config(state=tk.NORMAL)


def main():
    app = PuzzleGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
