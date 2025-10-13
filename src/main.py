
import sys
import os
import subprocess
import ctypes  # Windows DPI awareness
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from repository import MySQLRepository


repo = MySQLRepository()


BASE_DIR = Path(__file__).resolve().parent
VIEWS_DIR = BASE_DIR / "views"


def open_window(script_name: str) -> None:
    """Launch a view script from src/views with the same Python interpreter."""
    script_path = VIEWS_DIR / script_name
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return
    subprocess.Popen([sys.executable, str(script_path)], cwd=str(BASE_DIR))


def build_ui() -> tk.Tk:
   
    if sys.platform.startswith("win"):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    root.title("Academic Database")

    
    try:
        if sys.platform.startswith("win"):
            root.state("zoomed")             # maximized on Windows
        else:
            root.attributes("-zoomed", True) # some X11/Wayland builds support this
    except tk.TclError:
        
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

   
    try:
        root.tk.call("tk", "scaling", 1.15)
    except tk.TclError:
        pass

  
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Card.TFrame", padding=24)
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    style.configure("TButton", padding=(16, 10), font=("Segoe UI", 12))

    
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    
    wrapper = ttk.Frame(root, padding=24)
    wrapper.grid(row=0, column=0, sticky="nsew")
    wrapper.rowconfigure(0, weight=1)
    wrapper.columnconfigure(0, weight=1)

   
    card = ttk.Frame(wrapper, style="Card.TFrame")
    card_width = 520
    card_height = 280
    
    card.place(relx=0.5, rely=0.5, anchor="center", width=card_width, height=card_height)

  
    for r in range(5):
        card.rowconfigure(r, weight=1)
    card.columnconfigure(0, weight=1)

    ttk.Label(card, text="Academic Database", style="Title.TLabel")\
        .grid(row=0, column=0, sticky="n", pady=(0, 8))

    btns = ttk.Frame(card)
    btns.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
    btns.columnconfigure(0, weight=1)
    for r in range(3):
        btns.rowconfigure(r, weight=1)

    ttk.Button(
        btns, text="Students",
        command=lambda: open_window("list_students.py")
    ).grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    ttk.Button(
        btns, text="Lecturers",
        command=lambda: open_window("list_lecturers.py")
    ).grid(row=1, column=0, sticky="nsew", padx=6, pady=6)

    ttk.Button(
        btns, text="Courses",
        command=lambda: open_window("list_courses.py")
    ).grid(row=2, column=0, sticky="nsew", padx=6, pady=6)

    
    def on_close():
        try:
            repo.close()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    return root


if __name__ == "__main__":
    app = build_ui()
    app.mainloop()
